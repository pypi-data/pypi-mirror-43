from anyblok.tests.testcase import BlokTestCase
from anyblok_bus.status import MessageStatus
from uuid import uuid1
from json import dumps
from bus_schema.odoo8toolskehl_sync.recept_shelving import (
    MSG_RECEPTION_DONE, MSG_SHELVING_DONE)


class TestReception(BlokTestCase):
    """ Test Sensee wms"""

    def setUp(self):
        super(TestReception, self).setUp()
        self.Sync = self.registry.Reception
        self.Type = self.registry.Wms.PhysObj.Type
        self.Location = self.registry.Wms.Location
        self.Reception = self.registry.Reception
        self.reason = "PO00001"
        self.physobj_type = self.registry.Wms.PhysObj.Type.query().filter_by(
            code="IAH01-NOIR-12").one()
        self.location = self.registry.Wms.Location.query().limit(1).one()
        self.carrier = self.registry.Delivery.Carrier.insert(name="MY CARRIER",
                                                             code="MYCARRIER")

    def build_reception_done_message(self):
        uuid = uuid1()
        default_mesg = dict(
            msg_type=MSG_RECEPTION_DONE,
            uuid=str(uuid),
            recipient_address=dict(
                first_name="Jon",
                last_name="Doe",
                street1="1 street",
                street2="crossroad",
                street3="♥",
                zip_code="66000",
                state="A region",
                city="Perpignan",
                country="FRA",
                phone1="0977552210",
            ),
            sender_address=dict(
                first_name="Shipping",
                last_name="services",
                company_name="Acme",
                street1="1 company street",
                zip_code="75000",
                state="",
                city="Paris",
                country="FRA",
            ),
            carrier=self.carrier.code,
            pack='Pack',
            reason=self.reason,
            tracking_number="8R00000",
            lines=[dict(
                location_code=self.location.code,
                # let's assume we have a one-to-one
                odoo_product_code=self.physobj_type.code,
                quantity=2,
            )])
        return default_mesg

    def create_reception_by_bus(self, mesg=None):
        default_mesg = self.build_reception_done_message()
        message = mesg if mesg is not None else default_mesg
        self.assertEqual(self.Sync.msg_recept_shelving(dumps(message)),
                         MessageStatus.ACK)
        return self.Reception.query().get(default_mesg['uuid'])

    def test_create_done_reception_by_bus(self):
        reception = self.create_reception_by_bus()
        self.assertIsNotNone(reception)
        self.assertEqual(len(reception.lines), 1)
        self.assertEqual(len(reception.lines[0].operations), 2)
        self.assertEqual(reception.state, 'done')

    def test_reception_done_message_already_exists(self):
        reception = self.create_reception_by_bus()
        second_message = self.build_reception_done_message()
        second_message.update(uuid=str(reception.uuid))
        self.assertEqual(self.Sync.msg_recept_shelving(dumps(second_message)),
                         MessageStatus.ACK)

    def test_shelve_reception_line_by_bus(self):
        Move = self.registry.Wms.Operation.Move
        self.create_reception_by_bus()
        uuid = uuid1()
        message = dict(
            msg_type=MSG_SHELVING_DONE,
            uuid=str(uuid),
            reason=self.reason,
            destination_code=self.location.code,
            odoo_product_code=self.physobj_type.code,
            quantity=2,
        )
        self.assertEqual(Move.query().filter_by(state="planned", reason=self.reason).count(),
                         2)
        self.assertEqual(self.Sync.msg_recept_shelving(dumps(message)),
                         MessageStatus.ACK)
        self.assertEqual(Move.query().filter_by(state="planned", reason=self.reason).count(),
                         0)
        self.assertEqual(Move.query().filter_by(state="done", reason=self.reason).count(),
                         2)

    def test_shelve_reception_line_missing_move(self):
        """LookupError due to missing move"""
        self.create_reception_by_bus()
        uuid = uuid1()
        message = dict(
            msg_type=MSG_SHELVING_DONE,
            uuid=str(uuid),
            reason=self.reason,
            destination_code=self.location.code,
            odoo_product_code=self.physobj_type.code,
            quantity=2,
        )
        Move = self.registry.Wms.Operation.Move
        Move.query().filter_by(state="planned", reason=self.reason).delete()
        with self.assertRaises(LookupError) as arc:
            self.Sync.msg_recept_shelving(dumps(message))

        self.assertEqual(arc.exception.args, ('move', self.reason, self.physobj_type.code))

    def test_shelve_reception_line_missing_physobj_type(self):
        """LookupError due to missing physobj_type"""
        uuid = uuid1()
        message = dict(
            msg_type=MSG_SHELVING_DONE,
            uuid=str(uuid),
            reason=self.reason,
            destination_code=self.location.code,
            odoo_product_code="missing",
            quantity=2,
        )
        with self.assertRaises(LookupError) as arc:
            self.Sync.msg_recept_shelving(dumps(message))

        self.assertEqual(arc.exception.args, ('physobj_type', "missing"))

    def test_shelve_reception_line_changed_destination_expected_not_input(self):
        """ValueError due to changed destination compared to the planned one"""
        recept = self.create_reception_by_bus()
        # lets change the destination planned from WH-KEHL-INPUT to WH-KEHL-STOCK
        stock_code = "WH-KEHL-STOCK"
        for line in recept.lines:
            line.location_code = stock_code
        Move = self.registry.Wms.Operation.Move
        moves = Move.query().filter_by(reason=recept.reason).all()
        stock_loc = self.registry.Wms.PhysObj.query().filter_by(code=stock_code).one()
        for move in moves:
            move.destination = stock_loc

        uuid = uuid1()
        message = dict(
            msg_type=MSG_SHELVING_DONE,
            uuid=str(uuid),
            reason=self.reason,
            destination_code="NOWHERE",
            odoo_product_code=self.physobj_type.code,
            quantity=2,
        )
        with self.assertRaises(ValueError) as arc:
            self.Sync.msg_recept_shelving(dumps(message))

        self.assertEqual(arc.exception.args, ('destination (expected, received)',
                                              stock_code,
                                              "NOWHERE"))

    def test_shelve_reception_line_changed_destination_expected_input(self):
        """ValueError due to changed destination compared to the planned one"""
        recept = self.create_reception_by_bus()
        Move = self.registry.Wms.Operation.Move
        move = Move.query().filter_by(reason=recept.reason).first()
        uuid = uuid1()
        message = dict(
            msg_type=MSG_SHELVING_DONE,
            uuid=str(uuid),
            reason=self.reason,
            destination_code="NOWHERE",
            odoo_product_code=self.physobj_type.code,
            quantity=2,
        )
        with self.assertRaises(ValueError) as arc:
            self.Sync.msg_recept_shelving(dumps(message))

        self.assertEqual(arc.exception.args, ('destination (expected, received)',
                                              move.destination.code,
                                              "NOWHERE"))

    def test_change_shelving_destination(self):
        recept = self.create_reception_by_bus()
        stock_code = "WH-KEHL-STOCK"
        Move = self.registry.Wms.Operation.Move
        move = Move.query().filter_by(reason=recept.reason).first()
        self.registry.Reception.change_shelving_destination(move=move,
                                                            destination_code=stock_code)

        self.assertEqual(move.destination.code, stock_code)

    def test_shelve_reception_line_changed_destination(self):
        """ValueError due to changed destination compared to the planned one"""
        recept = self.create_reception_by_bus()
        stock_code = "WH-KEHL-STOCK"
        Move = self.registry.Wms.Operation.Move
        move = Move.query().filter_by(reason=recept.reason).first()
        uuid = uuid1()
        message = dict(
            msg_type=MSG_SHELVING_DONE,
            uuid=str(uuid),
            reason=self.reason,
            destination_code=stock_code,
            odoo_product_code=self.physobj_type.code,
            quantity=2,
        )
        with self.assertRaises(ValueError) as arc:
            self.Sync.msg_recept_shelving(dumps(message))

        self.assertEqual(arc.exception.args, ('destination (expected, received)',
                                              move.destination.code,
                                              stock_code))

    def test_shelve_reception_line_missing_arrival(self):
        """LookupError due to missing arrival"""
        uuid = uuid1()
        message = dict(
            msg_type=MSG_SHELVING_DONE,
            uuid=str(uuid),
            reason="NOREASON",
            destination_code=self.location.code,
            odoo_product_code=self.physobj_type.code,
            quantity=2,
        )
        with self.assertRaises(LookupError) as arc:
            self.Sync.msg_recept_shelving(dumps(message))

        self.assertEqual(arc.exception.args, ('arrival', "NOREASON", self.physobj_type.code))

    def test_shelve_reception_line_quantity_higher_than_expected(self):
        """Error due to the quantity shelved is higher than expected"""
        self.create_reception_by_bus()
        uuid = uuid1()
        message = dict(
            msg_type=MSG_SHELVING_DONE,
            uuid=str(uuid),
            reason=self.reason,
            destination_code=self.location.code,
            odoo_product_code=self.physobj_type.code,
            quantity=3,
        )
        self.assertEqual(self.Sync.msg_recept_shelving(dumps(message)),
                         MessageStatus.NACK)

    def test_shelve_reception_line_moves_already_executed(self):
        """Error due to the quantity shelved is higher than expected"""
        recept = self.create_reception_by_bus()
        Move = self.registry.Wms.Operation.Move
        moves = Move.query().filter_by(reason=recept.reason).all()
        moves.execute()
        uuid = uuid1()
        message = dict(
            msg_type=MSG_SHELVING_DONE,
            uuid=str(uuid),
            reason=self.reason,
            destination_code=self.location.code,
            odoo_product_code=self.physobj_type.code,
            quantity=3,
        )
        self.assertEqual(self.Sync.msg_recept_shelving(dumps(message)),
                         MessageStatus.ACK)
