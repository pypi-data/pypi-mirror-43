from anyblok_pyramid import current_blok
from anyblok_pyramid_rest_api.crud_resource import CrudResource, resource
from anyblok_marshmallow import SchemaWrapper
from anyblok_marshmallow import fields
from marshmallow import Schema
from .inventory import InventoryListSchema

MODEL = "Model.Wms.Inventory.Node"


class PhysObjTypeSchema(Schema):
    id = fields.Integer()


class PhysObjSchema(Schema):
    id = fields.Integer()
    code = fields.String()


class InventoryNodeSerializationSchema(Schema):
    id = fields.Integer()


class InventoryLinePostSchema(Schema):
    id = fields.Integer()
    location = fields.Nested(PhysObjSchema)
    physobj_type = fields.Nested(PhysObjTypeSchema)
    quantity = fields.Integer()
    quantity_observed = fields.Integer()


class InventoryLineSchema(Schema):
    id = fields.Integer()
    location = fields.Nested(PhysObjSchema)
    location_code = fields.String()
    physobj_type = fields.Nested(PhysObjTypeSchema)
    physobj_type_code = fields.String()
    quantity = fields.Integer()


class InventoryNodePostSchema(SchemaWrapper):
    model = MODEL

    class Schema:
        id = fields.Integer()
        state = fields.String()
        lines = fields.Nested(InventoryLinePostSchema, many=True)


class InventoryNodeLightSchema(SchemaWrapper):
    model = MODEL

    class Schema:
        id = fields.Integer()
        inventory_id = fields.Integer()
        state = fields.String()
        parent = fields.Nested("self", allow_none=True)
        leafs = fields.Method('get_leafs')

        @staticmethod
        def get_leafs(obj):
            return InventoryNodeSchema.Schema.get_leafs(obj)


class InventoryNodeSchema(SchemaWrapper):
    model = MODEL

    class Schema:
        id = fields.Integer()
        state = fields.String()
        inventory_id = fields.Integer()
        inventory = fields.Nested(InventoryListSchema)
        parent = fields.Nested("self", allow_none=True)
        location = fields.Nested(PhysObjSchema)
        leafs = fields.Method('get_leafs')
        lines = fields.Method('get_stock_lines')
        actions = fields.Method('get_actions')

        @staticmethod
        def get_leafs(obj):
            if obj.is_leaf:
                return []
            registry = obj.registry
            Wms = registry.Wms
            Node = Wms.Inventory.Node
            PhysObj = Wms.PhysObj
            leafs_raw = (Node.query()
                             .join(Node.location)
                             .filter(Node.parent_id == obj.id,
                                     Node.inventory_id == obj.inventory_id)
                             .order_by(PhysObj.code)
                         ).all()
            leafs = []
            for leaf in leafs_raw:
                leafs.append({
                    'id': leaf.id,
                    'inventory_id': obj.inventory_id,
                    'state': leaf.state,
                    'location': {
                        'id': leaf.location_id,
                        'code': leaf.location.code,
                    }
                })
            return leafs

        @staticmethod
        def get_stock_lines(obj):
            registry = obj.registry
            Wms = registry.Wms
            node_lines = {}
            for line in obj.lines:
                node_lines[line.location_id + line.type_id] = line
            additional_filter = None
            considered_types = obj.inventory.considered_types
            if considered_types:
                additional_filter = Wms.filter_on_phobj_types(
                    obj.inventory.considered_types)

            query = Wms.grouped_quantity_query(joined=True,
                                               location=obj.location,
                                               additional_filter=additional_filter)
            query = query.filter(registry.Wms.PhysObj.Type.query_is_storable())
            lines_raw = query.all()
            lines = []
            for line in lines_raw:
                qty, loc, type_ = line
                index = loc.id + type_.id
                qty_observed = 0
                if index in node_lines.keys():
                    nl = node_lines.pop(index)
                    qty_observed = nl.quantity
                lines.append({
                    'location': {
                        'id': loc.id,
                        'code': loc.code},
                    'physobj_type': {
                        'id': type_.id,
                        'code': type_.code},
                    'quantity': qty,
                    'quantity_observed': qty_observed
                })
            for line in node_lines.values():
                lines.append({
                    'location': {
                        'id': line.location_id,
                        'code': line.location.code},
                    'physobj_type': {
                        'id': line.type_id,
                        'code': line.type.code},
                    'quantity': 0,
                    'quantity_observed': line.quantity})
            if considered_types:
                for type_code in considered_types:
                    filtered_lines = list(
                        filter(
                            lambda line: line['physobj_type']['code'] == type_code,
                            lines)
                    )
                    if len(filtered_lines) == 0:
                        type_ = Wms.PhysObj.Type.query().filter_by(
                            code=type_code).one()
                        loc = type_.get_default_storage_location()
                        lines.append({
                            'location': {
                                'id': loc.id,
                                'code': loc.code},
                            'physobj_type': {
                                'id': type_.id,
                                'code': type_.code},
                            'quantity': 0,
                            'quantity_observed': 0
                        })
            return lines

        @staticmethod
        def get_actions(obj):
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


