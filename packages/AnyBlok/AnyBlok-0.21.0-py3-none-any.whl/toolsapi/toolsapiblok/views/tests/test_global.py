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

    def test_get_global(self):
        """Wms.Location GET /api/v1/wms/locations?limit=10"""
        response = self.webserver.get(
            '/api/v1/init/global',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
