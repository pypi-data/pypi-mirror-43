from anyblok_pyramid.tests.testcase import PyramidBlokTestCase
import csv


class TestApiv1WmsStock(PyramidBlokTestCase):

    def setUp(self):
        super(TestApiv1WmsStock, self).setUp()
        self.user = self.registry.User.insert(
            email='t@t', login='test', first_name='test', last_name='test')
        self.registry.User.CredentialStore.insert(
            login='test', password='testpassword')
        resp = self.webserver.post_json(
            '/api/v1/login', {'login': 'test', 'password': 'testpassword'})
        self.headers = {"cookie": resp.headers["Set-Cookie"]}
        self.physobj_type_code = "AE01-ECAILLE-32"
        self.location_code = "WH-KEHL_D_01_01_03"

    def create_goods(self):
        Wms = self.registry.Wms
        Operation = Wms.Operation
        PhysObj = Wms.PhysObj
        gt = PhysObj.Type.query().filter_by(code=self.physobj_type_code).one()
        location = PhysObj.query().filter_by(code=self.location_code).one()
        Operation.Apparition.create(physobj_type=gt, location=location, quantity=3, state='done')

    def test_collection_get_must_be_authenticated(self):
        response_protected = self.webserver.get(
            '/api/v1/wms/stock/locations',
            status=401
        )
        self.assertIsNone(response_protected.request.authorization)
        self.assertEqual(response_protected.status, '401 Unauthorized')

    def test_collection_get_empty(self):
        response = self.webserver.get(
            '/api/v1/wms/stock/locations',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)

    def test_collection_get(self):
        self.create_goods()
        response = self.webserver.get(
            '/api/v1/wms/stock/locations',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json_body), 1)
        stock_line = response.json_body[0]
        self.assertEqual(stock_line['physobj_type']['code'], self.physobj_type_code)
        self.assertEqual(stock_line['location']['code'], self.location_code)
        self.assertEqual(stock_line['quantity'], 3)

    def test_collection_get_csv_must_be_authenticated(self):
        response_protected = self.webserver.post(
            '/api/v1/wms/stock/locations/execute/get_csv',
            status=401
        )
        self.assertIsNone(response_protected.request.authorization)
        self.assertEqual(response_protected.status, '401 Unauthorized')

    def test_collection_get_csv_empty(self):
        response = self.webserver.post(
            '/api/v1/wms/stock/locations/execute/get_csv',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)

    def test_collection_get_csv(self):
        self.create_goods()
        PhysObj = self.registry.Wms.PhysObj
        gt = PhysObj.Type.query().filter_by(code=self.physobj_type_code).one()
        gt.properties['product_category'] = 'Monture'
        gt.properties['cost_price'] = 23.68
        response = self.webserver.post(
            '/api/v1/wms/stock/locations/execute/get_csv',
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        dialect = csv.Sniffer().sniff(response.body.decode())
        lines = response.body.decode().split('\n')
        reader = csv.DictReader(lines, dialect=dialect, delimiter=';')
        row = next(reader)
        quantity = int(row.get('quantity'))
        location_code = row.get('location')
        physobj_type_code = row.get('sku')
        valo = float(row.get('valo'))
        self.assertEqual(quantity, 3)
        self.assertEqual(location_code, self.location_code)
        self.assertEqual(physobj_type_code, self.physobj_type_code)
        self.assertEqual(valo, round(quantity * gt.properties['cost_price'], 2))
