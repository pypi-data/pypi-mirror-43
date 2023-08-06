from anyblok_pyramid_rest_api.adapter import Adapter
from anyblok_pyramid import current_blok
from anyblok_pyramid_rest_api.crud_resource import CrudResource, resource
from anyblok_marshmallow import SchemaWrapper
from anyblok_marshmallow import fields
from marshmallow import Schema

MODEL = "Model.Wms.Inventory"


class PhysObjSchema(Schema):
    id = fields.Integer()


class UserSchema(Schema):
    login = fields.String()


class InventoryNodeSerializationSchema(Schema):
    id = fields.Integer()
    state = fields.String()


class InventoryPostSchema(SchemaWrapper):
    model = MODEL

    class Schema:
        id = fields.Integer()
        reason = fields.String()
        creator = fields.Nested(UserSchema)
        root_location = fields.Nested(PhysObjSchema)
        date = fields.DateTime()
        considered_types = fields.List(fields.String())


class InventorySerializationSchema(Schema):
    id = fields.Integer()


class InventorySchema(SchemaWrapper):
    model = MODEL

    class Schema:
        id = fields.Integer()
        reason = fields.String()
        creator = fields.Nested(UserSchema)
        root = fields.Method('get_root_node')
        root_location = fields.Method('get_root_location')
        considered_types = fields.List(fields.String())
        considered_references = fields.Method('get_considered_references')
        date = fields.DateTime()
        nodes = fields.Method('get_nodes')
        split = fields.Method('is_split')

        def get_root_node(self, obj):
            root = obj.root
            return {
                'id': root.id,
                'inventory_id': root.inventory_id,
                'location': root.location.to_dict(),
                'state': root.state,
                'actions': self.get_pushed_actions(obj=root)
            }

        @staticmethod
        def get_pushed_actions(obj):
            actions = []
            for action in obj.actions:
                new_action = {
                    'type': action.type,
                    'physobj_type': {
                        'id': action.physobj_type_id,
                        'code': action.physobj_type.code
                    },
                    'quantity': action.quantity,
                    'location': {
                        'id': action.location_id,
                        'code': action.location.code
                    },
                    'destination': {}
                }
                if action.destination_id:
                    new_action['destination'] = {
                        'id': action.destination_id,
                        'code': action.destination.code
                    }
                actions.append(new_action)
            return actions

        @staticmethod
        def get_root_location(obj):
            return {'id': obj.root.location.id}

        @staticmethod
        def format_node(node):
            return {
                'id': node.id,
                'inventory_id': node.inventory_id,
                'location': {
                  'id': node.location_id,
                  'code': node.location.code,
                },
                'leafs': __class__.get_leafs(node, node.is_leaf),
                'state': node.state
            }

        @staticmethod
        def get_nodes(obj):
            registry = obj.registry
            Wms = registry.Wms
            Node = Wms.Inventory.Node
            PhysObj = Wms.PhysObj
            nodes_raw = Node.query().join(Node.location).filter(
                Node.inventory_id == obj.id,
                Node.parent_id == obj.root.id).order_by(PhysObj.code).all()
            nodes = []
            for node in nodes_raw:
                nodes.append(__class__.format_node(node))
            return nodes

        @staticmethod
        def format_leaf(leaf):
            return {
                'id': leaf.id,
                'inventory_id': leaf.inventory_id,
                'state': leaf.state,
                'location': {
                    'id': leaf.location_id,
                    'code': leaf.location.code,
                }
            }

        @staticmethod
        def get_leafs(node, is_leaf=True):
            if is_leaf:
                return [__class__.format_leaf(node)]
            registry = node.registry
            Wms = registry.Wms
            Node = Wms.Inventory.Node
            PhysObj = Wms.PhysObj
            leafs_raw = Node.query().join(Node.location).filter(
                Node.parent_id == node.id).order_by(PhysObj.code).all()
            leafs = []
            for leaf in leafs_raw:
                leafs.append(__class__.format_leaf(leaf))
            return leafs

        @staticmethod
        def is_split(obj):
            Node = obj.registry.Wms.Inventory.Node
            nd = Node.query().filter_by(inventory=obj,
                                        parent=obj.root).first()
            return Node.query().filter_by(parent=nd).count() > 0

        @staticmethod
        def get_considered_references(obj):
            if not obj.considered_types:
                return []
            Type = obj.registry.Wms.PhysObj.Type
            gts = Type.query().filter(Type.code.in_(obj.considered_types)).all()
            references = []
            for gt in gts:
                phobj_type = {
                    'id': gt.id,
                    'code': gt.code,
                }
                references.append({'physobj_type': phobj_type})
            return references


