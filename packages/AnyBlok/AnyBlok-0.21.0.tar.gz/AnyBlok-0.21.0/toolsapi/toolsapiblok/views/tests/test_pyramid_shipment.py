from anyblok_pyramid.tests.testcase import PyramidBlokTestCase


class TestApiv1Shipment(PyramidBlokTestCase):

    def setUp(self):
        super(TestApiv1Shipment, self).setUp()
        self.user = self.registry.User.insert(
            email='t@t', login='test', first_name='test', last_name='test')
        self.registry.User.CredentialStore.insert(
            login='test', password='testpassword')
        resp = self.webserver.post_json(
            '/api/v1/login', {'login': 'test', 'password': 'testpassword'})
        self.headers = {"cookie": resp.headers["Set-Cookie"]}

    def create_shipment(self):
        doc = self.registry.Attachment.Document.insert()
        address = self.registry.Address.insert(
            first_name="Shipping",
            last_name="services",
            street1="1 company street",
            zip_code="75000",
            city="Paris",
            country="FRA")
        ca = self.registry.Delivery.Carrier.insert(
            name="ColissimoTest", code="COLISSIMOTEST")
        ca_cred = self.registry.Delivery.Carrier.Credential.insert(
                    account_number="123",
                    password="password")
        service = self.registry.Delivery.Carrier.Service.Colissimo.insert(
                    name="Livraison à domicile", product_code="TEST",
                    carrier=ca, credential=ca_cred)
        ship = self.registry.Delivery.Shipment.insert(
            service=service,
            sender_address=address,
            recipient_address=address,
            reason="Test",
            pack="Test",
            document_uuid=doc.uuid,
            tracking_number="test")
        self.registry.flush()
        ship.expire()
        return ship

    def test_collection_get_must_be_authenticated(self):
        response_protected = self.webserver.get(
            '/api/v1/shipments',
            status=401
        )
        self.assertIsNone(response_protected.request.authorization)
        self.assertEqual(response_protected.status, '401 Unauthorized')

    def test_get_must_be_authenticated(self):
        ship = self.create_shipment()
        response_protected = self.webserver.get(
            '/api/v1/shipment/' + str(ship.uuid),
            status=401
        )
        self.assertIsNone(response_protected.request.authorization)
        self.assertEqual(response_protected.status, '401 Unauthorized')

    def test_collection_get_empty(self):
        response = self.webserver.get(
            '/api/v1/shipments',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)

    def test_collection_get(self):
        self.create_shipment()
        response = self.webserver.get(
            '/api/v1/shipments',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)

    def test_get(self):
        ship = self.create_shipment()
        response = self.webserver.get(
            '/api/v1/shipment/' + str(ship.uuid),
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
