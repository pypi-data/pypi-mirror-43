import logging
from anyblok import Declarations
from anyblok_bus import bus_consumer
import marshmallow
from anyblok_bus.status import MessageStatus
from bus_schema.odoo8toolskehl_sync.move import MoveSchema


logger = logging.getLogger(__name__)


@Declarations.register(Declarations.Model.Bus.Odoo8Sync)
class InternalMove:
    """Reflecting stock.move_lines changes on the Odoo 8 side for
    internal moves only
    """

    @bus_consumer(queue_name='kehl_odoo8_internal_move',
                  schema=MoveSchema(unknown=marshmallow.INCLUDE))
    def msg_create_internal_move(cls, body=None):
        """ Create moves to reflect internal moves done by Odoo
        :param body:
        :return:
        """
        Wms = cls.registry.Wms
        Operation = Wms.Operation
        PhysObj = Wms.PhysObj
        data = body
        reason = data['reason']
        location_code = data['location_code']
        destination_code = data['destination_code']
        odoo_product_code = data['odoo_product_code']
        quantity = data['quantity']
        logger.info("msg_create_internal_move, "
                    "reason=%s ,loc=%s, physobj_type=%s, quantity=%d, dest=%s",
                    reason, location_code, odoo_product_code, quantity, destination_code)
        OdooUtils = cls.registry.OdooUtils
        convert_odoo_product = OdooUtils.odoo8_product_schema_to_tools_wms
        type_code, phobj_code = convert_odoo_product(data)

        if type_code in ["SOLOLENS-PAIR", "SOLOLENS_SRV01"] and location_code == "WH-KEHL_ATELIER":
            gt = cls.registry.Wms.PhysObj.Type.query().filter_by(code=type_code).one()
            loc = cls.registry.Wms.PhysObj.query().filter_by(code=location_code).one()
            cls.registry.Wms.Operation.Apparition.create(
                state='done',
                reason=reason,
                comment="Customer frame [%s] apparition" % type_code,
                quantity=1,
                location=loc,
                physobj_type=gt,
                physobj_code=phobj_code)

        avs = cls.find_present_avatars(type_code, location_code, quantity, physobj_code=phobj_code)
        dest = PhysObj.query().filter_by(code=destination_code).one_or_none()
        if dest is None:
            raise LookupError('destination', destination_code)

        for av in avs:
            if av.obj.code is None:
                logger.info("associating phobj=%r to reason=%s",
                            av.obj, reason)
                av.obj.code = reason
            Operation.Move.create(
                reason=reason,
                state="done",
                input=av,
                destination=dest,
            )
            logger.info("msg_create_internal_move: "
                        "a move have been created, reason=%s, input=%r, dest=%r",
                        reason, av, dest)

        return MessageStatus.ACK

    @classmethod
    def find_present_avatars(cls, type_code, location_code,
                             qty_requested=1,
                             physobj_code=None):
        """Find an Avatar in 'present' state for the given type and location.

        :param type_code: PhysObj.Type code to look for
        :param location_code: PhysObj code (location) where to find the avatar
        :param qty_requested: Quantity of avatars to find, default 1
        :param physobj_code: If specified, only an Avatar of a PhysObj with
                             that code can be returned.
        :returns: the Avatar
        :raises: LookupError(reason) where ``reason`` can be:

                 - 'type': no PhysObj.Type has not been found with the given
                           code.
                 - 'location': no PhysObj has been found with the given code.
                 - 'avatar': both the PhysObj.Type and the location could be
                             resolved, but no avatar for a physical object of
                             that type has been found at that location in the
                             ``present`` state.
        """
        PhysObj = cls.registry.Wms.PhysObj
        pot = PhysObj.Type.query().filter_by(code=type_code).first()
        if pot is None:
            raise LookupError('type', type_code)
        loc = PhysObj.query().filter_by(code=location_code).first()
        if loc is None:
            raise LookupError('location', location_code)
        # no need to check if loc is a container, it would simply lead to
        # the Avatar not been found
        Avatar = PhysObj.Avatar
        query = Avatar.query().join(Avatar.obj).filter(
            PhysObj.type == pot,
            Avatar.state == 'present')

        precise_query = query.filter(Avatar.location == loc)

        other_query = precise_query.filter(PhysObj.code.is_(None))
        if physobj_code:
            precise_query = precise_query.filter(PhysObj.code == physobj_code)

        if precise_query.count() >= qty_requested:
            return precise_query.limit(qty_requested).all()

        if other_query.count() >= qty_requested:
            return other_query.limit(qty_requested).all()

        raise LookupError('avatars', qty_requested, type_code, physobj_code, location_code)
