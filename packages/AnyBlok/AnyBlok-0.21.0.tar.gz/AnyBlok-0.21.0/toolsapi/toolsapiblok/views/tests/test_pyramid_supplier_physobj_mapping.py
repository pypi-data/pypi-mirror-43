from anyblok_pyramid.tests.testcase import PyramidBlokTestCase


class TestApiv1SupplierPhysObjMapping(PyramidBlokTestCase):

    def setUp(self):
        super(TestApiv1SupplierPhysObjMapping, self).setUp()
        self.user = self.registry.User.insert(
            email='t@t', login='test', first_name='test', last_name='test')
        self.registry.User.CredentialStore.insert(
            login='test', password='testpassword')
        resp = self.webserver.post_json(
            '/api/v1/login', {'login': 'test', 'password': 'testpassword'})
        self.headers = {"cookie": resp.headers["Set-Cookie"]}

    def get_mapping(self):
        physobj_type = self.registry.Wms.PhysObj.Type.query().filter_by(code="SENGC-001").first()
        return self.registry.Supplier.PhysObjMapping.query().filter_by(
            physobj_type=physobj_type).first()

    def test_collection_get_must_be_authenticated(self):
        response_protected = self.webserver.get(
            '/api/v1/suppliers/physobj-mapping',
            status=401
        )
        self.assertIsNone(response_protected.request.authorization)
        self.assertEqual(response_protected.status, '401 Unauthorized')

    def test_get_must_be_authenticated(self):
        mapping = self.get_mapping()
        response_protected = self.webserver.get(
            '/api/v1/suppliers/' + str(mapping.supplier.uuid) +
            '/physobj-mapping/' + str(mapping.code),
            status=401
        )
        self.assertIsNone(response_protected.request.authorization)
        self.assertEqual(response_protected.status, '401 Unauthorized')

    def test_collection_get(self):
        self.get_mapping()
        response = self.webserver.get(
            '/api/v1/suppliers/physobj-mapping?limit=10',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)

    def test_collection_get_filter_code(self):
        mapping = self.get_mapping()
        response = self.webserver.get(
            '/api/v1/suppliers/physobj-mapping?filter[code][or-ilike]=%s&limit=10' % mapping.code,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json_body), 1)
        self.assertEqual(response.json_body[0]['code'], mapping.code)

    def test_collection_get_filter_physobj_type_code(self):
        mapping = self.get_mapping()
        response = self.webserver.get(
            '/api/v1/suppliers/physobj-mapping?filter[physobj_type.code][or-ilike]=%s&limit=10'
            % mapping.physobj_type.code,
            headers=self.headers,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json_body), 1)
        self.assertEqual(response.json_body[0]['code'], mapping.code)

    def test_collection_get_filter_supplier_name(self):
        mapping = self.get_mapping()
        response = self.webserver.get(
            '/api/v1/suppliers/physobj-mapping?filter[supplier.name][or-ilike]=%s&limit=10'
            % mapping.supplier.name,
            headers=self.headers,
            )
        results_expected = self.registry.Supplier.PhysObjMapping.query().filter_by(
            supplier=mapping.supplier).count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json_body), results_expected)

    # def test_get(self):
    #     mapping = self.get_mapping()
    #     response = self.webserver.get(
    #         '/api/v1/suppliers/' + str(mapping.supplier.uuid) +
    #         '/physobj-mapping/' + str(mapping.code),
    #         headers=self.headers,
    #     )
    #     self.assertEqual(response.status_code, 200)
