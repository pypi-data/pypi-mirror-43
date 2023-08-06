import json
import marshmallow
from anyblok_wms_base.testing import WmsTestCase
from anyblok_bus.status import MessageStatus
from bus_schema.odoo8toolskehl_sync.physobj_type import PhysObjTypeSchema


class TestPhysObjType(WmsTestCase):
    """Tests for the Operations that are created as counterparts of Odoo side
    """

    def setUp(self):
        self.Sync = self.registry.Bus.Odoo8Sync.PhysObjType
        self.consume = self.Sync.msg_create_or_update_physobj_type
        self.schema = PhysObjTypeSchema(unknown=marshmallow.INCLUDE)
        self.POT = self.PhysObj.Type

    def test_create_update_frame(self):
        msg1 = dict(parent_code='FRAME',
                    code="Test1",
                    properties=dict(ean13='1337'),
                    behaviours=dict(default_storage_locations=['A/1', 'A/2'],
                                    storable=True)
                    )
        # make sure the test is relevant
        self.schema.validate(msg1)

        self.assertEqual(self.consume(json.dumps(msg1)), MessageStatus.ACK)

        pot = self.single_result(self.POT.query().filter_by(code='Test1'))
        self.assertEqual(pot.properties, msg1['properties'])
        self.assertEqual(pot.behaviours, msg1['behaviours'])

        msg2 = msg1.copy()
        msg2['behaviours']['default_storage_locations'] = ['B/1']
        self.schema.validate(msg2)
        self.assertEqual(self.consume(json.dumps(msg1)), MessageStatus.ACK)

        self.assertEqual(pot.behaviours, msg2['behaviours'])
