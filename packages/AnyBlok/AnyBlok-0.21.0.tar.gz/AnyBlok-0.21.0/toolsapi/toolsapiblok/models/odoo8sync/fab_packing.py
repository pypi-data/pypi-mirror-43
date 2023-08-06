import logging
from datetime import datetime
from sqlalchemy import not_
from anyblok import Declarations
from anyblok_bus import bus_consumer
import marshmallow
from anyblok_bus.status import MessageStatus
from bus_schema.odoo8toolskehl_sync.assembly import FinalAssemblySchema
from bus_schema.odoo8toolskehl_sync.departure import DepartureSchema
from bus_schema.odoo8toolskehl_sync.fab_packing import FabPackingSchema

logger = logging.getLogger(__name__)


@Declarations.register(Declarations.Model.Bus.Odoo8Sync)
class FabPacking:
    """Reflecting manufacturing and packing done on the Odoo 8 side.

    These two types of events have to be treated together, because
    it happens often that packing and shipping take place right after
    some manufacturing is done, meaning that we should ensure that the
    bus messages are treated in order, hence a single queue with at most
    one worker.
    """

    ODOO_FINAL_ASSEMBLY_NAME = 'odoo_final'
    MSG_FINAL_ASSEMBLY_DONE = 'FINAL_ASSEMBLY_DONE'
    MSG_DEPARTURE = 'DEPARTURE'

    # putting classmethods in a dict would not work (classmethods objects instead of bound methods)
    SUB_CONSUMERS = {MSG_FINAL_ASSEMBLY_DONE: (FinalAssemblySchema(), 'msg_final_assembly_done'),
                     MSG_DEPARTURE: (DepartureSchema(), 'msg_departure')
                     }

    @bus_consumer(queue_name='kehl_odoo8_fab_packing',
                  schema=FabPackingSchema(unknown=marshmallow.INCLUDE),
                  processes=1)
    def msg_fab_packing(cls, body=None):
        msg_type = body.pop('msg_type')
        sub_schema, sub_consumer = cls.SUB_CONSUMERS[msg_type]
        return getattr(cls, sub_consumer)(**sub_schema.load(body))

    @classmethod
    def msg_final_assembly_done(cls, inputs=None, outcome=None, reason=None, quantity=1):
        logger.info("msg_final_assembly_done inputs=%r, outcome=%r, reason=%r, quantity=%d",
                    inputs, outcome, reason, quantity)

        Assembly = cls.registry.Wms.Operation.Assembly
        if Assembly.query().filter_by(reason=reason).count():
            logger.info("Skipped. An assembly already exists for reason=%s", reason)
            return MessageStatus.ACK

        OdooUtils = cls.registry.OdooUtils
        convert_odoo_product = OdooUtils.odoo8_product_schema_to_tools_wms

        for assembly in range(quantity):
            input_descrs = []
            for inp in inputs:
                type_code, phobj_code = convert_odoo_product(inp)
                input_descrs.append(dict(type_code=type_code,
                                         phobj_code=phobj_code,
                                         location_code=inp['location_code']))

            out_type_code, out_phobj_code = convert_odoo_product(outcome)
            outcome_descr = dict(location_code=outcome['location_code'],
                                 type_code=out_type_code,
                                 phobj_code=out_phobj_code)
            # checked with Hugo: currently, the Assemblies planned by Preparations
            # don't produce any contents Property, hence we don't have either in
            # order to be consistent with them.
            ass, missing = cls.odoo_final_assembly_done(
                input_descrs, outcome_descr, reason=reason)
            logger.info("msg_final_assembly_done created Assembly(id=%d) %d/%d",
                        ass.id, assembly, quantity)
            if missing:
                raise LookupError("msg_final_assembly_done",
                                  "Some inputs not found. Assembly not created.",
                                  missing)

        return MessageStatus.ACK

    @classmethod
    def msg_departure(cls, quantity=1,
                      reason=None, **kwargs):
        logger.info("msg_departure, reason=%r, quantity=%d, kwargs=%r",
                    reason, quantity, kwargs)
        OdooUtils = cls.registry.OdooUtils
        type_code, physobj_code = OdooUtils.odoo8_product_schema_to_tools_wms(
            kwargs, pop=True)

        kwargs.pop('uuid', None)
        departures = [cls.odoo_departure(type_code,
                                         physobj_code=physobj_code,
                                         reason=reason,
                                         **kwargs)
                      for _ in range(quantity)]
        logger.info("msg_departure, created %d Departure(s) wih ids %r",
                    len(departures), [dep.id for dep in departures])
        # raising that could have happened is enough error treatment for now
        return MessageStatus.ACK

    @classmethod
    def odoo_final_assembly_done(cls, input_descrs, outcome_descr,
                                 dt_execution=None,
                                 reason='odoo_sync'):
        """Create an Assembly to account for a final one done by Odoo.

        :param outcome_descr:
            a ``dict`` with keys

            - type_code: a ``code`` of ``PhysObj.Type``
            - location_code: a ``code` of ``PhysObj```
            - props (optional): a :class:`dict` to initialize the outcome
                     Properties (e.g., with a serial number).
            - phobj_code (optional): code for the outcome PhysObj.code

        :param input_descrs:
            an iterable of :class:`dicts <dict>` whose keys are

            - type_code
            - location_code

            with semantics as in ``outcome-descr``

        :param reason: will be stored as ``reason`` field onto the resulting
                       Departure. It would be better for tracking purposes
                       if the caller would include the identifier of the
                       Odoo production order (or similar) that triggered this
                       message.
        :returns: the created Assembly instance, and a list of describing
                  input descriptors that couldn't be resolved. Each element
                  of that list is the pair made of the descriptor, and the
                  exception that describes what's exactly is missing.
        :raises: LookupError if the outcome type or location is missing.

        This Assembly is just a placeholder that represents that the
        inputs have been consumed and the outcome has been produced.
        Its ``name`` attribute is :attr:`ODOO_FINAL_ASSEMBLY_NAME`.

        The normal Assembly methods wouldn't work on that one, since we don't
        put the inputs and outcomes in a single place.

        If needed, a later development could rewrite all these assemblies so
        that inputs are first moved to a common location, and the outcome is
        moved from that location to the included one.

        """
        Wms = cls.registry.Wms
        PhysObj = Wms.PhysObj
        Assembly = Wms.Operation.Assembly
        if dt_execution is None:
            dt_execution = datetime.now()

        outcome_type_code = outcome_descr['type_code']
        outcome_location_code = outcome_descr['location_code']

        outcome_type = PhysObj.Type.query().filter_by(
            code=outcome_type_code).first()
        if outcome_type is None:
            raise LookupError('outcome_type', outcome_type_code)
        outcome_loc = PhysObj.query().filter_by(
            code=outcome_location_code).first()
        if outcome_loc is None:
            raise LookupError('outcome_location', outcome_location_code)

        inputs = []
        missing_inputs = []
        for descr in input_descrs:
            try:
                inputs.append(cls.find_present_avatar(descr['type_code'],
                                                      descr['location_code'],
                                                      physobj_code=descr['phobj_code'],
                                                      exclude=inputs))
            except LookupError as exc:
                missing_inputs.append((descr, exc))

        assembly = Assembly.insert(name=cls.ODOO_FINAL_ASSEMBLY_NAME,
                                   outcome_type=outcome_type,
                                   state='done',
                                   dt_execution=dt_execution,
                                   reason=reason)
        assembly.link_inputs(inputs)

        outcome_phobj = PhysObj.insert(type=outcome_type,
                                       code=outcome_descr.get('phobj_code'))
        outcome_props = outcome_descr.get('props')
        if outcome_props is not None:
            outcome_phobj.update_properties(outcome_props)
        PhysObj.Avatar.insert(obj=outcome_phobj,
                              dt_from=dt_execution,
                              dt_until=None,
                              state='present',
                              location=outcome_loc,
                              outcome_of=assembly)
        for inp_av in inputs:
            inp_av.update(dt_until=dt_execution, state='past')
        return assembly, missing_inputs

    @classmethod
    def find_present_avatar(cls, type_code, location_code,
                            exclude=None,
                            physobj_code=None):
        """Find an Avatar in 'present' state for the given type and location.

        :param type_code: PhysObj.Type code to look for
        :param location_code: PhysObj code (location) where to find the avatar
        :param physobj_code: If specified, only an Avatar of a PhysObj with
                             that code can be returned.
        :param exclude: If specified, do not return the given Avatar. Useful
                        in cases something needs potentially 2 Avatars with
                        the same PhysObj specifications.
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

        if exclude is not None:
            query = query.filter(not_(Avatar.id.in_(ex.id for ex in exclude)))

        av = cls.get_precise_avatar(query=query, location=loc, physobj_code=physobj_code)
        if av is not None:
            return av

        if physobj_code is not None and physobj_code.startswith('RESUPPLY'):
            # let's try again with a less precise query
            all_avatars = query.all()
            if not all_avatars:
                raise LookupError('avatar', 'nowhere')
            if any(av.location != all_avatars[0].location for av in all_avatars):
                raise LookupError('avatar', 'multiple locations')
            return all_avatars[0]

        raise LookupError('avatar', 'nowhere')

    @classmethod
    def get_precise_avatar(cls, query, location, physobj_code=None):
        PhysObj = cls.registry.Wms.PhysObj
        Avatar = PhysObj.Avatar
        precise_query = query.filter(Avatar.location == location)

        av = None
        if physobj_code:
            av = precise_query.filter(PhysObj.code == physobj_code).first()
        if av is not None:
            return av

        av = precise_query.filter(PhysObj.code.is_(None)).first()
        return av

    @classmethod
    def odoo_departure(cls, type_code, location_code,
                       reason='odoo_sync',
                       physobj_code=None,
                       dt_execution=None):
        """Create a Departure to reflect that Odoo shipped a Physical Object.

        In the first use case, this will be hooked onto messages telling
        us that it's gono to Packing on the Odoo side.

        :param type_code: code of PhysObj.Type to ship
        :param location_code: code of PhysObj (location) to find the avatar
        :param dt_execution: departure dt
        :param physobj_code: code of PhysObj to ship
        :param reason: will be stored as ``reason`` field onto the resulting
                       Departure. It would be better for tracking purposes
                       if the caller would include the UUID of the Odoo picking
                       that triggered this message.
        :raises LookupError: if the Departure input Avatar could not be
                             found.
        """
        if physobj_code == '':
            physobj_code = cls.get_physobj_code_from_string(reason=reason)

        if physobj_code and '/' in physobj_code:
            physobj_code = cls.get_physobj_code_from_string(reason=physobj_code)

        if '/' in reason and physobj_code:
            physobj_code = cls.get_physobj_code_from_string(reason=reason)

        if (type_code.startswith("SENGC")
                or type_code.startswith("BOX")
                or type_code in ["SOLOLENS-PAIR", "SOLOLENS_SRV01"]):
            gt = cls.registry.Wms.PhysObj.Type.query().filter_by(code=type_code).one()
            loc = cls.registry.Wms.PhysObj.query().filter_by(code=location_code).one()
            cls.registry.Wms.Operation.Apparition.create(
                state='done',
                reason=reason,
                comment="System apparition of good",
                quantity=1,
                location=loc,
                physobj_type=gt,
                physobj_code=physobj_code)

        avatar = cls.find_present_avatar(type_code, location_code,
                                         physobj_code=physobj_code)

        if dt_execution is None:
            dt_execution = datetime.now()
        return cls.registry.Wms.Operation.Departure.create(
            state='done',
            dt_execution=dt_execution,
            reason=reason,
            input=avatar)

    @classmethod
    def get_physobj_code_from_string(cls, reason):
        reasons = [x.strip() for x in reason.split('/')]
        physobj_code = ""
        for code in reasons:
            if code.startswith('OF'):
                physobj_code = code
        return physobj_code
