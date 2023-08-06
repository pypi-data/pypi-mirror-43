import logging
from anyblok import Declarations
from anyblok_bus import bus_consumer
import marshmallow
from anyblok_bus.status import MessageStatus
from bus_schema.odoo8toolskehl_sync.physobj_type import PhysObjTypeSchema

from bloks_sensee.bloks.sensee_data.sensee_wms.goods_type_data import (
    PhysObjTypeData
)


logger = logging.getLogger(__name__)


@Declarations.register(Declarations.Model.Bus.Odoo8Sync)
class PhysObjType:
    """Reflecting product.product changes on the Odoo 8 side for creation or
    update of PhysObj.Type
    """

    @bus_consumer(queue_name='kehl_create_or_update_physobj_type',
                  schema=PhysObjTypeSchema(unknown=marshmallow.INCLUDE))
    def msg_create_or_update_physobj_type(cls, body=None):
        Type = cls.registry.Wms.PhysObj.Type
        data = body
        pot = Type.query().filter_by(code=data['code']).one_or_none()
        if not pot:
            pot = PhysObjTypeData(registry=cls.registry).create_gt(**data)
            logger.info("A new physobj type has been created: %r", pot)
        else:
            pot = PhysObjTypeData(registry=cls.registry).update_gt(**data)
            logger.info("Physobj type has been updated: %r", pot)

        return MessageStatus.ACK
