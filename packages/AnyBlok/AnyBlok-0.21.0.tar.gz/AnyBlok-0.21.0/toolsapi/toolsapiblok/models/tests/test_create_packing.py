from anyblok.tests.testcase import BlokTestCase
from json import dumps
from marshmallow.exceptions import ValidationError
from uuid import uuid4
from os import urandom
from unittest.mock import patch
from base64 import b64encode


class TestShipment(BlokTestCase):
    """ Test delivery model"""

    def test_create_packing_document_with_empty_message(self):
        message = {}
        with self.assertRaises(ValidationError):
            self.registry.Packing.Document.create_packing_document(
                body=dumps(message))

    def test_create_packing_document_with_minimum_message(self):
        message = {'uuid': str(uuid4()), 'invoices': [],
                   'cerfas': [], 'prescriptions': []}
        self.registry.Packing.Document.create_packing_document(
            body=dumps(message))
        packing = self.registry.Packing.Document.query().get(message['uuid'])
        self.assertIsNotNone(packing)
        self.assertEqual(str(packing.uuid), message['uuid'])
        self.assertFalse(packing.invoices)
        self.assertFalse(packing.cerfas)
        self.assertFalse(packing.prescriptions)

    def test_create_packing_document_with_one_invoice(self):
        self.registry.Device.PrinterCups.insert(code='printer')
        file_ = urandom(100)
        message = {
            'uuid': str(uuid4()),
            'invoices': [{
                'device_code': 'printer',
                'name': 'file.jpg',
                'mimestype': 'application/jpeg',
                'binary': b64encode(file_).decode('utf-8'),
            }],
            'cerfas': [],
            'prescriptions': [],
        }
        with patch('toolsapi.toolsapiblok.models.packing.Line'
                   '.print_document'):
            self.registry.Packing.Document.create_packing_document(
                body=dumps(message))

        packing = self.registry.Packing.Document.query().get(message['uuid'])
        self.assertIsNotNone(packing)
        self.assertTrue(packing.invoices)
        self.assertFalse(packing.cerfas)
        self.assertFalse(packing.prescriptions)
        self.assertEqual(packing.invoices[0].latest_document.lobject, file_)

    def test_create_packing_document_with_one_cerfa(self):
        self.registry.Device.PrinterCups.insert(code='printer')
        file_ = urandom(100)
        message = {
            'uuid': str(uuid4()),
            'invoices': [],
            'cerfas': [{
                'device_code': 'printer',
                'name': 'file.jpg',
                'mimestype': 'application/jpeg',
                'binary': b64encode(file_).decode('utf-8'),
            }],
            'prescriptions': [],
        }
        with patch('toolsapi.toolsapiblok.models.packing.Line'
                   '.print_document'):
            self.registry.Packing.Document.create_packing_document(
                body=dumps(message))

        packing = self.registry.Packing.Document.query().get(message['uuid'])
        self.assertIsNotNone(packing)
        self.assertFalse(packing.invoices)
        self.assertTrue(packing.cerfas)
        self.assertFalse(packing.prescriptions)
        self.assertEqual(packing.cerfas[0].latest_document.lobject, file_)

    def test_create_packing_document_with_one_prescription(self):
        self.registry.Device.PrinterCups.insert(code='printer')
        file_ = urandom(100)
        message = {
            'uuid': str(uuid4()),
            'invoices': [],
            'cerfas': [],
            'prescriptions': [{
                'device_code': 'printer',
                'name': 'file.jpg',
                'mimestype': 'application/jpeg',
                'binary': b64encode(file_).decode('utf-8'),
            }],
        }
        with patch('toolsapi.toolsapiblok.models.packing.Line'
                   '.print_document'):
            self.registry.Packing.Document.create_packing_document(
                body=dumps(message))

        packing = self.registry.Packing.Document.query().get(message['uuid'])
        self.assertIsNotNone(packing)
        self.assertFalse(packing.invoices)
        self.assertFalse(packing.cerfas)
        self.assertTrue(packing.prescriptions)
        self.assertEqual(packing.prescriptions[0].latest_document.lobject, file_)
