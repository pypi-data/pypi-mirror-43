from datetime import datetime
from anyblok_pyramid.tests.testcase import PyramidBlokTestCase


class TestApiWmsOperationsBase(PyramidBlokTestCase):
    """ Wms.PhysObjType test class throught rest api
    """

    def setUp(self):
        super(TestApiWmsOperationsBase, self).setUp()
        self.user = self.registry.User.insert(
            email='t@t', login='test', first_name='test', last_name='test')
        self.registry.User.CredentialStore.insert(
            login='test', password='testpassword')
        resp = self.webserver.post_json(
            '/api/v1/login', {'login': 'test', 'password': 'testpassword'})
        self.headers = {"cookie": resp.headers["Set-Cookie"]}

    def test_wms_operations_ensure_protected_view(self):
        response_protected = self.webserver.get(
            '/api/v1/wms/operations?limit=10',
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

    def test_wms_operations_get(self):
        """Wms.PhysObjType GET /api/v1/wms/operations?limit=10"""
        response = self.webserver.get(
            '/api/v1/wms/operations?limit=10',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        op_query = self.registry.Wms.Operation.query().limit(10)
        self.assertEqual(len(response.json_body), op_query.count())

    def test_wms_operations_get_done(self):
        """
        Wms.PhysObjType GET/api/v1/wms/operations?filter[state]=done&limit=10
        """
        response = self.webserver.get(
            '/api/v1/wms/operations?filter[state][like]=done&limit=10',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        op_query = self.registry.Wms.Operation.query().filter_by(
            state='done').limit(10)
        self.assertEqual(len(response.json_body), op_query.count())

    def test_wms_operations_moves_get(self):
        """Wms.PhysObjType GET /api/v1/wms/operations/moves?limit=10"""
        response = self.webserver.get(
            '/api/v1/wms/operations?limit=10',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        op_query = self.registry.Wms.Operation.query().limit(10)
        self.assertEqual(len(response.json_body), op_query.count())

    def create_move_operation(self, state='planned', avatar=None):
        Move = self.registry.Wms.Operation.Move
        PhysObj = self.registry.Wms.PhysObj
        dest = PhysObj.query().join(PhysObj.type).filter(
            PhysObj.Type.query_is_a_container()).first()
        if avatar is None:
            avatar = PhysObj.Avatar.query().filter_by(state='present').first()
        self.op = Move.create(state=state,
                              input=avatar,
                              destination=dest,
                              dt_execution=datetime.now())

    def create_arrival_of_storable(self):
        PhysObj = self.registry.Wms.PhysObj
        Operation = self.registry.Wms.Operation
        gt = PhysObj.Type.query().filter(
            PhysObj.Type.query_is_storable()).first()
        op = Operation.Arrival.create(
          goods_type=gt,
          location=gt.get_default_storage_location(),
          dt_execution=datetime.now(),
          state='done'
        )
        return op.outcomes[0]

    def create_arrival_of_container(self):
        PhysObj = self.registry.Wms.PhysObj
        Operation = self.registry.Wms.Operation
        gt = PhysObj.Type.query().filter(
            PhysObj.Type.query_is_a_container()).first()
        op = Operation.Arrival.create(
            goods_type=gt,
            location=gt.get_default_storage_location(),
            dt_execution=datetime.now(),
            state='done'
        )
        return op.outcomes[0]

    def test_wms_operations_moves_tag_object_is_storable(self):
        av = self.create_arrival_of_storable()
        self.create_move_operation(avatar=av)
        response = self.webserver.get(
            '/api/v1/wms/operations/moves?tag=object-is-storable&limit=10',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json_body), 1)

    def test_wms_operations_moves_tag_object_is_a_container(self):
        av = self.create_arrival_of_container()
        self.create_move_operation(avatar=av)
        response = self.webserver.get(
            '/api/v1/wms/operations/moves?tag=object-is-a-container&limit=10',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json_body), 1)

    def test_wms_operations_moves_tag_operation_is_executable(self):
        av = self.create_arrival_of_storable()
        self.create_move_operation(avatar=av)
        response = self.webserver.get(
            '/api/v1/wms/operations/moves?tag=operation-is-executable&limit=10',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json_body), 1)

    def test_wms_operations_moves_tag_obj_is_storable_and_op_executable(self):
        av = self.create_arrival_of_storable()
        self.create_move_operation(avatar=av)
        response = self.webserver.get(
            '/api/v1/wms/operations/moves?tag=object-is-storable'
            '&tag=operation-is-executable&limit=10',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json_body), 1)

    def test_wms_operations_moves_filter_by_location(self):
        av = self.create_arrival_of_storable()
        self.create_move_operation(avatar=av)
        response = self.webserver.get(
            '/api/v1/wms/operations/moves?filter[input.location.code]'
            '[or-ilike]=%s' % av.location.code,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json_body), 1)

    # TODO: Can't apply two filters/tags using the same join, aliases
    # def test_wms_operations_moves_tag_op_executable_filter_by_location(self):
    #     av = self.create_arrival_of_storable()
    #     self.create_move_operation(avatar=av)
    #     response = self.webserver.get(
    #         '/api/v1/wms/operations/moves?tag=operation-is-executable&filter[input.location.code]'
    #         '[or-ilike]=%s' % av.location.code,
    #         headers=self.headers,
    #         )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(len(response.json_body), 1)

    def test_wms_operations_moves_filter_by_input_type(self):
        av = self.create_arrival_of_storable()
        self.create_move_operation(avatar=av)
        response = self.webserver.get(
            '/api/v1/wms/operations/moves?filter[input.type.code]'
            '[or-ilike]=%s' % av.obj.type.code,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json_body), 1)

    def test_wms_operations_moves_filter_by_destination(self):
        av = self.create_arrival_of_storable()
        self.create_move_operation(avatar=av)
        response = self.webserver.get(
            '/api/v1/wms/operations/moves?filter[destination.code]'
            '[or-ilike]=%s' % self.op.destination.code,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json_body), 1)

    def test_wms_operations_moves_execute_operations(self):
        self.create_move_operation()
        response = self.webserver.post_json(
            '/api/v1/wms/operations/execute/',
            params={
                'operation_ids': [self.op.id],
            },
            headers=self.headers,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.op.state, 'done')

    def test_wms_operations_moves_cancel_operation(self):
        self.create_move_operation()
        response = self.webserver.post_json(
            '/api/v1/wms/operations/cancel/',
            params={
                'operation_ids': [self.op.id],
            },
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.op.outcomes, [])

    def test_wms_operations_moves_revert_operation(self):
        self.create_move_operation(state='done')
        response = self.webserver.post_json(
            '/api/v1/wms/operations/revert/',
            params={
                'operation_ids': [self.op.id],
            },
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        reverse_op = response.json_body[0]
        reverse_op_id = reverse_op['id']
        self.assertNotEqual(reverse_op_id, self.op.id)
        Move = self.registry.Wms.Operation.Move
        reverse_op = Move.query().get(reverse_op_id)
        self.assertEqual(reverse_op.state, 'planned')
        self.assertEqual(self.op.destination, reverse_op.input.location)
        self.assertEqual(self.op.input.location, reverse_op.destination)

    def test_wms_operations_moves_obliviate_operation(self):
        self.create_move_operation(state='done')
        response = self.webserver.post_json(
            '/api/v1/wms/operations/obliviate/',
            params={
                'operation_ids': [self.op.id],
            },
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.op.outcomes, [])

    def test_wms_operations_moves_alter_destination(self):
        Operation = self.registry.Wms.Operation
        PhysObj = self.registry.Wms.PhysObj
        locations = PhysObj.query().join(PhysObj.type).filter(
            PhysObj.Type.query_is_a_container()).limit(2).all()
        dest1 = locations[0]
        dest2 = locations[1]
        gt = PhysObj.Type.query().filter(
            PhysObj.Type.query_is_storable()).first()
        op = Operation.Arrival.create(
                 goods_type=gt,
                 location=gt.get_default_storage_location(),
                 dt_execution=datetime.now(),
                 state='planned'
             )
        av = op.outcomes[0]
        op = Operation.Move.create(state='planned',
                                   input=av,
                                   destination=dest1,
                                   dt_execution=datetime.now())
        response = self.webserver.patch(
            '/api/v1/wms/operations/moves/%s/alter-destination' % op.id,
            params={
                'destination_id': dest2.id
            },
            headers=self.headers,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json_body['id'], dest2.id)
        self.assertEqual(op.destination, dest2)
        self.assertEqual(op.outcomes[0].location, dest2)
