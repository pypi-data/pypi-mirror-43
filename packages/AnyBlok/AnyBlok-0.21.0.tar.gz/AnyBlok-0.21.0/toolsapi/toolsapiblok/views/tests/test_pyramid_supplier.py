from anyblok_pyramid.tests.testcase import PyramidBlokTestCase


class TestApiv1Supplier(PyramidBlokTestCase):

    def setUp(self):
        super(TestApiv1Supplier, self).setUp()
        self.user = self.registry.User.insert(
            email='t@t', login='test', first_name='test', last_name='test')
        self.registry.User.CredentialStore.insert(
            login='test', password='testpassword')
        resp = self.webserver.post_json(
            '/api/v1/login', {'login': 'test', 'password': 'testpassword'})
        self.headers = {"cookie": resp.headers["Set-Cookie"]}

    def create_supplier(self):
        return self.registry.Supplier.insert(name="great supplier")

    def test_collection_get_must_be_authenticated(self):
        response_protected = self.webserver.get(
            '/api/v1/suppliers',
            status=401
        )
        self.assertIsNone(response_protected.request.authorization)
        self.assertEqual(response_protected.status, '401 Unauthorized')

    def test_get_must_be_authenticated(self):
        supplier = self.create_supplier()
        response_protected = self.webserver.get(
            '/api/v1/supplier/' + str(supplier.uuid),
            status=401
        )
        self.assertIsNone(response_protected.request.authorization)
        self.assertEqual(response_protected.status, '401 Unauthorized')

    def test_collection_get_empty(self):
        response = self.webserver.get(
            '/api/v1/suppliers',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)

    def test_collection_get(self):
        self.create_supplier()
        response = self.webserver.get(
            '/api/v1/suppliers',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)

    def test_get(self):
        supplier = self.create_supplier()
        response = self.webserver.get(
            '/api/v1/supplier/' + str(supplier.uuid),
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
