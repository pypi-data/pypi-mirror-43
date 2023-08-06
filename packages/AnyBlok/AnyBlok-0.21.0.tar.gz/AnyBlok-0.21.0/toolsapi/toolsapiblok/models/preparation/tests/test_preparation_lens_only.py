from .test_preparation_base import TestPreparationBase


class TestPreparationLensOnly(TestPreparationBase):

    def setUp(self):
        super(TestPreparationLensOnly, self).setUp()
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
            'preparation_type': 'LENS_ONLY',
            'properties': {
                'preparation_data': {
                    'quantity': 1,
                    'reason': 'BC2018WEB-PAR-RAMIJCPTR',
                    'sale_channel_code': 'WEB',
                    'use_oma_frame_shape': False,
                    # 'is_pdm_web': False,
                    # 'is_pickup_point': True,
                    # 'is_progressif': False,
                    'edi_purchase_crop_lens': False,
                    'odoo_name': u'OF0000023931',
                    # 'need_purchase_order': False,
                    'note': 'Notes concernant cette préparation',
                },
                'bom': {
                    'glasses_case_code': 'SENGC-006',
                    # 'lens_template': 'SUN-ORGA-160-002',
                    'inputs': {
                        'frame_code': 'FRAME',
                        'right_lens_code': 'SUN-ORGA-160-002+175+150',
                        'left_lens_code': 'SUN-ORGA-160-002+275+075',
                    },
                    'right_lens_supplier_code': '5114598666',
                    # 'right_lens_product_name': 'sync UF Stock Sph 16 HM',
                    'left_lens_supplier_code': '5114598781',
                    # 'left_lens_product_name': 'sync UF Stock Sph 16 HM',
                    # 'lens_code': '51145987815114598666',
                },
                'optical_data': {
                    'close_vision': False,
                    'lens_corridor': None,
                    'diameter': None,
                    'right': {
                        'height': u'18.5',
                        'addition': u'null',
                        'axis': u'80',
                        'cylinder': u'1.50',
                        'lens_power': u'1.75',
                        'pd': u'30.50',
                        'pd_close': False,
                    },
                    'left': {
                        'height': u'18.5',
                        'addition': u'null',
                        'axis': u'100',
                        'cylinder': u'0.75',
                        'lens_power': u'2.75',
                        'pd': u'31.50',
                        'pd_close': False,
                    },
                },
                'wearer': {
                    # 'vision_card': '2018-06-16 14:44:07 - John Doe',
                    # 'vision_card_status': 'confirmed',
                    # 'vision_card_wearer': 'John Doe',
                    # 'vision_type': u'far',
                },
                'binary_data': {
                    'photo_measure_height': None,
                    # 'photo_measure_height_lobj_oid': -1,
                    'photo_measure_pd': 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAABmJLR0QAAAAAAAD5Q7t/AAAACXBI\nWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH4AIEDxAwSHUQ1QAAABl0RVh0Q29tbWVudABDcmVhdGVk\nIHdpdGggR0lNUFeBDhcAAAJCSURBVHja7dq/r+lgGAfwb2+spBJ/hcFk4CYEOUGijU0iJxEdWonu\nFiwsEv+ArRY0TSwW4ojtmllEYjVq/BhF424SPw5uLifH8TxJl7dv38f78fZJ+8L8+fjY4YXjF148\nCIAACIAACOCVw3Rrx99vb085wUGvRyuAAAiAAAiAAAiAAAiAAAiAAAiAAAiAAAjgbgAMw5w9jmO9\nXoNlWVitViyXy7PjHMd8PofT6USxWLya79z1X7YCdrvdyXEcqqoiFAqB4zioqnp1zNlsBq/Xi1gs\nhnw+fzXfuZzf6hZQFAWpVAqiKEJRlIt9p9MpPB4PJElCJpN5+GczPTrBZDKBruvw+/1gGAbr9Rrj\n8Rh2u/2k72g0QjgcRi6XgyzLP6MIKooCSZL296koiqhWqyf9BoMBAoEACoXCl03+LgCXCpJhGNA0\nDclkct+WSCSgaRoMwzgYZzgcYrvdwuFw3KXwfosi2Ol04HK5YLPZ9m02mw1utxvtdvtgnHQ6jXK5\njGAwiH6//0/5/qcImh69/JvN5tnKv9lswHHcQZskSTCbzYhGo6jX6+B5/nlrgK7r6PV6WCwWJ9/W\narVCv9+Hrusn18XjcTQaDby/v6NWqz0vQK1WQyQSAcuyJ+csFgt4nv90ghzHodVqQZZlVCqV5wRQ\nFAWCIHx6XhCEi88EPp8P3W4X2WwWpVLpYUWQufVPUvTjKL0MEQABEAABEAABEAABEAABEAABEAAB\n/JS4eVP02sYCrQACIAACIAACIAACIIAni7/l3PgfSTtQRwAAAABJRU5ErkJggg==\n',  # noqa
                    # 'photo_measure_pd_lobj_oid': 10066719,
                }
            }
        }

    def create_lens_only_preparation(self):
        data = self.get_preparation_data()

        self.preparation = self.Preparation.create(**data)

        self.assertIsInstance(self.preparation,
                              self.Preparation.get_class_from_code(
                                  data["preparation_type"])
                              )
        req_query = self.Request.query().filter_by(
            purpose=['PREPARATION', self.preparation.code])
        self.assertEqual(req_query.count(), 1)

    def test_create_lens_only_preparation(self):
        self.create_lens_only_preparation()

    def test_plan_lens_only_preparation(self):
        self.create_lens_only_preparation()
        inputs = self.get_preparation_inputs()
        rlens_gt = self.PhysObjType.query().filter_by(code=inputs['right_lens_code']).first()
        self.plan_obj_arrival(gt=rlens_gt)
        llens_gt = self.PhysObjType.query().filter_by(code=inputs['left_lens_code']).first()
        self.plan_obj_arrival(gt=llens_gt)

        # plan_one() return True while it's not implemented
        self.assertTrue(self.preparation.plan_one(items=[]))
