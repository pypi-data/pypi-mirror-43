from datetime import datetime
from anyblok_pyramid.tests.testcase import PyramidBlokTestCase
from sqlalchemy.orm.exc import ObjectDeletedError


class TestApiv1WmsInventoryNodes(PyramidBlokTestCase):

    def setUp(self):
        super(TestApiv1WmsInventoryNodes, self).setUp()
        Wms = self.registry.Wms
        self.Inventory = Wms.Inventory
        self.PhysObj = Wms.PhysObj
        self.user = self.registry.User.insert(
            email='t@t', login='test', first_name='test', last_name='test')
        self.registry.User.CredentialStore.insert(
            login='test', password='testpassword')
        resp = self.webserver.post_json(
            '/api/v1/login', {'login': 'test', 'password': 'testpassword'})
        self.headers = {"cookie": resp.headers["Set-Cookie"]}

        self.root_location = self.registry.Wms.PhysObj.query().filter_by(code="WH-KEHL-STOCK").one()
        self.reason = 'Inventory 1'
        self.creator = self.user
        self.inventory_date = datetime.strptime("01/01/2019", "%d/%m/%Y")
        self.node_location = self.PhysObj.query().filter_by(code="WH-KEHL_A_01_02_03").one()
        self.node_physobj_type = self.PhysObj.Type.query().filter_by(code="MF02-BRUN-11").one()

    def create_inventory(self):
        inventory = self.Inventory.create(self.root_location, **{
                                              'reason': self.reason,
                                              'creator': self.creator,
                                              'date': self.inventory_date
                                          })
        return inventory

    def test_collection_get_must_be_authenticated(self):
        response_protected = self.webserver.get(
            '/api/v1/wms/inventories/nodes',
            status=401
        )
        self.assertIsNone(response_protected.request.authorization)
        self.assertEqual(response_protected.status, '401 Unauthorized')

    def test_get_must_be_authenticated(self):
        inventory = self.create_inventory()
        response_protected = self.webserver.get(
            '/api/v1/wms/inventories/nodes/' + str(inventory.root.id),
            status=401
        )
        self.assertIsNone(response_protected.request.authorization)
        self.assertEqual(response_protected.status, '401 Unauthorized')

    def test_collection_get_empty(self):
        response = self.webserver.get(
            '/api/v1/wms/inventories/nodes',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)

    def test_collection_get(self):
        self.create_inventory()
        response = self.webserver.get(
            '/api/v1/wms/inventories/nodes',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)

    def test_get(self):
        inventory = self.create_inventory()
        response = self.webserver.get(
            '/api/v1/wms/inventories/nodes/' + str(inventory.root.id),
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)

    def test_add_lines_all_ok(self):
        inventory = self.create_inventory()

        response = self.webserver.patch_json(
            '/api/v1/wms/inventories/nodes/' + str(inventory.root.id),
            headers=self.headers,
            params={
                'lines': [
                    {'location': {'id': self.node_location.id},
                     'physobj_type': {'id': self.node_physobj_type.id},
                     'quantity_observed': 5}
                ],
            },
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.Inventory.Line.query().count(),
                         1)

    def test_add_lines_already_exists(self):
        inventory = self.create_inventory()

        line = self.Inventory.Line.insert(node=inventory.root,
                                          location=self.node_location,
                                          type=self.node_physobj_type,
                                          quantity=3)

        self.assertEqual(line.quantity, 3)
        response = self.webserver.patch_json(
            '/api/v1/wms/inventories/nodes/' + str(inventory.root.id),
            headers=self.headers,
            params={
                'lines': [
                    {'location': {'id': self.node_location.id},
                     'physobj_type': {'id': self.node_physobj_type.id},
                     'quantity_observed': 5}
                ],
            },
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(line.quantity, 5)

    def test_add_lines_missing_location(self):
        inventory = self.create_inventory()

        with self.assertRaises(ObjectDeletedError):
            response = self.webserver.patch_json(
                '/api/v1/wms/inventories/nodes/' + str(inventory.root.id),
                headers=self.headers,
                params={
                    'lines': [
                        {'location': {'id': 0},
                         'physobj_type': {'id': self.node_physobj_type.id},
                         'quantity_observed': 5},
                    ],
                },
                status=200,
                )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(self.Inventory.Line.query().count(),
                             0)

    def test_add_lines_missing_physobj_type(self):
        inventory = self.create_inventory()

        with self.assertRaises(ObjectDeletedError):
            response = self.webserver.patch_json(
                '/api/v1/wms/inventories/nodes/' + str(inventory.root.id),
                headers=self.headers,
                params={
                    'lines': [
                        {'location': {'id': self.node_location.id},
                         'physobj_type': {'id': 0},
                         'quantity_observed': 5}
                    ],
                },
                status=200,
                )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(self.Inventory.Line.query().count(),
                             0)

    def test_update_state(self):
        inventory = self.create_inventory()

        response = self.webserver.post_json(
            '/api/v1/wms/inventories/nodes/execute/update-state',
            headers=self.headers,
            params={
                'node_ids': [str(inventory.root.id)],
                'state': 'full'
            },
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(inventory.root.state,
                         'full')

    def test_compute_actions(self):
        inventory = self.create_inventory()

        inventory.root.state = 'full'
        response = self.webserver.post_json(
            '/api/v1/wms/inventories/nodes/execute/compute-actions',
            headers=self.headers,
            params={
                'node_ids': [str(inventory.root.id)],
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(inventory.root.state,
                         'computed')

    def test_compute_actions_recompute(self):
        inventory = self.create_inventory()

        inventory.root.state = 'computed'
        response = self.webserver.post_json(
            '/api/v1/wms/inventories/nodes/execute/compute-actions',
            headers=self.headers,
            params={
                'node_ids': [str(inventory.root.id)],
                'recompute': "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(inventory.root.state,
                         'computed')

    def test_compute_push_actions(self):
        inventory = self.create_inventory()

        inventory.root.state = 'full'
        response = self.webserver.post_json(
            '/api/v1/wms/inventories/nodes/execute/compute-push-actions',
            headers=self.headers,
            params={
                'node_ids': [str(inventory.root.id)],
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(inventory.root.state,
                         'pushed')

    def test_recurse_compute_push_actions(self):
        inventory = self.create_inventory()

        inventory.root.state = 'full'
        response = self.webserver.post_json(
            '/api/v1/wms/inventories/nodes/execute/recurse-compute-push-actions',
            headers=self.headers,
            params={
                'node_ids': [str(inventory.root.id)],
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(inventory.root.state,
                         'pushed')
