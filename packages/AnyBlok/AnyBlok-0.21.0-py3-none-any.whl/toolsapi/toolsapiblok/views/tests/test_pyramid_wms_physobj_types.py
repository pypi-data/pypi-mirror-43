from anyblok_pyramid.tests.testcase import PyramidBlokTestCase


class TestApiWmsPhysObjTypesBase(PyramidBlokTestCase):
    """ Wms.PhysObjType test class throught rest api
    """

    def setUp(self):
        super(TestApiWmsPhysObjTypesBase, self).setUp()
        self.user = self.registry.User.insert(
            email='t@t', login='test', first_name='test', last_name='test')
        self.registry.User.CredentialStore.insert(
            login='test', password='testpassword')
        resp = self.webserver.post_json(
            '/api/v1/login', {'login': 'test', 'password': 'testpassword'})
        self.headers = {"cookie": resp.headers["Set-Cookie"]}

    def test_wms_physobj_types_ensure_protected_view(self):
        response_protected = self.webserver.get(
            '/api/v1/wms/physobj/types?limit=10',
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

    def test_wms_physobj_types_get(self):
        """Wms.PhysObjType GET /api/v1/wms/physobj/types?limit=10"""
        response = self.webserver.get(
            '/api/v1/wms/physobj/types?limit=10',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json_body), 10)

    def test_wms_physobj_types_get_frames(self):
        """Wms.PhysObjType GET /api/v1/wms/physobj/types"""
        response = self.webserver.get(
            '/api/v1/wms/physobj/types?filter[parent.code][like]=FRAME',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        parent_gt = self.registry.Wms.PhysObj.Type.query().filter_by(
            code='FRAME').one()
        children_count = self.registry.Wms.PhysObj.Type.query().filter_by(
            parent=parent_gt).count()
        self.assertEqual(len(response.json_body),
                         children_count)

    def test_wms_physobj_types_get_filter_by_code(self):
        PhysObjType = self.registry.Wms.PhysObj.Type
        lens = PhysObjType.query().filter_by(code="SDG-ORGA-150-004-RX-S").one()
        response = self.webserver.get(
            '/api/v1/wms/physobj/types?filter[code][eq]=%s' % lens.code,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json_body[0]['code'], lens.code)

    def test_wms_physobj_types_get_filter_by_supplier_code(self):
        PhysObjType = self.registry.Wms.PhysObj.Type
        lens = PhysObjType.query().filter_by(code="SDG-ORGA-150-004-RX-S").one()
        mapping = self.registry.Supplier.PhysObjMapping.query().filter_by(physobj_type=lens).first()
        response = self.webserver.get(
            '/api/v1/wms/physobj/types?filter[code][eq]=%s'
            % mapping.code,
            headers=self.headers,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json_body[0]['code'], lens.code)

    def test_wms_physobj_types_get_tag_is_frame(self):
        response = self.webserver.get(
            '/api/v1/wms/physobj/types?tag=parent is frame&limit=10',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        parent_gt = self.registry.Wms.PhysObj.Type.query().filter_by(
            code='FRAME').one()
        children_count = self.registry.Wms.PhysObj.Type.query().filter_by(
            parent=parent_gt).limit(10).count()
        self.assertEqual(len(response.json_body),
                         children_count)

    def test_wms_physobj_types_get_tag_is_lens(self):
        response = self.webserver.get(
            '/api/v1/wms/physobj/types?tag=parent is lens&limit=10',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        parent_gt = self.registry.Wms.PhysObj.Type.query().filter_by(
            code='LENS').one()
        children_count = self.registry.Wms.PhysObj.Type.query().filter_by(
            parent=parent_gt).limit(10).count()
        self.assertEqual(len(response.json_body),
                         children_count)

    def test_wms_physobj_types_get_tag_is_np_eyewear(self):
        response = self.webserver.get(
            '/api/v1/wms/physobj/types?tag=parent is np eyewear&limit=10',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        parent_gt = self.registry.Wms.PhysObj.Type.query().filter_by(
            code='NP_EYEWEAR').one()
        children_count = self.registry.Wms.PhysObj.Type.query().filter_by(
            parent=parent_gt).limit(10).count()
        self.assertEqual(len(response.json_body),
                         children_count)
