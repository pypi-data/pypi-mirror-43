from datetime import datetime

from anyblok.tests.testcase import BlokTestCase


class TestPreparationRequest(BlokTestCase):

    def setUp(self):
        super(TestPreparationRequest, self).setUp()
        self.Wms = self.registry.Wms
        self.PhysObj = self.Wms.PhysObj
        self.PhysObjType = self.Wms.PhysObj.Type
        self.Operation = self.Wms.Operation
        self.Reservation = self.Wms.Reservation
        self.Request = self.Reservation.Request
        self.RequestItem = self.Reservation.RequestItem
        self.Sensee = self.Wms.Sensee
        self.Preparation = self.Sensee.Preparation

    @staticmethod
    def get_eyewear_items():
        return dict(
            frame_code="IAH01-NOIR-12",
            right_lens_code="SO-4-ARGF-11-3+000+000",
            left_lens_code="SO-4-ARGF-11-3+000+000",
        )

    @staticmethod
    def get_preparation_data():
        return {
            'preparation_type': 'NP_EYEWEAR',
            'properties': {
                'preparation_data': {
                    'quantity': 1,
                    'reason': 'SO-TEST-00001',
                    'odoo_name': 'OF000000001',
                },
                'bom': {
                    'inputs': {
                        'frame_code': 'IAH01-NOIR-12',
                        'right_lens_code': 'SO-4-ARGF-11-3+000+000',
                        'left_lens_code': 'SO-4-ARGF-11-3+000+000',
                    }
                }
            }
        }

    def get_eyewear_inputs(self):
        data = self.get_preparation_data()
        return data['properties']['bom']['inputs']

    def create_eyewear_preparation(self):
        data = self.get_preparation_data()
        inputs = self.get_eyewear_inputs()

        self.quantities = {}
        for k, v in inputs.items():
            qty = self.quantities[v] if v in self.quantities.keys() else 0
            self.quantities[v] = qty + 1

        self.preparation = self.Preparation.create(**data)

    def plan_obj_arrival(self, gt, dt=datetime.now()):
        op = self.Operation.Arrival.create(
            goods_type=gt,
            location=gt.get_default_storage_location(),
            dt_execution=dt,
            state='planned'
        )
        return op.outcomes[0]

    def test_request_reserve(self):
        gt1 = self.goods_type1 = self.PhysObj.Type.insert(code='MG')
        gt2 = self.goods_type2 = self.PhysObj.Type.insert(code='MH')

        goods = []
        av = self.plan_obj_arrival(gt=gt1)
        goods.append(av.obj)
        av = self.plan_obj_arrival(gt=gt1)
        goods.append(av.obj)
        av = self.plan_obj_arrival(gt=gt2)
        goods.append(av.obj)

        req = self.Request(purpose="some delivery")
        self.RequestItem.insert(goods_type=gt1,
                                quantity=2,
                                request=req)
        self.RequestItem.insert(goods_type=gt2,
                                quantity=1,
                                request=req)
        self.assertTrue(req.reserve())
        self.assertTrue(req.reserved)
        reserved_goods = set(r.goods for r in self.Reservation.query().all())
        expected = set(goods)
        self.assertEqual(reserved_goods, expected)

        # idempotency
        req.reserve()
        self.assertEqual(self.Reservation.query().count(), 3)

    def test_request_reserve_preparation(self):
        data = self.get_preparation_data()
        inputs = self.get_eyewear_inputs()

        preparation = self.Preparation.insert(**data)

        req = preparation.request_frame_reservation()
        self.assertEqual(req.purpose, ["PREPARATION", preparation.code])
        self.assertFalse(req.reserve())
        self.assertFalse(req.reserved)

        frame_gt = self.PhysObjType.query().filter_by(
            code=inputs["frame_code"]).one()
        self.plan_obj_arrival(gt=frame_gt)

        self.assertTrue(req.reserve())
        self.assertFalse(req.reserved)

        req = preparation.request_lenses_reservation()
        right_lens_gt = self.PhysObjType.query().filter_by(
            code=inputs["right_lens_code"]).one()
        self.plan_obj_arrival(gt=right_lens_gt)
        self.assertFalse(req.reserve())
        self.assertFalse(req.reserved)

        left_lens_gt = self.PhysObjType.query().filter_by(
            code=inputs["left_lens_code"]).one()
        self.plan_obj_arrival(gt=left_lens_gt)
        self.assertTrue(req.reserve())
        self.assertTrue(req.reserved)
