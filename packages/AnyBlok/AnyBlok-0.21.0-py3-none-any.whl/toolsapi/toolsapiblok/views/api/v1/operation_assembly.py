from cornice.resource import resource
from anyblok_pyramid_rest_api.crud_resource import CrudResource
from anyblok_pyramid import current_blok
from anyblok_marshmallow import SchemaWrapper
from anyblok_marshmallow import fields
from .physobj_schemas import PhysObjAvatarSchema


MODEL = "Model.Wms.Operation.Assembly"


class OperationAssemblySchema(SchemaWrapper):
    model = "Model.Wms.Operation.Assembly"

    class Schema:
        inputs = fields.Nested(PhysObjAvatarSchema, many=True)
        outcomes = fields.Nested(PhysObjAvatarSchema, many=True)


@resource(
    collection_path='/api/v1/wms/operations/assemblies',
    path='/api/v1/wms/operations/assemblies/{id}',
    installed_blok=current_blok(),
)
class OperationsAssembliesResource(CrudResource):
    model = MODEL

    default_schema = OperationAssemblySchema
