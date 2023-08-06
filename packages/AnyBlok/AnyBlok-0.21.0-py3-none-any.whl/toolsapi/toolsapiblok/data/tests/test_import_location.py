from anyblok_wms_base.testing import WmsTestCase
from ..import_location import Location


class TestLocation(WmsTestCase):

    def setUp(self):
        super().setUp()
        self.importer = Location(self.registry)
        self.Avatar = self.registry.Wms.PhysObj.Avatar
        self.location_type = (self.registry.Wms.PhysObj.Type.query()
                              .filter_by(code='location')
                              .one())

    def test_create_location(self):
        Avatar = self.Avatar

        self.importer.dt_from = self.dt_test1

        root = self.importer.create_location('ZEROUT', self.location_type, None)
        self.assertEqual(root.type, self.location_type)
        self.assertEqual(root.code, 'ZEROUT')
        self.assertEqual(Avatar.query().filter_by(obj=root).count(), 0)

        furet = self.importer.create_location('FURET', self.location_type, root)
        self.assertEqual(furet.type, self.location_type)
        self.assertEqual(furet.code, 'FURET')
        av = self.single_result(Avatar.query().filter_by(obj=furet))
        self.assertEqual(av.location, root)
