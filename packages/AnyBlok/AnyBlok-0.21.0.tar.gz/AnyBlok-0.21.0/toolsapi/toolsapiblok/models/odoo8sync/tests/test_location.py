import json
import marshmallow
from anyblok_wms_base.testing import WmsTestCase
from anyblok_bus.status import MessageStatus
from bus_schema.odoo8toolskehl_sync.physobj_type import (
    PhysObjTypeContainerSchema,
)


class TestLocation(WmsTestCase):
    """Tests for the Operations that are created as counterparts of Odoo side
    """

    def setUp(self):
        self.Sync = self.registry.Bus.Odoo8Sync.Location
        self.consume = self.Sync.msg_create_or_update_location
        self.schema = PhysObjTypeContainerSchema(unknown=marshmallow.INCLUDE)
        self.PO = self.PhysObj

    def test_create_update_location(self):
        PO = self.PO
        msg1 = dict(parent_code='TESTROOT', code='TESTROOT-A')

        self.assertEqual(self.consume(json.dumps(msg1)), MessageStatus.ACK)

        parent = self.single_result(PO.query().filter_by(code='TESTROOT'))
        loc = self.single_result(PO.query().filter_by(code='TESTROOT-A'))

        loc_av = self.single_result(PO.Avatar.query().filter_by(obj=loc))
        self.assertEqual(loc_av.location, parent)

        msg2 = msg1.copy()
        with self.assertRaises(NotImplementedError):
            self.consume(json.dumps(msg2))
