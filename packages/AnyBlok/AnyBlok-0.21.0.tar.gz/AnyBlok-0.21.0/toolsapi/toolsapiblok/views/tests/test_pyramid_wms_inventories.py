from datetime import datetime
from anyblok_pyramid.tests.testcase import PyramidBlokTestCase


class TestApiv1WmsInventories(PyramidBlokTestCase):

    def setUp(self):
        super(TestApiv1WmsInventories, self).setUp()
        self.Inventory = self.registry.Wms.Inventory
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

    def create_inventory(self):
        inventory = self.Inventory.create(location=self.root_location, **{
                                              'reason': self.reason,
                                              'creator': self.creator,
                                              'date': self.inventory_date,
                                              'considered_types': ['IAH01-NOIR-12']
                                          })
        return inventory

    def test_collection_get_must_be_authenticated(self):
        response_protected = self.webserver.get(
            '/api/v1/wms/inventories',
            status=401
        )
        self.assertIsNone(response_protected.request.authorization)
        self.assertEqual(response_protected.status, '401 Unauthorized')

    def test_get_must_be_authenticated(self):
        inventory = self.create_inventory()
        response_protected = self.webserver.get(
            '/api/v1/wms/inventories/' + str(inventory.id),
            status=401
        )
        self.assertIsNone(response_protected.request.authorization)
        self.assertEqual(response_protected.status, '401 Unauthorized')

    def test_collection_get_empty(self):
        response = self.webserver.get(
            '/api/v1/wms/inventories',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)

    def test_collection_get(self):
        self.create_inventory()
        response = self.webserver.get(
            '/api/v1/wms/inventories',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)

    def test_get(self):
        inventory = self.create_inventory()
        response = self.webserver.get(
            '/api/v1/wms/inventories/' + str(inventory.id),
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        response = self.webserver.post_json(
            '/api/v1/wms/inventories',
            [{
                'root_location': {'id': self.root_location.id},
                'reason': self.reason,
                'creator': {'login': self.creator.login},
                'date': str(self.inventory_date)
            }],
            headers=self.headers,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.Inventory.query().count(), 1)

    def test_create_with_considered_types(self):
        response = self.webserver.post_json(
            '/api/v1/wms/inventories',
            [{
                'root_location': {'id': self.root_location.id},
                'reason': self.reason,
                'creator': {'login': self.creator.login},
                'date': str(self.inventory_date),
                'considered_types': ['IAH01-NOIR-12']
            }],
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.Inventory.query().count(), 1)

    def test_reconcile_all(self):
        inventory = self.create_inventory()

        inventory.root.state = 'full'
        inventory.root.compute_push_actions()
        response = self.webserver.post_json(
            '/api/v1/wms/inventories/execute/reconcile-all',
            headers=self.headers,
            params={
                'inventory_ids': [str(inventory.id)],
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(inventory.root.state,
                         'reconciled')

    def test_split_leafs(self):
        inventory = self.create_inventory()

        root_node = inventory.root
        self.assertTrue(root_node.is_leaf)
        root_node.split()
        self.assertFalse(root_node.is_leaf)
        response = self.webserver.post_json(
            '/api/v1/wms/inventories/execute/split-leafs',
            headers=self.headers,
            params={
                'inventory_ids': [str(inventory.id)],
            },
        )
        self.assertEqual(response.status_code, 200)
        Wms = self.registry.Wms
        Node = Wms.Inventory.Node
        PhysObj = Wms.PhysObj
        location = PhysObj.query().filter_by(code='WH-KEHL_A').first()
        child_node = Node.query().filter_by(parent=root_node,
                                            location=location).first()
        self.assertFalse(child_node.is_leaf)
