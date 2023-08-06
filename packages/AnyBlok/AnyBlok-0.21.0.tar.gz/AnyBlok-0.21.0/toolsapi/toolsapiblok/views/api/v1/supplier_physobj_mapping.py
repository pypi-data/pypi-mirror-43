from anyblok_marshmallow import SchemaWrapper, Nested
from anyblok_pyramid_rest_api.adapter import Adapter
from cornice.resource import resource
from anyblok_pyramid_rest_api.crud_resource import CrudResource
from anyblok_pyramid import current_blok
from marshmallow.fields import String

from .physobj_schemas import PhysObjTypeSchema
from .supplier import SupplierSchema


MODEL = "Model.Supplier.PhysObjMapping"


class SupplierPhysObjMappingSchema(SchemaWrapper):
    model = MODEL

    class Schema:
        code = String()
        name = String()
        supplier = Nested(SupplierSchema)
        physobj_type = Nested(PhysObjTypeSchema)


class SupplierPhysObjMappingAdapter(Adapter):

    @Adapter.filter('physobj_type.code', ['or-ilike'])
    def filter_by_physobj_type(self, querystring, query, operator, value, mode):
        PhysObjType = self.registry.Wms.PhysObj.Type
        PhysObjMapping = self.registry.Supplier.PhysObjMapping
        type_ids = []
        for val in value.split(','):
            type_ids = (PhysObjType.query('id')
                        .filter(PhysObjType.code.contains(val.upper())).all())

        query = query.filter(PhysObjMapping.physobj_type_id.in_(type_ids))
        return query

    @Adapter.filter('supplier.name', ['or-ilike'])
    def filter_by_supplier_name(self, querystring, query, operator, value, mode):
        Supplier = self.registry.Supplier
        PhysObjMapping = self.registry.Supplier.PhysObjMapping
        supplier_uuids = []
        for val in value.split(','):
            supplier_uuids = Supplier.query().filter(Supplier.name.contains(val)).all().uuid

        query = query.filter(PhysObjMapping.supplier_uuid.in_(supplier_uuids))
        return query


@resource(
    collection_path='/api/v1/suppliers/physobj-mapping',
    path='/api/v1/suppliers/{supplier_uuid}/physobj-mapping/{code}',
    installed_blok=current_blok()
)
class SupplierPhysObjMappingResource(CrudResource):
    model = MODEL
    default_schema = SupplierPhysObjMappingSchema

    adapter_cls = SupplierPhysObjMappingAdapter
