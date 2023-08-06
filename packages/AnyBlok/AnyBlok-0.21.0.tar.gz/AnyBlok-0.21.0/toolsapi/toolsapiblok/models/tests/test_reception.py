from anyblok.tests.testcase import BlokTestCase
from anyblok_pyramid.tests.testcase import PyramidBlokTestCase
from uuid import uuid1
from json import dumps
from unittest.mock import patch
from unittest import skip


class TestReception(BlokTestCase):
    """ Test Sensee wms"""

    def setUp(self):
        super(TestReception, self).setUp()
        self.Type = self.registry.Wms.PhysObj.Type
        self.Location = self.registry.Wms.Location
        self.Reception = self.registry.Reception

    def assertOperationStatus(self, reception, status):
        for line in reception.lines:
            if not line.operations:
                self.fail('No operation found')

            for op in line.operations:
                self.assertEqual(op.state, status)

    @skip('Waiting fix on anyblok bus')
    def test_create_reception_by_bus(self):
        uuid = uuid1()
        physobj_type = self.registry.Wms.PhysObj.Type.query().filter_by(
            code="IAH01-NOIR-12").one()
        location = self.registry.Wms.Location.query().limit(1).one()
        message = dict(
            uuid=str(uuid),
            recipient_address=dict(
                first_name="Jon",
                last_name="Doe",
                street1="1 street",
                street2="crossroad",
                street3="♥",
                zip_code="66000",
                state="A region",
                city="Perpignan",
                country="FRA",
                phone1="0977552210",
            ),
            sender_address=dict(
                first_name="Shipping",
                last_name="services",
                company_name="Acme",
                street1="1 company street",
                zip_code="75000",
                state="",
                city="Paris",
                country="FRA",
            ),
            pack='Pack',
            reason="SO",
            tracking_number="8R00000",
            lines=[dict(
                location_code=location.code,
                physobj_type=physobj_type.code,
                expected_quantity=2,
            )])
        self.Reception.create_planned_reception(body=dumps(message))
        reception = self.Reception.query().get(uuid)
        self.assertIsNotNone(reception)
        self.assertEqual(len(reception.lines), 1)
        self.assertEqual(len(reception.lines[0].operations), 2)
        self.assertOperationStatus(reception, 'planned')

    def create_sender_address(self):
        return self.registry.Address.insert(
            first_name="Shipping",
            last_name="services",
            company_name="Acme",
            street1="1 company street",
            zip_code="75000",
            state="",
            city="Paris",
            country="FRA",
        )

    def create_recipient_address(self):
        return self.registry.Address.insert(
            first_name="Jon",
            last_name="Doe",
            street1="1 street",
            street2="crossroad",
            street3="♥",
            zip_code="66000",
            state="A region",
            city="Perpignan",
            country="FRA",
            phone1="0977552210",
        )

    def create_reception(self, operations=None, expected_quantity=None, quantity=None,
                         location_code=None):
        goods_type = self.registry.Wms.PhysObj.Type.query().filter_by(
            code="IAH01-NOIR-12").one()
        sender_address = self.create_sender_address()
        recipient_address = self.create_recipient_address()
        return self.Reception.create(
            dict(sender_address=sender_address, recipient_address=recipient_address,
                 pack='Test', reason='Test', tracking_number='test'),
            lines=[dict(
                physobj_type=goods_type,
                expected_quantity=expected_quantity,
                quantity=quantity,
                location_code=location_code,
            )])

    def test_create_reception(self):
        reception = self.create_reception()
        self.assertEqual(len(reception.lines), 1)
        self.assertEqual(len(reception.lines[0].operations), 0)

    def test_create_reception_with_expected(self):
        reception = self.create_reception(expected_quantity=2)
        self.assertEqual(len(reception.lines), 1)
        self.assertEqual(len(reception.lines[0].operations), 2)
        self.assertOperationStatus(reception, 'planned')

    def test_create_planned_reception(self):
        reception = self.create_reception(expected_quantity=2)
        reception.state = 'planned'
        self.registry.flush()
        self.assertEqual(len(reception.lines), 1)
        self.assertOperationStatus(reception, 'planned')

    def test_create_reception_and_execute_it(self):
        reception = self.create_reception(quantity=1)
        self.assertEqual(len(reception.lines[0].operations), 0)
        self.assertFalse(reception.reception_date)

        with patch('toolsapi.toolsapiblok.models.reception.Reception'
                   '.push_in_bus_do_reception'):
            reception.update_state_to_done()

        self.assertEqual(len(reception.lines[0].operations), 1)
        self.assertOperationStatus(reception, 'done')
        self.assertTrue(reception.reception_date)
        self.assertIsNone(reception.rest)

    def test_create_planned_reception_with_partial_execute(self):
        reception = self.create_reception(expected_quantity=2, quantity=1)
        self.assertEqual(len(reception.lines[0].operations), 2)
        self.assertOperationStatus(reception, 'planned')
        self.assertFalse(reception.reception_date)

        with patch('toolsapi.toolsapiblok.models.reception.Reception'
                   '.push_in_bus_do_reception'):
            reception.update_state_to_done()

        self.assertEqual(len(reception.lines[0].operations), 1)
        self.assertOperationStatus(reception, 'done')
        self.assertTrue(reception.reception_date)
        self.assertIsNotNone(reception.rest)
        self.assertEqual(len(reception.rest.lines[0].operations), 1)
        self.assertOperationStatus(reception.rest, 'planned')


