from anyblok_pyramid.tests.testcase import PyramidBlokTestCase


class TestApiv1NpEyewear(PyramidBlokTestCase):

    def setUp(self):
        super(TestApiv1NpEyewear, self).setUp()
        self.user = self.registry.User.insert(
            email='t@t', login='test', first_name='test', last_name='test')
        self.registry.User.CredentialStore.insert(
            login='test', password='testpassword')
        resp = self.webserver.post_json(
            '/api/v1/login', {'login': 'test', 'password': 'testpassword'})
        self.headers = {"cookie": resp.headers["Set-Cookie"]}
        self.Wms = self.registry.Wms
        self.Location = self.Wms.Location
        self.Reservation = self.Wms.Reservation
        self.PhysObjType = self.Wms.PhysObj.Type
        self.Operation = self.Wms.Operation
        self.Preparation = self.Wms.Sensee.Preparation

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

    def create_preparation(self):
        data = self.get_preparation_data()

        preparation = self.Preparation.create(**data)
        for req in preparation.requests:
            req_items = self.Reservation.RequestItem.query().filter_by(
                    request=req).all()
            for item in req_items:
                arrival_gt = self.PhysObjType.query().filter_by(
                    code=item.goods_type.code).one()
                arrival_location = arrival_gt.get_default_storage_location()
                self.Operation.Arrival.create(goods_type=arrival_gt,
                                              location=arrival_location,
                                              state='done')
            req.reserve()

        self.Preparation.plan_preparation()
        return preparation

    def test_get_must_be_authenticated(self):
        preparation = self.create_preparation()
        response_protected = self.webserver.get(
            '/api/v1/wms/preparations/np-eyewear/' + str(preparation.uuid),
            status=401
        )
        self.assertIsNone(response_protected.request.authorization)
        self.assertEqual(response_protected.status, '401 Unauthorized')

    def test_get(self):
        preparation = self.create_preparation()
        response = self.webserver.get(
            '/api/v1/wms/preparations/np-eyewear/' + str(preparation.uuid),
            headers=self.headers,
            )
        self.assertEqual(response.status_code, 200)
