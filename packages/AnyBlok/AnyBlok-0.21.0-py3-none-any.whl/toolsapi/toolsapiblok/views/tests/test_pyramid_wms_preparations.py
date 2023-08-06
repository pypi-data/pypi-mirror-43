from anyblok_pyramid.tests.testcase import PyramidBlokTestCase


class TestApiv1Preparations(PyramidBlokTestCase):

    def setUp(self):
        super(TestApiv1Preparations, self).setUp()
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

    def test_collection_get_must_be_authenticated(self):
        response_protected = self.webserver.get(
            '/api/v1/wms/preparations',
            status=401
        )
        self.assertIsNone(response_protected.request.authorization)
        self.assertEqual(response_protected.status, '401 Unauthorized')

    def test_collection_get_empty(self):
        response = self.webserver.get(
            '/api/v1/wms/preparations',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)

    def test_collection_get(self):
        self.create_preparation()
        response = self.webserver.get(
            '/api/v1/wms/preparations',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)

    def test_get_preparation_from_barcode_with_code(self):
        preparation = self.create_preparation()
        response = self.webserver.get(
            '/api/v1/wms/preparations/from-barcode',
            params={
                'value': preparation.code
            },
            headers=self.headers,
        )
        self.assertEqual(str(preparation.uuid),
                         response.json_body['uuid'])

    def test_get_preparation_from_barcode_with_odoo_name(self):
        preparation = self.create_preparation()
        preparation_data = preparation.properties['preparation_data']
        response = self.webserver.get(
            '/api/v1/wms/preparations/from-barcode',
            params={
                'value': preparation_data['odoo_name']
            },
            headers=self.headers,
        )
        self.assertEqual(str(preparation.uuid),
                         response.json_body['uuid'])

    def test_get_preparation_from_barcode_with_reason(self):
        preparation = self.create_preparation()
        response = self.webserver.get(
            '/api/v1/wms/preparations/from-barcode',
            params={
                'value': preparation.properties['preparation_data']['reason']
            },
            headers=self.headers,
        )
        self.assertEqual(str(preparation.uuid),
                         response.json_body['uuid'])

    def test_get_preparation_from_barcode_with_preparation_unexisting(self):
        # TODO: to be modified
        pass
        # response = self.webserver.get(
        #     '/api/v1/wms/preparations/from-barcode',
        #     params={
        #         'value': 'PXXXXXXXXXX'
        #     },
        #     headers=self.headers,
        #     status=401
        # )
        # self.assertIsNone(response.request.authorization)
        # self.assertEqual(response.status, '401 Unauthorized')
        # self.assertEqual(response.json_body['errors'][0]['description'],
        #                  'preparation not found')

    def test_next_task_data_for_picking(self):
        # TODO: to be modified
        pass
        # preparation = self.create_preparation()
        # self.assertEqual(preparation.state, 'todo')
        # response = self.webserver.get(
        #     '/api/v1/wms/preparations/next-task-data',
        #     params={
        #         'uuid': str(preparation.uuid)
        #     },
        #     headers=self.headers,
        # )
        # self.assertEqual(str(preparation.uuid),
        #                  response.json_body['uuid'])
        # self.assertTrue('frame_code' in response.json_body.keys())
        # self.assertTrue('right_lens_code' in response.json_body.keys())
        # self.assertTrue('left_lens_code' in response.json_body.keys())
        # self.assertEqual(response.status_code, 200)

    def test_get_next_task_data_with_preparation_unexisting(self):
        # TODO: to be modified
        pass
        # response = self.webserver.get(
        #     '/api/v1/wms/preparations/next-task-data',
        #     params={
        #         'uuid': uuid.uuid4()
        #     },
        #     headers=self.headers,
        #     status=401
        # )
        # self.assertIsNone(response.request.authorization)
        # self.assertEqual(response.status, '401 Unauthorized')
        # self.assertEqual(response.json_body['errors'][0]['description'],
        #                  'preparation not found')

    def test_get_next_task_data_with_preparation_already_picked(self):
        # TODO: to be modified
        pass
        # preparation = self.create_preparation()
        # inputs_ = preparation.properties['bom']['inputs']
        # self.webserver.post_json(
        #     '/api/v1/wms/preparations/validate-products-picking',
        #     params={
        #         'preparation_uuid': str(preparation.uuid),
        #         'frame_code': inputs_['frame_code'],
        #         'right_lens_code': inputs_['right_lens_code'],
        #         'left_lens_code': inputs_['left_lens_code'],
        #         'next_preparation': ''
        #     },
        #     headers=self.headers,
        # )

        # response = self.webserver.get(
        #     '/api/v1/wms/preparations/next-task-data',
        #     params={
        #         'uuid': str(preparation.uuid)
        #     },
        #     headers=self.headers,
        # )
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.json_body, {})

    def assert_picking_operations(self, preparation, posted_references):
        # TODO: to be modified
        pass
        # for key, code in preparation.get_expected_picking_references(
        # ).items():
        #     if key in posted_references.keys(
        # ) and posted_references[key] != '':
        #         op = preparation.get_picking_move(key=key, code=code)
        #         self.assertEqual(op.state, 'done')
        #     else:
        #         op = preparation.get_picking_move(key=key, code=code)
        #         self.assertEqual(op.state, 'planned')

    def test_validate_products_picking_complete(self):
        # TODO: to be modified
        pass
        # preparation = self.create_preparation()
        # inputs_ = preparation.properties['bom']['inputs']
        # params = {
        #     'preparation_uuid': str(preparation.uuid),
        #     'next_preparation': '',
        # }
        # posted_references = {
        #     'frame_code': inputs_['frame_code'],
        #     'right_lens_code': inputs_['right_lens_code'],
        #     'left_lens_code': inputs_['left_lens_code'],
        # }
        # params.update(posted_references)
        # response = self.webserver.post_json(
        #     '/api/v1/wms/preparations/validate-products-picking',
        #     params=params,
        #     headers=self.headers,
        # )
        # self.assert_picking_operations(preparation=preparation,
        #                                posted_references=posted_references)
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(preparation.state, 'assembly_in_progress')

    def test_validate_products_picking_with_partial_frame(self):
        # TODO: to be modified
        pass
        # preparation = self.create_preparation()
        # inputs_ = preparation.properties['bom']['inputs']
        # params = {
        #     'preparation_uuid': str(preparation.uuid),
        #     'next_preparation': preparation.code,
        # }
        # posted_references = {
        #     'frame_code': inputs_['frame_code'],
        #     'right_lens_code': '',
        #     'left_lens_code': '',
        # }
        # params.update(posted_references)
        # response = self.webserver.post_json(
        #     '/api/v1/wms/preparations/validate-products-picking',
        #     params=params,
        #     headers=self.headers,
        # )
        # self.assert_picking_operations(preparation=preparation,
        #                                posted_references=posted_references)
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(preparation.state, 'picking_in_progress')

    def test_validate_products_picking_with_partial_lens(self):
        # TODO: to be modified
        pass
        # preparation = self.create_preparation()
        # inputs_ = preparation.properties['bom']['inputs']
        # params = {
        #     'preparation_uuid': str(preparation.uuid),
        #     'next_preparation': preparation.code,
        # }
        # posted_references = {
        #     'frame_code': '',
        #     'right_lens_code': inputs_['right_lens_code'],
        #     'left_lens_code': '',
        # }
        # params.update(posted_references)
        # response = self.webserver.post_json(
        #     '/api/v1/wms/preparations/validate-products-picking',
        #     params=params,
        #     headers=self.headers,
        # )
        # self.assert_picking_operations(preparation=preparation,
        #                                posted_references=posted_references)
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(preparation.state, 'picking_in_progress')

    def test_validate_products_picking_with_partial_lens_consecutive(self):
        # TODO: to be modified
        pass
        # preparation = self.create_preparation()
        # inputs_ = preparation.properties['bom']['inputs']
        # params = {
        #     'preparation_uuid': str(preparation.uuid),
        #     'next_preparation': preparation.code,
        # }
        # posted_references = {
        #     'frame_code': '',
        #     'right_lens_code': inputs_['right_lens_code'],
        #     'left_lens_code': '',
        # }
        # params.update(posted_references)
        # response = self.webserver.post_json(
        #     '/api/v1/wms/preparations/validate-products-picking',
        #     params=params,
        #     headers=self.headers,
        # )
        # self.assert_picking_operations(preparation=preparation,
        #                                posted_references=posted_references)
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(preparation.state, 'picking_in_progress')
        # response2 = self.webserver.post_json(
        #     '/api/v1/wms/preparations/validate-products-picking',
        #     params=params,
        #     headers=self.headers,
        # )
        # self.assert_picking_operations(preparation=preparation,
        #                                posted_references=posted_references)
        # self.assertEqual(response2.status_code, 200)
        # self.assertEqual(preparation.state, 'picking_in_progress')
