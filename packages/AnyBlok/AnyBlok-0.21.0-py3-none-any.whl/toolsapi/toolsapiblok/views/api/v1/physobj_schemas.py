from anyblok_marshmallow import SchemaWrapper
from anyblok_marshmallow import fields
from marshmallow.schema import Schema


class PhysObjTypeListSchema(Schema):
    code = fields.String()


class PhysObjListSchema(Schema):
    code = fields.String()
    type = fields.Nested(PhysObjTypeListSchema)


class PhysObjAvatarListSchema(Schema):
    goods = fields.Nested(PhysObjListSchema)
    location = fields.Nested(PhysObjListSchema)


class PhysObjTypeSchema(SchemaWrapper):
    model = "Model.Wms.PhysObj.Type"

    class Schema:
        parent = fields.Nested("self", allow_none=True)
        properties = fields.Dict()
        short_label = fields.Method("get_short_label")

        @staticmethod
        def get_short_label(phobj_type):
            if phobj_type.label is None:
                return phobj_type.label
            short_label = phobj_type.label
            short_label = short_label.replace("Monture Sensee ", "")
            short_label = short_label.replace("Prémontée Sensee ", "")
            return short_label


class PhysObjTypeSerializeSchema(SchemaWrapper):
    model = "Model.Wms.PhysObj.Type"

    class Schema:
        parent = fields.Nested("self", allow_none=True)
        properties = fields.Dict()
        storage_locations = fields.Method("get_default_storage_locations")
        suppliers_mapping = fields.Method("get_suppliers_physobj_mapping")
        short_label = fields.Method("get_short_label")

        @staticmethod
        def get_short_label(phobj_type):
            if phobj_type.label is None:
                return phobj_type.label
            short_label = phobj_type.label
            short_label = short_label.replace("Monture Sensee ", "")
            short_label = short_label.replace("Prémontée Sensee ", "")
            return short_label

        @staticmethod
        def get_default_storage_locations(phobj_type):
            locations = phobj_type.get_default_storage_locations()
            if len(locations):
                return {loc.id: loc.code for loc in locations}
            else:
                return {}

        @staticmethod
        def get_suppliers_physobj_mapping(phobj_type):
            registry = phobj_type.registry
            mapping = registry.Supplier.PhysObjMapping.query().filter_by(
                physobj_type=phobj_type).all()
            mapping_dict = {}
            for elem in mapping:
                mapping_dict[str(elem.supplier.uuid)] = {
                    'code': elem.code,
                    'name': elem.name,
                    'supplier': elem.supplier.name,
                }
            return mapping_dict


class PhysObjSchema(SchemaWrapper):
    model = "Model.Wms.PhysObj"

    class Schema:
        type = fields.Nested(PhysObjTypeSchema)
        properties = fields.Dict()


class PhysObjAvatarSchema(SchemaWrapper):
    model = "Model.Wms.PhysObj.Avatar"

    class Schema:
        goods = fields.Nested(PhysObjSchema)
        location = fields.Nested(PhysObjSchema)
