from cornice.resource import resource
from anyblok_pyramid_rest_api.crud_resource import CrudResource
from anyblok_pyramid import current_blok
from marshmallow import Schema, fields
from anyblok_marshmallow import SchemaWrapper
from anyblok_marshmallow.fields import Nested
from .operation import OperationSchema
from .operation_move import OperationMoveSchema
from .operation_assembly import OperationAssemblySchema


MODEL = "Model.Wms.Sensee.Preparation"


class PreparationPropertiesInputsSchema(Schema):
    frame_code = fields.Str()
    right_lens_code = fields.Str(required=True)
    left_lens_code = fields.Str(required=True)


class PreparationPropertiesBomSchema(Schema):
    glasses_case_code = fields.Str()
    inputs = Nested(PreparationPropertiesInputsSchema)


class PreparationPropertiesSchema(Schema):
    reason = fields.Str(required=True)
    quantity = fields.Integer(required=True)
    bom = Nested(PreparationPropertiesBomSchema)


OperationSchemas = {
    'Model.Wms.Operation.Arrival': OperationSchema(),
    'Model.Wms.Operation.Observation': OperationSchema(),
    'Model.Wms.Operation.Move': OperationMoveSchema(),
    'Model.Wms.Operation.Assembly': OperationAssemblySchema(),
}


class PreparationSchema(SchemaWrapper):
    model = MODEL

    class Schema:
        properties = Nested(PreparationPropertiesSchema)
        operations = fields.Method('get_operations')

        def get_operations(self, preparation):
            result = []
            for operation in preparation.operations:
                schema = OperationSchemas.get(
                    operation.__registry_name__,
                    SchemaWrapper(model=operation.__registry_name__))
                schema.context = self.context
                result.append(schema.dump(operation))

            return result


class PreparationPropertiesPartialSchema(Schema):
    reason = fields.Str(required=True)
    quantity = fields.Integer(required=True)
    bom = Nested(PreparationPropertiesBomSchema(partial=True))


class PreparationPartialSchema(SchemaWrapper):
    model = MODEL

    class Schema:
        properties = Nested(PreparationPropertiesSchema(partial=True))


@resource(
    collection_path='/api/v1/wms/preparations/np-eyewear',
    path='/api/v1/wms/preparations/np-eyewear/{uuid}',
    installed_blok=current_blok()
)
class PreparationResource(CrudResource):
    model = MODEL

    default_schema = PreparationSchema
    deserialize_patch = PreparationPartialSchema

    def create(self, Model, params):
        if params is None:
            params = {}

        return Model.create(**params)

    def update(self, preparation, params=None):
        if params is None:
            return preparation

        preparation.modify(params)
