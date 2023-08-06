from anyblok_pyramid.tests.testcase import PyramidBlokTestCase


class TestApiv1Packing(PyramidBlokTestCase):

    def setUp(self):
        super(TestApiv1Packing, self).setUp()
        self.user = self.registry.User.insert(
            email='t@t', login='test', first_name='test', last_name='test')
        self.registry.User.CredentialStore.insert(
            login='test', password='testpassword')
        resp = self.webserver.post_json(
            '/api/v1/login', {'login': 'test', 'password': 'testpassword'})
        self.headers = {"cookie": resp.headers["Set-Cookie"]}

    def create_packing(self):
        doc = self.registry.Attachment.Document.insert()
        printer = self.registry.Device.PrinterCups.insert()
        pack = self.registry.Packing.Document.insert(
            reason="Test",
            pack="Test")
        pack.invoices.append(self.registry.Packing.Document.Line.insert(
            printer=printer,
            latest_document_uuid=doc.uuid))
        pack.cerfas.append(self.registry.Packing.Document.Line.insert(
            printer=printer,
            latest_document_uuid=doc.uuid))
        pack.prescriptions.append(self.registry.Packing.Document.Line.insert(
            printer=printer,
            latest_document_uuid=doc.uuid))
        return pack

    def test_collection_get_must_be_authenticated(self):
        response_protected = self.webserver.get(
            '/api/v1/packing/documents',
            status=401
        )
        self.assertIsNone(response_protected.request.authorization)
        self.assertEqual(response_protected.status, '401 Unauthorized')

    def test_get_must_be_authenticated(self):
        pack = self.create_packing()
        response_protected = self.webserver.get(
            '/api/v1/packing/documents/' + str(pack.uuid),
            status=401
        )
        self.assertIsNone(response_protected.request.authorization)
        self.assertEqual(response_protected.status, '401 Unauthorized')

    def test_collection_get_empty(self):
        response = self.webserver.get(
            '/api/v1/packing/documents',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)

    def test_collection_get(self):
        self.create_packing()
        response = self.webserver.get(
            '/api/v1/packing/documents',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)

    def test_get(self):
        pack = self.create_packing()
        response = self.webserver.get(
            '/api/v1/packing/documents/' + str(pack.uuid),
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
