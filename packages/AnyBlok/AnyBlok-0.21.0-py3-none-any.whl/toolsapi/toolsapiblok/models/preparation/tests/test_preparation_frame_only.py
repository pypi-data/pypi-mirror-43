from .test_preparation_base import TestPreparationBase


class TestPreparationFrameOnly(TestPreparationBase):

    def setUp(self):
        super(TestPreparationFrameOnly, self).setUp()
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

    def create_frame_only_preparation(self):
        data = self.get_preparation_data()

        self.preparation = self.Preparation.create(**data)

        self.assertIsInstance(self.preparation,
                              self.Preparation.get_class_from_code(
                                  data["preparation_type"])
                              )
        req_query = self.Request.query().filter_by(
            purpose=['PREPARATION', self.preparation.code])
        self.assertEqual(req_query.count(), 1)

    def test_create_frame_only_preparation(self):
        self.create_frame_only_preparation()

    def test_plan_frame_only_preparation(self):
        self.create_frame_only_preparation()
        inputs = self.get_preparation_inputs()
        frame_gt = self.PhysObjType.query().filter_by(code=inputs['frame_code']).first()
        self.plan_obj_arrival(gt=frame_gt)

        # plan_one() return True while it's not implemented
        self.assertTrue(self.preparation.plan_one(items=[]))
