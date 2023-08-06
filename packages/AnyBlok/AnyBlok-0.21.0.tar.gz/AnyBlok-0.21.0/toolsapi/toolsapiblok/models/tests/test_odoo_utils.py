from anyblok.tests.testcase import BlokTestCase


class TestOdooUtils(BlokTestCase):

    def setUp(self):
        super().setUp()
        self.Utils = self.registry.OdooUtils

    def test_odoo_product_to_tools_wms(self):
        convert = self.Utils.odoo8_product_to_tools_wms
        self.assertEqual(convert('hop', 'foo'), ('hop', 'foo'))

    def test_odoo_product_to_tools_wms_schema(self):
        convert = self.Utils.odoo8_product_schema_to_tools_wms
        data = dict(odoo_product_code='hop',
                    odoo_production_lot_name='foo')
        data_c = data.copy()

        self.assertEqual(convert(data), ('hop', 'foo'))
        # nothing has been removed
        self.assertEqual(data, data_c)

    def test_odoo_product_to_tools_wms_schema_pop(self):
        convert = self.Utils.odoo8_product_schema_to_tools_wms
        data = dict(odoo_product_code='hop',
                    odoo_production_lot_name='foo')

        self.assertEqual(convert(data, pop=True), ('hop', 'foo'))
        # nothing has been removed
        self.assertEqual(data, {})

    def test_tools_wms_to_odoo_product(self):
        convert = self.Utils.tools_wms_to_odoo8_product
        self.assertEqual(convert('foo', 'bar'), ('foo', 'bar'))
