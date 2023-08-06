from datetime import datetime
import csv


class Location:

    def __init__(self, registry):
        self.registry = registry
        self.PhysObj = registry.Wms.PhysObj

    def import_locations_as_goods(self, file_path, **options):
        goods_types = self.create_goods_types()
        self.dt_from = datetime.now()
        query = self.PhysObj.query()
        query = query.join(self.PhysObj.type)
        query = query.filter(self.PhysObj.Type.query_is_a_container())
        existing_locations = {loc.code: loc for loc in query.all()}
        imported_locations = {}
        with open(file_path) as csvfile:
            spamreader = csv.reader(csvfile, **options)
            next(spamreader)  # remove headers
            for (identity, code, parent_identity, goods_type) in spamreader:
                if code is None:
                    continue
                location = existing_locations.pop(code, None)
                goods_type = goods_types[goods_type]
                if location is None:
                    imported_locations[identity] = self.create_location(
                        code, goods_type,
                        imported_locations.get(parent_identity, None))
                else:
                    imported_locations[identity] = location
                    self.update_location_tree(
                        location, goods_type,
                        imported_locations.get(parent_identity, None))

        if existing_locations:
            pass  # TODO desapear location

    def create_goods_type(self, code, container):
        location_type = self.PhysObj.Type.query().filter_by(code=code).one_or_none()
        if location_type is None:
            location_type = self.PhysObj.Type.insert(
                code=code, behaviours=dict(container=container))

        return location_type

    def create_goods_types(self):
        return {
            'location': self.create_goods_type('location', {})
        }

    def create_location(self, code, goods_type, parent):
        Wms = self.registry.Wms
        if parent is None:
            return Wms.create_root_container(goods_type, code=code)

        app = Wms.Operation.Apparition.create(
                    physobj_type=goods_type,
                    physobj_code=code,
                    quantity=1,
                    location=parent,
                    dt_execution=self.dt_from,
                    state='done')
        return next(iter(app.outcomes)).obj

    def update_location_tree(self, location, goods_type, parent_location):
        print(' ==> update location tree', location, goods_type, parent_location)
