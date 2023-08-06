from cornice.resource import resource
from anyblok_pyramid_rest_api.crud_resource import CrudResource
from anyblok_pyramid_rest_api.adapter import Adapter
from anyblok_pyramid import current_blok
from anyblok_marshmallow import SchemaWrapper
from marshmallow import Schema, EXCLUDE
from anyblok_marshmallow.fields import Nested, Integer, String, Method, UUID
from sqlalchemy import or_


MODEL = "Model.Reception"


class PhysObjTypeSchema(Schema):
    id = Integer()


class ReceptionLineSchema(SchemaWrapper):
    model = 'Model.Reception.Line'

    class Schema:
        physobj_type = Nested(PhysObjTypeSchema, partial=True)
        expected_quantity = Method('get_expected_quantity', deserialize='set_expected_quantity')
        barcode = String()

        def get_expected_quantity(self, obj):
            return len(obj.operations)

        def set_expected_quantity(self, value):
            if not value:
                return 0

            return int(value)


class AddressSchema(SchemaWrapper):
    model = 'Model.Address'


class DeliveryCarrierSerializeSchema(SchemaWrapper):
    model = 'Model.Delivery.Carrier'


class DeliveryCarrierDeSerializeSchema(Schema):
    uuid = UUID(required=True)


class ReceptionSerializationSchema(SchemaWrapper):
    model = MODEL

    class Schema:
        sender_address = Nested(AddressSchema, partial=True)
        recipient_address = Nested(AddressSchema, partial=True)
        carrier = Nested(DeliveryCarrierSerializeSchema, partial=True)
        lines = Nested(ReceptionLineSchema, many=True)


class ReceptionDeSerializationSchema(SchemaWrapper):
    model = MODEL

    class Schema:
        carrier = Nested(DeliveryCarrierDeSerializeSchema, unknown=EXCLUDE)
        lines = Nested(ReceptionLineSchema, many=True)


class ReceptionAdapter(Adapter):

    @Adapter.filter('sender_address.all_name', ['or-ilike'])
    def filter_by_sender_address_by_names(self, querystring, query, op, value, mode):
        values = value.split(',')
        Reception = self.registry.Reception
        Address = self.registry.Address.aliased(name='sender_address')
        query = query.join(Address, Reception.sender_address_uuid == Address.uuid)
        return self.filter_by_address_by_names(query, Address, values, mode)

    @Adapter.filter('recipient_address.all_name', ['or-ilike'])
    def filter_by_recipient_address_by_names(self, querystring, query, op, value, mode):
        values = value.split(',')
        Reception = self.registry.Reception
        Address = self.registry.Address.aliased(name='recipient_address')
        query = query.join(Address, Reception.recipient_address_uuid == Address.uuid)
        return self.filter_by_address_by_names(query, Address, values, mode)

    def filter_by_address_by_names(self, query, Address, values, mode):
        filters = []
        for value in values:
            value = '%' + value + '%'
            filters.append(or_(
                Address.company_name.ilike(value),
                Address.first_name.ilike(value),
                Address.last_name.ilike(value)
            ))

        if len(filters) == 1:
            filters = filters[0]
        else:
            filters = or_(*filters)

        if mode == 'exclude':
            filters = ~ filters

        return query.filter(filters)


@resource(
    collection_path='/api/v1/receptions',
    path='/api/v1/receptions/{uuid}',
    installed_blok=current_blok()
)
class ReceptionResource(CrudResource):
    model = MODEL
    adapter_cls = ReceptionAdapter
    default_serialize_schema = ReceptionSerializationSchema
    default_deserialize_schema = ReceptionDeSerializationSchema

    def create(self, Model, params=None):
        if params is None:
            params = {}

        lines = params.pop('lines', [])
        for line in lines:
            line.pop('barcode', None)
            line['physobj_type'] = self.registry.Wms.PhysObj.Type.query().get(
                line['physobj_type']['id'])

        if params.get('carrier') and params['carrier'].get('uuid'):
            params['carrier'] = self.registry.Delivery.Carrier.query().get(
                params['carrier']['uuid'])
        if params.get('sender_address') and params['sender_address'].get('uuid'):
            params['sender_address'] = self.registry.Address.query().get(
                params['sender_address']['uuid'])
        if params.get('recipient_address') and params['recipient_address'].get('uuid'):
            params['recipient_address'] = self.registry.Address.query().get(
                params['recipient_address']['uuid'])

        return Model.create(params, lines=lines)

    def update(self, reception, params=None):
        if params is None:
            params = {}

        lines = params.pop('lines', [])
        for line in lines:
            line.pop('barcode', None)
            line['physobj_type'] = self.registry.Wms.PhysObj.Type.query().get(
                line['physobj_type']['id'])

        if params.get('sender_address') and params['sender_address'].get('uuid'):
            params['sender_address'] = self.registry.Address.query().get(
                params['sender_address']['uuid'])
        if params.get('recipient_address') and params['recipient_address'].get('uuid'):
            params['recipient_address'] = self.registry.Address.query().get(
                params['recipient_address']['uuid'])
        if params.get('carrier') and params['carrier'].get('uuid'):
            params['carrier'] = self.registry.Delivery.Carrier.query().get(
                params['carrier']['uuid'])

        reception.update(lines=lines, **params)
