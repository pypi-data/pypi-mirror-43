from cornice import Service
from anyblok_pyramid.security import AnyBlokResourceFactory
from cornice.resource import resource
from anyblok_pyramid_rest_api.crud_resource import CrudResource
from anyblok_pyramid import current_blok
from anyblok_marshmallow import SchemaWrapper
from anyblok_marshmallow import fields
from .physobj_schemas import (PhysObjTypeListSchema, PhysObjAvatarListSchema,
                              PhysObjAvatarSchema)


MODEL = "Model.Wms.Operation"


class OperationListSchema(SchemaWrapper):
    model = MODEL

    class Schema:
        inputs = fields.List(fields.Nested(PhysObjAvatarListSchema))
        goods_type = fields.Nested(PhysObjTypeListSchema)
        reason = fields.String()


class OperationSchema(SchemaWrapper):
    model = MODEL

    class Schema:
        inputs = fields.List(fields.Nested(PhysObjAvatarSchema), )
        outcomes = fields.Nested(PhysObjAvatarSchema, many=True)


execute = Service(name='execute_operation',
                  path='api/v1/wms/operations/execute/',
                  description='execute_operation',
                  installed_blok=current_blok(),
                  factory=AnyBlokResourceFactory('operations'),
                  permission='update')


@execute.post()
def execute_operation(request):
    try:
        registry = request.anyblok.registry
        params = dict(request.json_body)
        for op_id in params['operation_ids']:
            operation = registry.Wms.Operation.query().get(op_id)
            operation.execute()
    except Exception as e:
        request.errors.add('body', '500 Internal error', str(e))
        request.errors.status = 500
        request.anyblok.registry.rollback()

    return {}


revert = Service(name='revert_operation',
                 path='api/v1/wms/operations/revert/',
                 description='revert_operation',
                 installed_blok=current_blok(),
                 factory=AnyBlokResourceFactory('operations'),
                 permission='update')


@revert.post()
def revert_operation(request):
    try:
        registry = request.anyblok.registry
        params = dict(request.json_body)
        ids = []
        for op_id in params['operation_ids']:
            operation = registry.Wms.Operation.query().get(op_id)
            rev, leafs = operation.plan_revert()
            ids.append({'id': rev.id})
        return ids
    except Exception as e:
        request.errors.add('body', '500 Internal error', str(e))
        request.errors.status = 500
        request.anyblok.registry.rollback()

    return {}


obliviate = Service(name='obliviate_operation',
                    path='api/v1/wms/operations/obliviate/',
                    description='obliviate_operation',
                    installed_blok=current_blok(),
                    factory=AnyBlokResourceFactory('operations'),
                    permission='update')


@obliviate.post()
def obliviate_operation(request):
    try:
        registry = request.anyblok.registry
        params = dict(request.json_body)
        for op_id in params['operation_ids']:
            operation = registry.Wms.Operation.query().get(op_id)
            operation.obliviate()
    except Exception as e:
        request.errors.add('body', '500 Internal error', str(e))
        request.errors.status = 500
        request.anyblok.registry.rollback()

    return {}


cancel = Service(name='cancel_operation',
                 path='api/v1/wms/operations/cancel/',
                 description='cancel_operation',
                 installed_blok=current_blok(),
                 factory=AnyBlokResourceFactory('operations'),
                 permission='update')


@cancel.post()
def cancel_operation(request):
    try:
        registry = request.anyblok.registry
        params = dict(request.json_body)
        for op_id in params['operation_ids']:
            operation = registry.Wms.Operation.query().get(op_id)
            operation.cancel()
    except Exception as e:
        request.errors.add('body', '500 Internal error', str(e))
        request.errors.status = 500
        request.anyblok.registry.rollback()

    return {}


@resource(
    collection_path='/api/v1/wms/operations',
    path='/api/v1/wms/operations/{id}',
    installed_blok=current_blok()
)
class OperationsResource(CrudResource):
    model = MODEL

    default_schema = OperationSchema
    serialize_collection_get = OperationListSchema
