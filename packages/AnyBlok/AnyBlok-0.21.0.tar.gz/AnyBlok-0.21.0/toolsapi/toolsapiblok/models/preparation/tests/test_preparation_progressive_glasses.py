from .test_preparation_eyewear_rx import TestPreparationEyewearRx


class TestPreparationProgressiveGlasses(TestPreparationEyewearRx):

    @staticmethod
    def get_preparation_data():
        return {
            'preparation_type': 'PROGRESSIVE_GLASSES',
            'properties': {
                'preparation_data': {
                    'quantity': 1,
                    'reason': 'BC2018SHO-PAR-RAMEQWOXK',
                    'sale_channel_code': 'SHO-PAR-RAM',
                    'use_oma_frame_shape': False,
                    # 'is_pdm_web': False,
                    # 'is_pickup_point': True,
                    # 'is_progressif': True,
                    'edi_purchase_crop_lens': False,
                    'odoo_name': u'OF0000023924',
                    # 'need_purchase_order': True,
                    'note': 'Notes concernant cette préparation',
                },
                'bom': {
                    'inputs': {
                        'frame_code': 'AH16-ECAILLE2-32',
                        'right_lens_code': 'SPG-ORGA-160-G11-RX-L',
                        'left_lens_code': 'SPG-ORGA-160-G11-RX-L',
                    },
                    'glasses_case_code': 'SENGC-006',
                    # 'lens_template': 'SPG-ORGA-160-G11',
                    'right_lens_supplier_code': '920911',
                    # 'right_lens_product_name': 'sync PRG Easy View 16 HC',
                    'left_lens_supplier_code': '920911',
                    # 'left_lens_product_name': 'sync PRG Easy View 16 HC',
                    # 'lens_code': '920911920911',
                },
                'optical_data': {
                    'close_vision': False,
                    'lens_corridor': u'long',
                    'diameter': '65',
                    'right': {
                        'height': '28.5',
                        'addition': '3.00',
                        'axis': '10',
                        'cylinder': u'0.50',
                        'lens_power': u'1.75',
                        'pd': u'33.50',
                        'pd_close': False,
                    },
                    'left': {
                        'height': '28.5',
                        'addition': '3.00',
                        'axis': '160',
                        'cylinder': u'0.50',
                        'lens_power': u'1.50',
                        'pd': u'33.50',
                        'pd_close': False,
                    },
                },
                'wearer': {
                    # 'vision_card': '2018-06-16 13:59:19 - Janis Doe',
                    # 'vision_card_status': 'confirmed',
                    # 'vision_card_wearer': 'Janis Doe',
                    # 'vision_type': 'progressive',
                },
                'binary_data': {
                    'photo_measure_height': None,
                    # 'photo_measure_height_lobj_oid': 10048735,
                    'photo_measure_pd': 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAABmJLR0QAAAAAAAD5Q7t/AAAACXBI\nWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH4AIEDxAwSHUQ1QAAABl0RVh0Q29tbWVudABDcmVhdGVk\nIHdpdGggR0lNUFeBDhcAAAJCSURBVHja7dq/r+lgGAfwb2+spBJ/hcFk4CYEOUGijU0iJxEdWonu\nFiwsEv+ArRY0TSwW4ojtmllEYjVq/BhF424SPw5uLifH8TxJl7dv38f78fZJ+8L8+fjY4YXjF148\nCIAACIAACOCVw3Rrx99vb085wUGvRyuAAAiAAAiAAAiAAAiAAAiAAAiAAAiAAAjgbgAMw5w9jmO9\nXoNlWVitViyXy7PjHMd8PofT6USxWLya79z1X7YCdrvdyXEcqqoiFAqB4zioqnp1zNlsBq/Xi1gs\nhnw+fzXfuZzf6hZQFAWpVAqiKEJRlIt9p9MpPB4PJElCJpN5+GczPTrBZDKBruvw+/1gGAbr9Rrj\n8Rh2u/2k72g0QjgcRi6XgyzLP6MIKooCSZL296koiqhWqyf9BoMBAoEACoXCl03+LgCXCpJhGNA0\nDclkct+WSCSgaRoMwzgYZzgcYrvdwuFw3KXwfosi2Ol04HK5YLPZ9m02mw1utxvtdvtgnHQ6jXK5\njGAwiH6//0/5/qcImh69/JvN5tnKv9lswHHcQZskSTCbzYhGo6jX6+B5/nlrgK7r6PV6WCwWJ9/W\narVCv9+Hrusn18XjcTQaDby/v6NWqz0vQK1WQyQSAcuyJ+csFgt4nv90ghzHodVqQZZlVCqV5wRQ\nFAWCIHx6XhCEi88EPp8P3W4X2WwWpVLpYUWQufVPUvTjKL0MEQABEAABEAABEAABEAABEAABEAAB\n/JS4eVP02sYCrQACIAACIAACIAACIIAni7/l3PgfSTtQRwAAAABJRU5ErkJggg==\n',  # noqa
                    # 'photo_measure_pd_lobj_oid': 10066713,
                }
            },
        }
