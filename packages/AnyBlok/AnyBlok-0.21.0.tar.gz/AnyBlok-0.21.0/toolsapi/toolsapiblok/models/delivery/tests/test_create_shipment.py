from anyblok.tests.testcase import BlokTestCase
from json import dumps
from marshmallow.exceptions import ValidationError
from uuid import uuid1
from unittest.mock import patch


class TestShipment(BlokTestCase):
    """ Test delivery model"""

    def setUp(self):
        super(TestShipment, self).setUp()
        # self.registry.Address.query().delete()

    def create_carrier_service_colissimo(self):
        ca = self.registry.Delivery.Carrier.insert(
            name="Colissimo", code="COLISSIMO")

        ca_cred = self.registry.Delivery.Carrier.Credential.insert(
                    account_number="123",
                    password="password")
        service = self.registry.Delivery.Carrier.Service.Colissimo.insert(
                    name="Livraison à domicile", product_code="DOM",
                    carrier=ca, credential=ca_cred)
        return service

    def test_create_shipment_for_colissimo_with_empty_message(self):
        message = {}
        Shipment = self.registry.Delivery.Shipment
        with self.assertRaises(ValidationError):
            Shipment.create_shipment(body=dumps(message))

    def get_message(self):
        colissimo = self.create_carrier_service_colissimo()
        return dict(
            uuid=str(uuid1()),
            service=dict(
                product_code=colissimo.product_code,
                carrier_code=colissimo.carrier_code,
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
            device_code='pnr0.kehl.sensee',
        )

    def test_create_shipment_for_colissimo(self):
        message = self.get_message()
        Shipment = self.registry.Delivery.Shipment
        Address = self.registry.Address
        initial_shipment_count = Shipment.query().count()
        initial_address_count = Address.query().count()

        with patch('toolsapi.toolsapiblok.models.delivery.shipment.Shipment'
                   '.get_and_print_label'):
            Shipment.create_shipment(body=dumps(message))

        self.assertTrue(Shipment.query().count() - initial_shipment_count)
        self.assertEqual(Address.query().count() - initial_address_count, 2)

    def test_create_shipment_for_colissimo_with_existing_address(self):
        Shipment = self.registry.Delivery.Shipment
        Address = self.registry.Address
        initial_shipment_count = Shipment.query().count()
        initial_address_count = Address.query().count()
        message = self.get_message()
        Address.insert(**message['sender_address'])
        self.assertFalse(Shipment.query().count() - initial_shipment_count)
        self.assertEqual(Address.query().count() - initial_address_count, 1)

        with patch('toolsapi.toolsapiblok.models.delivery.shipment.Shipment'
                   '.get_and_print_label'):
            Shipment.create_shipment(body=dumps(message))

        self.assertTrue(Shipment.query().count() - initial_shipment_count)
        self.assertEqual(Address.query().count() - initial_address_count, 2)

    def test_create_shipment_for_colissimo_with_closed_existing_address(self):
        message = self.get_message()
        Shipment = self.registry.Delivery.Shipment
        Address = self.registry.Address
        initial_shipment_count = Shipment.query().count()
        initial_address_count = Address.query().count()
        sender_address = message['sender_address'].copy()
        sender_address.update(dict(street1="♥"))
        Address.insert(**sender_address)
        self.assertFalse(Shipment.query().count() - initial_shipment_count)
        self.assertEqual(Address.query().count() - initial_address_count, 1)

        with patch('toolsapi.toolsapiblok.models.delivery.shipment.Shipment'
                   '.get_and_print_label'):
            Shipment.create_shipment(body=dumps(message))

        self.assertTrue(Shipment.query().count() - initial_shipment_count)
        self.assertEqual(Address.query().count() - initial_address_count, 3)