class TestApiv1Reception(PyramidBlokTestCase):

    def setUp(self):
        super(TestApiv1Reception, self).setUp()
        self.user = self.registry.User.insert(
            email='t@t', login='test', first_name='test', last_name='test')
        self.registry.User.CredentialStore.insert(
            login='test', password='testpassword')
        resp = self.webserver.post_json(
            '/api/v1/login', {'login': 'test', 'password': 'testpassword'})
        self.headers = {"cookie": resp.headers["Set-Cookie"]}
        self.reception = self.create_reception()

    def create_sender_address(self):
        return self.registry.Address.insert(
            first_name="Shipping",
            last_name="services",
            company_name="Acme",
            street1="1 company street",
            zip_code="75000",
            state="",
            city="Paris",
            country="FRA",
        )

    def create_recipient_address(self):
        return self.registry.Address.insert(
            first_name="Jon",
            last_name="Doe",
            street1="1 street",
            street2="crossroad",
            street3="♥",
            zip_code="66000",
            state="A region",
            city="Perpignan",
            country="FRA",
            phone1="0977552210",
        )

    def create_reception(self):
        sender_address = self.create_sender_address()
        recipient_address = self.create_recipient_address()
        goods_type = self.registry.Wms.PhysObj.Type.query().filter_by(
            code="IAH01-NOIR-12").one()
        return self.registry.Reception.create(
            dict(sender_address=sender_address, recipient_address=recipient_address,
                 pack='Test', reason='Test', tracking_number='test'),
            lines=[
                dict(physobj_type=goods_type,
                     expected_quantity=1),
                dict(physobj_type=goods_type,
                     expected_quantity=1),
            ])

    def assertOperationStatus(self, status, reception=None):
        if reception is None:
            reception = self.reception

        for line in reception.lines:
            if not line.operations:
                self.fail('No operation found')

            for op in line.operations:
                self.assertEqual(op.state, status)

    def test_no_reception(self):
        lines = [dict(id=l.id, physobj_type=dict(id=l.physobj_type.id))
                 for l in self.reception.lines]
        response = self.webserver.patch_json(
            '/api/v1/receptions/%s' % self.reception.uuid,
            dict(lines=lines),
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.reception.state, 'draft')
        self.assertOperationStatus('planned')

    def test_partial_reception(self):
        lines = [dict(id=l.id, physobj_type=dict(id=l.physobj_type.id))
                 for l in self.reception.lines]
        lines[0]['quantity'] = 1

        with patch('toolsapi.toolsapiblok.models.reception.Reception'
                   '.push_in_bus_do_reception'):
            response = self.webserver.patch_json(
                '/api/v1/receptions/%s' % self.reception.uuid,
                dict(state='done', lines=lines),
                headers=self.headers,
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.reception.state, 'done')
        self.assertIsNotNone(self.reception.rest)
        self.assertEqual(len(self.reception.lines), 1)
        self.assertEqual(len(self.reception.rest.lines), 1)
        self.assertOperationStatus('done')

    def test_reception(self):
        lines = [dict(id=l.id, quantity=1, physobj_type=dict(id=l.physobj_type.id))
                 for l in self.reception.lines]

        with patch('toolsapi.toolsapiblok.models.reception.Reception'
                   '.push_in_bus_do_reception'):
            response = self.webserver.patch_json(
                '/api/v1/receptions/%s' % self.reception.uuid,
                dict(state='done', lines=lines),
                headers=self.headers,
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.reception.state, 'done')
        self.assertOperationStatus('done')

    def test_two_way_reception(self):
        lines = [dict(id=l.id, quantity=1, physobj_type=dict(id=l.physobj_type.id))
                 for l in self.reception.lines]

        with patch('toolsapi.toolsapiblok.models.reception.Reception'
                   '.push_in_bus_do_reception'):
            response = self.webserver.patch_json(
                '/api/v1/receptions/%s' % self.reception.uuid,
                dict(state='done', lines=[lines[0]]),
                headers=self.headers,
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.reception.state, 'done')

        with patch('toolsapi.toolsapiblok.models.reception.Reception'
                   '.push_in_bus_do_reception'):
            response = self.webserver.patch_json(
                '/api/v1/receptions/%s' % self.reception.rest.uuid,
                dict(state='done', lines=[lines[1]]),
                headers=self.headers,
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.reception.state, 'done')
        for l in self.reception.lines:
            self.assertOperationStatus('done')

        for l in self.reception.rest.lines:
            self.assertOperationStatus('done', reception=self.reception.rest)

    def test_no_lines(self):
        response = self.webserver.patch_json(
            '/api/v1/receptions/%s' % self.reception.uuid,
            dict(lines=[]),
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.reception.state, 'draft')
        self.assertOperationStatus('planned')
