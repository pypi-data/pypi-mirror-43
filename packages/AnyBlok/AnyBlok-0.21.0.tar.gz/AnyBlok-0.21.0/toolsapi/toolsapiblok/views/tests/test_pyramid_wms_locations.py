from anyblok_pyramid.tests.testcase import PyramidBlokTestCase


class TestApiWmsLocationsBase(PyramidBlokTestCase):
    """ Wms.Location test class throught rest api
    """

    def setUp(self):
        super(TestApiWmsLocationsBase, self).setUp()
        self.user = self.registry.User.insert(
            email='t@t', login='test', first_name='test', last_name='test')
        self.registry.User.CredentialStore.insert(
            login='test', password='testpassword')
        resp = self.webserver.post_json(
            '/api/v1/login', {'login': 'test', 'password': 'testpassword'})
        self.headers = {"cookie": resp.headers["Set-Cookie"]}

    def test_wms_locations_ensure_protected_view(self):
        response_protected = self.webserver.get(
            '/api/v1/wms/locations?limit=10',
            status=401
        )
        self.assertIsNone(response_protected.request.authorization)
        self.assertEqual(response_protected.status, '401 Unauthorized')
        self.assertIsNotNone(response_protected.json_body.get('errors', None))
        self.assertEqual(len(response_protected.json_body.get('errors')), 1)
        self.assertEqual(
            response_protected.json_body.get('errors')[0].get('location'),
            'header'
        )
        self.assertEqual(
            response_protected.json_body.get('errors')[0].get('name'),
            'auth'
        )
        self.assertEqual(response_protected.status_code, 401)

    def test_wms_locations_get(self):
        """Wms.Location GET /api/v1/wms/locations?limit=10"""
        response = self.webserver.get(
            '/api/v1/wms/locations?limit=10',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json_body), 10)

    def test_wms_locations_get_stock_location(self):
        """Wms.Location GET /api/v1/wms/locations?code=WH-KEHL-STOCK"""
        response = self.webserver.get(
            '/api/v1/wms/locations?filter[code][like]=WH-KEHL-STOCK',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json_body), 1)

    # def test_wms_locations_post(self):  TODO must overwrite the resource create to do it
    #     """Wms.Location POST /api/v1/wms/locations"""
    #     response = self.webserver.post_json(
    #         '/api/v1/wms/locations',
    #         dict(code="TEST"),
    #         headers=self.headers,
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json_body.get('code'), "TEST")

    def test_wms_locations_get_filter_by_parent_location(self):
        stock = self.registry.Wms.PhysObj.query().filter_by(code="WH-KEHL-STOCK").first()
        response = self.webserver.get(
            '/api/v1/wms/physobj/locations?filter[parent_location.id]'
            '[or-ilike]=%s' % stock.id,
            headers=self.headers,
            )
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json_body), 1)
