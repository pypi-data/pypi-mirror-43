import logging
from anyblok import Declarations
from anyblok_bus import bus_consumer
import marshmallow
from anyblok_bus.status import MessageStatus
from bus_schema.odoo8toolskehl_sync.physobj_type import (
    PhysObjTypeContainerSchema,
)


logger = logging.getLogger(__name__)


@Declarations.register(Declarations.Model.Bus.Odoo8Sync)
class Location:
    """Reflecting stock.location changes on the Odoo 8 side for creation or
    update of locations (PhysObj with type 'location')
    """

    @bus_consumer(queue_name='kehl_odoo8_create_or_update_physobj_type_container',
                  schema=PhysObjTypeContainerSchema(unknown=marshmallow.INCLUDE))
    def msg_create_or_update_location(cls, body=None):
        Wms = cls.registry.Wms
        Operation = Wms.Operation
        PhysObj = Wms.PhysObj
        Type = PhysObj.Type
        data = body
        gt = Type.query().filter_by(code='location').one()
        parent_code = data['parent_code']
        loc_code = data['code']
        logger.info("msg_create_or_update_location, code=%r, parent_code=%r",
                    loc_code, parent_code)
        loc = PhysObj.query().filter_by(code=loc_code, type=gt).one_or_none()
        parent = PhysObj.query().filter_by(code=parent_code, type=gt).one_or_none()
        if loc:
            raise NotImplementedError("Doesn't support updates yet.")

        if parent is None:
            parent = Wms.create_root_container(gt, code=parent_code)
            logger.error("A new parent location %r has been created at the "
                         "Manual intervention required to place it where it "
                         "should (this method doesn't have the information)",
                         parent)

        app = Operation.Apparition.create(state='done',
                                          quantity=1,
                                          location=parent,
                                          physobj_type=gt,
                                          physobj_code=loc_code)
        logger.info("A new location has been created: %r", app.outcomes[0].obj)

        return MessageStatus.ACK
