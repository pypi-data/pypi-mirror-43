from .test_preparation_base import TestPreparationBase


class TestPreparationCommon(TestPreparationBase):

    def setUp(self):
        super(TestPreparationCommon, self).setUp()
        # shorcuts
        self.Customer = self.registry.Customer
        self.Address = self.registry.Address
        self.VisionCard = self.registry.VisionCard
        self.Sale = self.registry.Sale
        self.Wms = self.registry.Wms
        self.PhysObj = self.Wms.PhysObj
        self.PhysObjType = self.Wms.PhysObj.Type
        self.Avatar = self.Wms.PhysObj.Avatar
        self.Operation = self.Wms.Operation
        self.Reservation = self.Wms.Reservation
        self.Request = self.Reservation.Request
        self.RequestItem = self.Reservation.RequestItem
        self.Sensee = self.Wms.Sensee
        self.Preparation = self.Sensee.Preparation
        self.npeyewear_gt = self.PhysObjType.query().filter_by(
            code="NP_EYEWEAR").one()
        self.stock = self.PhysObj.query().filter_by(
            code="WH-KEHL-STOCK").one()

    @staticmethod
    def get_preparation_data():
        return {
            'preparation_type': 'FRAME_ONLY',
            'properties': {
                'preparation_data': {
                    'quantity': 1,
                    'reason': 'SO-TEST-00001',
                    'sale_channel_code': 'WEB',
                },
                'bom': {
                    'inputs': {
                        'frame_code': 'IAH01-NOIR-12',
                    }
                }
            }
        }

    def create_basic_preparation(self):
        data = self.get_preparation_data()

        self.preparation = self.Preparation.create(**data)

    def test_preparation_str(self):
        self.create_basic_preparation()
        self.assertEqual(str(self.preparation), self.preparation.code)

    def test_preparation_repr(self):
        self.create_basic_preparation()
        prep_repr = '<Sensee.Preparation.%s: %s>' % (self.preparation.preparation_type,
                                                     self.preparation.code)
        self.assertEqual(self.preparation.__repr__(),
                         prep_repr)

    def test_preparation_polymorphic_query(self):
        self.create_basic_preparation()
        self.assertEqual(self.Preparation.FrameOnly.query().count(), 1)
        self.assertEqual(self.Preparation.FrameOnly.query().count(),
                         self.Preparation.query().filter_by(code=self.preparation.code).count())

    def test_preparation_get_class_from_code_unexisting(self):
        with self.assertRaises(Exception) as arc:
            self.Preparation.get_class_from_code(code="UNEXISTING")

        self.assertEqual(arc.exception.args[0],
                         "Preparation type UNEXISTING unknown")

    def test_preparation_create_not_callable(self):
        self.create_basic_preparation()
        with self.assertRaises(Exception) as arc:
            super(self.Preparation, self.preparation).create()

        self.assertEqual(arc.exception.args[0],
                         "create method is not callable from %s"
                         % self.preparation.__registry_name__)

    def test_plan_preparation_req_is_none(self):
        self.assertFalse(self.Preparation.plan_preparation())

    def test_plan_preparation_without_request_items(self):
        req = self.Request.insert(purpose=["TEST"])
        req.reserve()
        self.assertFalse(self.Preparation.plan_preparation())

    def test_print_tray_labels(self):
        self.create_basic_preparation()
        self.assertEqual(self.registry.Attachment.Document.query().count(), 0)
        self.Preparation.print_tray_labels(labels_type="Test")
        self.assertEqual(self.registry.Attachment.Document.query().count(), 1)

    def test_get_tray_config(self):
        self.assertIsInstance(self.Preparation.get_tray_config(), dict)

    def test_preparation_parser_serialize(self):
        self.create_basic_preparation()
        serialize_result = self.Preparation.Parser.serialize("Model.Wms.Sensee.Preparation", {
            'uuids': [str(p.uuid) for p in self.Preparation.query().all()]
        })
        self.assertIsInstance(serialize_result, dict)
        self.assertEqual(serialize_result['data'], self.Preparation.query().all().to_dict())

    def test_preparation_parser_check_if_file_must_be_generated(self):
        preparation_parser = self.Preparation.Parser("Model.Wms.Sensee.Preparation")
        self.assertTrue(preparation_parser.check_if_file_must_be_generated())
