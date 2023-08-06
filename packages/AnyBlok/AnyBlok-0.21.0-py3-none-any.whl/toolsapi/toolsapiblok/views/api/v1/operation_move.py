from cornice import Service
from anyblok_pyramid.security import AnyBlokResourceFactory
from cornice.resource import resource
from anyblok_pyramid_rest_api.crud_resource import CrudResource, get_item
from anyblok_pyramid_rest_api.adapter import Adapter
from anyblok_pyramid import current_blok
from anyblok_marshmallow import SchemaWrapper
from anyblok_marshmallow import fields
from .physobj_schemas import (PhysObjListSchema, PhysObjAvatarListSchema,
                              PhysObjSchema, PhysObjAvatarSchema)
from anyblok.declarations import Declarations

Model = Declarations.Model


MODEL = "Model.Wms.Operation.Move"


class OperationMoveListSchema(SchemaWrapper):
    model = MODEL

    class Schema:
        reason = fields.String()
        comment = fields.String()
        dt_execution = fields.DateTime()
        input = fields.Nested(PhysObjAvatarListSchema)
        destination = fields.Nested(PhysObjListSchema)
        executable = fields.Method('is_executable')

        @staticmethod
        def is_executable(operation):
            for inp in operation.inputs:
                if inp.state != 'present':
                    return False
            return True


class OperationMoveDeserializeSchema(SchemaWrapper):
    model = MODEL

    class Schema:
        reason = fields.String()
        input = fields.Nested(PhysObjAvatarSchema)
        inputs = fields.List(fields.Nested(PhysObjAvatarSchema))
        destination = fields.Nested(PhysObjSchema)
        outcomes = fields.List(fields.Nested(PhysObjAvatarSchema))


class OperationMoveSchema(SchemaWrapper):
    model = MODEL

    class Schema:
        reason = fields.String()
        input = fields.Nested(PhysObjAvatarSchema)
        inputs = fields.List(fields.Nested(PhysObjAvatarSchema))
        destination = fields.Nested(PhysObjSchema)
        outcomes = fields.Nested(PhysObjAvatarSchema, many=True)
        executable = fields.Method('is_executable')
        reversible = fields.Method('is_reversible')
        obliviatable = fields.Method('is_obliviatable')
        cancelable = fields.Method('is_cancelable')

        @staticmethod
        def is_executable(operation):
            for inp in operation.inputs:
                if inp.state != 'present':
                    return False
            return True

        @staticmethod
        def is_reversible(operation):
            return operation.state == 'done' and operation.is_reversible()

        @staticmethod
        def is_obliviatable(operation):
            return operation.state == 'done'

        @staticmethod
        def is_cancelable(operation):
            return operation.state == 'planned'


class OperationMoveAdapter(Adapter):

    @Adapter.filter('input.type.code', ['or-ilike'])
    def filter_by_input_type(self, querystring, query, operator, value, mode):
        PhysObj = self.registry.Wms.PhysObj
        Operation = self.registry.Wms.Operation
        gt_ids = []
        for val in value.split(','):
            gt_ids += PhysObj.Type.query('id').filter(
                PhysObj.Type.code.contains(val.upper())).all()

        res = Operation.query_join_input_physobj(query=query)
        query = res['query']
        query = query.filter(res['obj_alias'].type_id.in_(gt_ids))
        return query

    @Adapter.filter('input.location.code', ['or-ilike'])
    def filter_by_location(self, querystring, query, operator, value, mode):
        PhysObj = self.registry.Wms.PhysObj
        Operation = self.registry.Wms.Operation
        loc_ids = []
        for val in value.split(','):
            loc_ids += PhysObj.query('id').filter(
                PhysObj.code.contains(val.upper())).all()

        res = Operation.query_join_input_physobj(query=query)
        query = res['query']
        query = query.filter(res['av_alias'].location_id.in_(loc_ids))
        return query

    @Adapter.filter('destination.code', ['or-ilike'])
    def filter_by_destination(self, querystring, query, operator, value, mode):
        PhysObj = self.registry.Wms.PhysObj
        Operation = self.registry.Wms.Operation
        Move = Operation.Move
        loc_ids = []
        for val in value.split(','):
            loc_ids += PhysObj.query('id').filter(
                PhysObj.code.contains(val.upper())).all()

        query = query.filter(Move.destination_id.in_(loc_ids))
        return query

    @Adapter.tag('object-is-storable')
    def tag_object_is_storable(self, querystring, query):
        """
        Filter by physobj with 'storable' property set to True
        :param querystring:
        :param query:
        :return:
        """
        Operation = self.registry.Wms.Operation
        res = Operation.query_join_output_physobj(query=query)
        query = res['query']
        query = query.filter(
            res['type_alias'].behaviours.comparator.contains({'storable': True}))
        return query

    @Adapter.tag('object-is-a-container')
    def tag_object_is_a_container(self, querystring, query):
        """
        Filter by physobj with 'container' property set
        :param querystring:
        :param query:
        :return:
        """
        Operation = self.registry.Wms.Operation
        res = Operation.query_join_output_physobj(query=query)
        query = res['query']
        query = query.filter(
            res['type_alias'].behaviours.comparator.has_key('container'))  # noqa
        return query

    @Adapter.tag('operation-is-executable')
    def tag_operation_is_executable(self, querystring, query):
        """
        Filter by physobj with 'container' property set
        :param querystring:
        :param query:
        :return:
        """
        Operation = self.registry.Wms.Operation
        res = Operation.query_join_input_physobj(query=query)
        query = res['query']
        query = query.filter(res['av_alias'].state == 'present')
        return query


alter_destination = Service(name='alter_destination',
                            path='api/v1/wms/operations/moves/{id}/alter-destination',
                            description='alter destination',
                            installed_blok=current_blok(),
                            factory=AnyBlokResourceFactory('operations'),
                            permission='update')


@alter_destination.patch()
def alter_move_destination(request):
    try:
        registry = request.anyblok.registry
        PhysObj = registry.Wms.PhysObj
        dest_id = request.params['destination_id']
        destination = PhysObj.query().get(dest_id)
        operation = get_item(request, MODEL)
        operation.alter_destination(destination)
        return destination.to_dict()
    except Exception as e:
        request.errors.add('body', '500 Internal error', str(e))
        request.errors.status = 500
        request.anyblok.registry.rollback()
        return


@resource(
    collection_path='/api/v1/wms/operations/moves',
    path='/api/v1/wms/operations/moves/{id}',
    installed_blok=current_blok(),
)
class OperationsMovesResource(CrudResource):
    model = MODEL

    default_schema = OperationMoveSchema
    deserialize_schema = OperationMoveDeserializeSchema
    serialize_collection_get = OperationMoveListSchema
    adapter_cls = OperationMoveAdapter

    def create(self, Model, params=None):
        if params is None:
            params = {}

    def update(self, operation, params=None):
        if params is None:
            params = {}

        PhysObj = self.registry.Wms.PhysObj
        destination_id = params['destination']['id']
        destination = PhysObj.query().filter_by(id=destination_id).first()
        operation.alter_destination(destination)

    def update_collection_get_filter(self, query):
        return query.filter_by(type="wms_move")