@resource(
    collection_path='/api/v1/wms/inventories/nodes',
    path='/api/v1/wms/inventories/nodes/{id}',
    installed_blok=current_blok()
)
class InventoryNodeResource(CrudResource):
    model = MODEL

    default_schema = InventoryNodeSchema
    default_deserialize_schema = InventoryNodePostSchema

    def update(self, node, params=None):
        if params is None:
            params = {}

        Wms = self.registry.Wms
        Line = Wms.Inventory.Line
        errors = []
        if 'lines' in params:
            node_lines = {}
            for l in Line.query().filter_by(node=node).all():
                line_index = str(l.location_id) + str(l.type_id)
                node_lines[line_index] = l
            for line in params['lines']:
                if 'id' not in line['location'] or 'id' not in line['physobj_type']:
                    continue
                location_id = line['location']['id']
                type_id = line['physobj_type']['id']
                quantity = line['quantity_observed']
                index = str(location_id) + str(type_id)
                if index in node_lines.keys():
                    node_line = node_lines[index]
                    node_line.quantity = quantity
                else:
                    location = Wms.PhysObj.query().get(location_id)
                    if location is None:
                        errors.append("location not found: %s" % location_id)
                        continue
                    physobj_type = Wms.PhysObj.Type.query().get(type_id)
                    if physobj_type is None:
                        errors.append("physobj_type not found: %s" % type_id)
                        continue
                    Line.insert(node=node,
                                location=location,
                                type=physobj_type,
                                quantity=quantity)
        if errors:
            request = self.request
            request.errors.add('body', '400 Bad request', str(errors))
            request.errors.status = 400
            request.anyblok.registry.rollback()

    def format_light_node(self, node):
        schema = InventoryNodeLightSchema()
        schema.context['registry'] = self.registry
        return schema.dump(node)

    @CrudResource.service('update-state', collection=True, permission='update')
    def update_state(self):
        try:
            params = dict(self.request.json_body)
            ids = params['node_ids']
            node = None
            for node_id in ids:
                node = self.registry.Wms.Inventory.Node.query().get(node_id)
                node.state = params['state']
            return self.format_light_node(node) if len(ids) == 1 else {}
        except Exception as e:
            self.request.errors.add('body', '500 Internal error', str(e))
            self.request.errors.status = 500
            self.request.anyblok.registry.rollback()

    @CrudResource.service('compute-actions', collection=True, permission='update')
    def compute_actions(self):
        try:
            params = dict(self.request.json_body)
            recompute = True if 'recompute' in params else False
            ids = params['node_ids']
            node = None
            for node_id in ids:
                node = self.registry.Wms.Inventory.Node.query().get(node_id)
                node.compute_actions(recompute=recompute)
            return self.format_light_node(node) if len(ids) == 1 else {}
        except Exception as e:
            self.request.errors.add('body', '500 Internal error', str(e))
            self.request.errors.status = 500
            self.request.anyblok.registry.rollback()

    @CrudResource.service('compute-push-actions', collection=True, permission='update')
    def compute_push_actions(self):
        try:
            params = dict(self.request.json_body)
            ids = params['node_ids']
            node = None
            for node_id in ids:
                node = self.registry.Wms.Inventory.Node.query().get(node_id)
                node.compute_push_actions()
            return self.format_light_node(node) if len(ids) == 1 else {}
        except Exception as e:
            self.request.errors.add('body', '500 Internal error', str(e))
            self.request.errors.status = 500
            self.request.anyblok.registry.rollback()

    @CrudResource.service('recurse-compute-push-actions', collection=True, permission='update')
    def recurse_compute_push_actions(self):
        try:
            params = dict(self.request.json_body)
            ids = params['node_ids']
            node = None
            for node_id in ids:
                node = self.registry.Wms.Inventory.Node.query().get(node_id)
                node.recurse_compute_push_actions()
            return self.format_light_node(node) if len(ids) == 1 else {}
        except Exception as e:
            self.request.errors.add('body', '500 Internal error', str(e))
            self.request.errors.status = 500
            self.request.anyblok.registry.rollback()
