import json
from uuid import uuid1

import marshmallow
from anyblok_wms_base.testing import WmsTestCase
from anyblok_bus.status import MessageStatus
from bus_schema.odoo8toolskehl_sync.move import MoveSchema


class TestInternalMove(WmsTestCase):
    """Tests for the Operations that are created as counterparts of Odoo side
    """

    def setUp(self):
        self.Sync = self.registry.Bus.Odoo8Sync.InternalMove
        self.consume = self.Sync.msg_create_internal_move
        self.schema = MoveSchema(unknown=marshmallow.INCLUDE)
        self.PO = self.PhysObj

        self.reason = "SO-TEST"
        self.location_code = "WH-KEHL-INPUT"
        self.loc = self.PO.query().filter_by(
            code=self.location_code).one()
        self.odoo_product_code = "IAH01-NOIR-12"
        self.physobj_type = self.PO.Type.query().filter_by(
            code=self.odoo_product_code).one()
        self.destination_code = "WH-KEHL-STOCK"
        self.dest = self.PO.query().filter_by(
            code=self.destination_code).one()

    def create_physobj(self, qty=1, physobj_code=None):
        apparition = self.Operation.Apparition.create(
            state='done',
            quantity=qty,
            location=self.loc,
            physobj_type=self.physobj_type,
            physobj_code=physobj_code
        )
        return apparition.outcomes

    def test_int_move_all_ok(self):
        avatars = self.create_physobj(qty=1)
        uuid = uuid1()
        msg1 = {
            "uuid": str(uuid),
            "reason": self.reason,
            "location_code": self.location_code,
            "odoo_product_code": self.odoo_product_code,
            "destination_code": self.destination_code,
            "quantity": 1,
        }

        self.assertEqual(
            self.PO.Avatar.query().filter_by(obj=avatars[0].obj,
                                             location=self.loc, state='present').count(),
            1
        )
        self.assertEqual(self.consume(json.dumps(msg1)), MessageStatus.ACK)
        self.assertEqual(
            self.PO.Avatar.query().filter_by(obj=avatars[0].obj,
                                             location=self.loc, state='present').count(),
            0
        )
        self.assertEqual(
            self.PO.Avatar.query().filter_by(obj=avatars[0].obj,
                                             location=self.dest, state='present').count(),
            1
        )

    def test_int_move_type_and_code(self):
        avatars = self.create_physobj(qty=1, physobj_code="A1")
        uuid = uuid1()
        msg1 = {
            "uuid": str(uuid),
            "reason": self.reason,
            "location_code": self.location_code,
            "odoo_product_code": self.odoo_product_code,
            "odoo_production_lot_name": "A1",
            "destination_code": self.destination_code,
            "quantity": 1,
        }

        self.assertEqual(
            self.PO.Avatar.query().filter_by(obj=avatars[0].obj,
                                             location=self.loc, state='present').count(),
            1
        )
        self.assertEqual(self.consume(json.dumps(msg1)), MessageStatus.ACK)
        self.assertEqual(
            self.PO.Avatar.query().filter_by(obj=avatars[0].obj,
                                             location=self.loc, state='present').count(),
            0
        )
        self.assertEqual(
            self.PO.Avatar.query().filter_by(obj=avatars[0].obj,
                                             location=self.dest, state='present').count(),
            1
        )

    def test_int_move_missing_location(self):
        self.create_physobj(qty=1)
        uuid = uuid1()
        msg1 = {
            "uuid": str(uuid),
            "reason": self.reason,
            "location_code": "NOWHERE",
            "odoo_product_code": self.odoo_product_code,
            "destination_code": self.destination_code,
            "quantity": 1,
        }
        with self.assertRaises(LookupError) as arc:
            self.consume(json.dumps(msg1))

        self.assertEqual(arc.exception.args, ('location', 'NOWHERE'))

    def test_int_move_missing_destination(self):
        self.create_physobj(qty=1)
        uuid = uuid1()
        msg1 = {
            "uuid": str(uuid),
            "reason": self.reason,
            "location_code": self.location_code,
            "odoo_product_code": self.odoo_product_code,
            "destination_code": "NOWHERE",
            "quantity": 1,
        }
        with self.assertRaises(LookupError) as arc:
            self.consume(json.dumps(msg1))

        self.assertEqual(arc.exception.args, ('destination', 'NOWHERE'))

    def test_int_move_missing_obj_type(self):
        self.create_physobj(qty=1)
        uuid = uuid1()
        msg1 = {
            "uuid": str(uuid),
            "reason": self.reason,
            "location_code": self.location_code,
            "odoo_product_code": "UNEXISTING",
            "destination_code": self.destination_code,
            "quantity": 1,
        }
        with self.assertRaises(LookupError) as arc:
            self.consume(json.dumps(msg1))

        self.assertEqual(arc.exception.args, ('type', 'UNEXISTING'))

    def test_int_move_obj_missing(self):
        uuid = uuid1()
        msg1 = {
            "uuid": str(uuid),
            "reason": self.reason,
            "location_code": self.location_code,
            "odoo_product_code": self.odoo_product_code,
            "destination_code": self.destination_code,
            "quantity": 1,
        }
        with self.assertRaises(LookupError) as arc:
            self.consume(json.dumps(msg1))

        self.assertEqual(arc.exception.args, ('avatars', 1, self.odoo_product_code, None,
                                              self.location_code))
