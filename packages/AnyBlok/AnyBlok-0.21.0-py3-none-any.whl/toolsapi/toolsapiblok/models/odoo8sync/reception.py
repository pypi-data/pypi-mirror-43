from anyblok import Declarations
from anyblok_bus.status import MessageStatus
from anyblok_bus import bus_consumer
import marshmallow
from bus_schema.odoo8toolskehl_sync.reception import (DoneReceptionSchema,
                                                      ShelvedReceptionLineSchema)
from bus_schema.odoo8toolskehl_sync.recept_shelving import (
    ReceptShelvingSchema, MSG_RECEPTION_DONE, MSG_SHELVING_DONE)
import logging

logger = logging.getLogger(__name__)

Model = Declarations.Model
Mixin = Declarations.Mixin


@Declarations.register(Model)
class Reception:
    """Reflecting reception and shelving on the Odoo 8 side.

    These two types of events have to be treated together to ensure
    that the bus messages are treated in order, hence a single queue.
    """

    # putting classmethods in a dict would not work (classmethods objects instead of bound methods)
    SUB_CONSUMERS = {MSG_RECEPTION_DONE: (DoneReceptionSchema(), 'msg_reception_done'),
                     MSG_SHELVING_DONE: (ShelvedReceptionLineSchema(), 'msg_shelving_done')
                     }

    @bus_consumer(queue_name="kehl_odoo8_recept_shelving", processes=1,
                  schema=ReceptShelvingSchema(unknown=marshmallow.INCLUDE))
    def msg_recept_shelving(cls, body=None):
        msg_type = body.pop('msg_type')
        logger.info("message received: %s", msg_type)
        sub_schema, sub_consumer = cls.SUB_CONSUMERS[msg_type]
        return getattr(cls, sub_consumer)(**sub_schema.load(body))

    @classmethod
    def msg_reception_done(cls, **kwargs):
        """Create a Reception to relfect the one done by Odoo

        :param kwargs:
            - sender_address
            - recipient_address
            - carrier
            - lines: content of the reception
                - odoo_product_code
        :return: the bus MessageStatus
        :raises
        """
        if cls.query().filter_by(uuid=kwargs['uuid']).count():
            logger.warning("message already exists")
            return MessageStatus.ACK

        reason = kwargs['reason']
        Departure = cls.registry.Wms.Operation.Departure
        if "WEBPDM" in reason and Departure.query().filter_by(
                reason=reason).count() == 0:
            logger.warning("This is a return for a WEBPDM, the Departure"
                           "associated should exist before the Arrival")
            return MessageStatus.NACK

        kwargs['sender_address'] = cls.get_address(**kwargs['sender_address'])
        kwargs['recipient_address'] = cls.get_address(**kwargs['recipient_address'])
        if kwargs.get('carrier'):
            kwargs['carrier'] = cls.registry.Delivery.Carrier.query().filter_by(
                code=kwargs['carrier']).one()

        lines = kwargs.pop('lines', [])
        Type = cls.registry.Wms.PhysObj.Type
        OdooUtils = cls.registry.OdooUtils
        convert_odoo_product = OdooUtils.odoo8_product_schema_to_tools_wms
        for line in lines:
            type_code, phobj_code = convert_odoo_product(line, pop=True)

            if phobj_code is not None:
                raise NotImplementedError(  # pragma no cover
                    "Can't treat physical objects with code field yet. "
                    "PhysObj.Type.code=%r, PhysObj.code=%r" % (
                        type_code, phobj_code))
            line['physobj_type'] = Type.query().filter_by(code=type_code).one()

        reception = cls.create(kwargs, lines=lines)
        # check the flush before ACK, mean that the DB and workflow has verified
        # the arrival with planned state
        reception.update(state='done')
        logger.info("Reception done: %r", reception.uuid)
        return MessageStatus.ACK

    @classmethod
    def change_shelving_destination(cls, move, destination_code):
        destination = cls.registry.Wms.PhysObj.query().filter_by(
            code=destination_code).one_or_none()
        if destination is None:
            raise LookupError('destination', destination_code)
        move.alter_destination(destination)

    @classmethod
    def msg_shelving_done(cls, **kwargs):
        """Shelve a physobj after it was done by Odoo.
        It executes ``Operation.Move`` linked to the ``Reception``
        matching with ``reason`` and ``odoo_product_code``

        :param kwargs:
            - reason: the ``reason`` of the ``Reception``
            - odoo_product_code: the Odoo8 product code
            - quantity: the quantity to shelve
        :return: the bus MessageStatus
        :raises LookupError: if the physobj_type or arrivals are missing
                ValueError: if the destination expected is not the given one
        """
        Operation = cls.registry.Wms.Operation
        OdooUtils = cls.registry.OdooUtils
        convert_odoo_product = OdooUtils.odoo8_product_schema_to_tools_wms
        type_code, phobj_code = convert_odoo_product(kwargs)
        if phobj_code is not None:
            raise NotImplementedError(  # pragma no cover
                "Can't treat physical objects with code field (PhysObj.code) "
                "yet (Type.code=%r, PhysObj.code=%r)" % (
                    type_code, phobj_code))
        physobj_type = cls.registry.Wms.PhysObj.Type.query().filter_by(code=type_code).one_or_none()
        if physobj_type is None:
            logger.error("physobj_type %s not found" % type_code)
            raise LookupError('physobj_type', type_code)

        reason = kwargs['reason']
        arrival_query = Operation.Arrival.query().filter_by(reason=reason,
                                                            physobj_type=physobj_type)
        if arrival_query.count() == 0:
            logger.error("arrivals not found for {reason: %s, physobj_type: %s}" %
                         (reason, type_code))
            raise LookupError('arrival', reason, type_code)

        outcome_ids = [arrival.outcomes[0].id for arrival in arrival_query]
        moves_query = Operation.Move.query()
        join_result = Operation.query_join_input_physobj(query=moves_query)
        moves_query = join_result['query']
        moves_query = moves_query.filter(join_result['av_alias'].id.in_(outcome_ids))
        total_count = moves_query.count()
        if total_count == 0:
            logger.error("moves not found for {reason: %s, physobj_type: %s}" % (reason, type_code))
            raise LookupError('move', reason, type_code)

        moves_query = moves_query.filter(Operation.state == 'planned')
        planned_count = moves_query.count()
        if planned_count == 0:
            logger.warning("all moves (%d) have already been executed "
                           "{reason: %s, physobj_type: %s}",
                           total_count,
                           reason,
                           type_code)
            return MessageStatus.ACK

        qty_to_shelve = kwargs['quantity']
        if qty_to_shelve > planned_count:
            # quantity to shelve has not matched with Wms.Operation.Move lines
            logger.error("quantity to shelve (%d) doesn't match with "
                         "Wms.Operation.Move lines count (%d)" %
                         (qty_to_shelve, planned_count))
            return MessageStatus.NACK

        moves = moves_query.limit(qty_to_shelve).all()
        for move in moves:
            expected_dest_code = move.destination.code
            odoo_dest_code = kwargs['destination_code']
            if expected_dest_code != odoo_dest_code:
                if 'WH-KEHL-INPUT' == expected_dest_code:
                    cls.change_shelving_destination(move=move,
                                                    destination_code=odoo_dest_code)
                else:
                    logger.error('destination expected %s but got %s'
                                 % (expected_dest_code, odoo_dest_code))
                    raise ValueError('destination (expected, received)',
                                     expected_dest_code, odoo_dest_code)

            move.execute()
        logger.info("Moves executed (%d): %r", qty_to_shelve, moves.id)
        return MessageStatus.ACK