class InventoryListSchema(SchemaWrapper):
    model = MODEL

    class Schema:
        id = fields.Integer()
        reason = fields.String()
        creator = fields.Nested(UserSchema)
        root = fields.Nested(InventoryNodeSerializationSchema)
        root_location_code = fields.Method('get_root_location_code')
        date = fields.DateTime()

        @staticmethod
        def get_root_location_code(obj):
            return obj.root.location.code


class InventoryAdapter(Adapter):

    @Adapter.filter('root.code', ['or-ilike'])
    def filter_by_root_code(self, querystring, query, operator, value, mode):
        return query


@resource(
    collection_path='/api/v1/wms/inventories',
    path='/api/v1/wms/inventories/{id}',
    installed_blok=current_blok()
)
class InventoryResource(CrudResource):
    model = MODEL

    default_schema = InventorySchema
    default_deserialize_schema = InventoryPostSchema
    serialize_collection_get = InventoryListSchema
    adapter_cls = InventoryAdapter

    def create(self, Model, params):
        if params is None:
            params = {}

        Wms = self.registry.Wms
        root_location = None
        if 'root_location' in params:
            root_id = params['root_location']['id']
            root_location = Wms.PhysObj.query().get(root_id)
            if root_location is None:
                raise LookupError('location', root_id)
        if 'physobj_type' in params:
            type_id = params['physobj_type']['id']
            type = Wms.PhysObj.Type.query().get(type_id)
            if type is None:
                raise LookupError('physobj_type', type_id)

        refs = params['considered_types'] if 'considered_types' in params else []

        creator_login = params['creator']['login']
        creator = self.registry.User.query().filter_by(login=creator_login).one()

        fields_ = dict(
            reason=params['reason'],
            creator=creator,
            date=params['date'],
            considered_types=refs,
        )

        inventory = Model.create(root_location, **fields_)
        if not refs:
            inventory.root.split()
        return inventory

    @CrudResource.service('reconcile-all', collection=True, permission='update')
    def reconcile_all(self):
        try:
            params = dict(self.request.json_body)
            for inv_id in params['inventory_ids']:
                inventory = self.registry.Wms.Inventory.query().get(inv_id)
                if inventory is None:
                    raise LookupError('inventory', inv_id)
                inventory.reconcile_all()
        except Exception as e:
            self.request.errors.add('body', '500 Internal error', str(e))
            self.request.errors.status = 500
            self.request.anyblok.registry.rollback()

        return {}

    @CrudResource.service('split-leafs', collection=True, permission='update')
    def split_leafs(self):
        try:
            Inventory = self.registry.Wms.Inventory
            params = dict(self.request.json_body)
            for inv_id in params['inventory_ids']:
                inventory = Inventory.query().get(inv_id)
                if inventory is None:
                    raise LookupError('inventory', inv_id)
                nodes = Inventory.Node.query().filter_by(parent=inventory.root).all()
                nodes.split()
        except Exception as e:
            self.request.errors.add('body', '500 Internal error', str(e))
            self.request.errors.status = 500
            self.request.anyblok.registry.rollback()

        return {}
