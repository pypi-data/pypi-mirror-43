from anyblok.tests.testcase import BlokTestCase
from .. import import_declarations


class TestPhysObjPackage(BlokTestCase):

    def test_reload(self):
        import sys
        module_type = sys.__class__  # is there a simpler way ?

        def fake_reload(module):
            self.assertIsInstance(module, module_type)

        import_declarations(reload=fake_reload)
