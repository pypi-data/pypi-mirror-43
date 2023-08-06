from cornice import Service
from anyblok_pyramid.security import AnyBlokResourceFactory
from anyblok_pyramid_rest_api.crud_resource import get_item
from cornice.resource import resource
from anyblok_pyramid_rest_api.crud_resource import CrudResource
from anyblok_pyramid_rest_api.adapter import Adapter
from sqlalchemy import or_

from anyblok_marshmallow.schema import SchemaWrapper
from anyblok_marshmallow.fields import Nested
from anyblok_pyramid import current_blok


MODEL = "Model.Delivery.Shipment"


class AddressSchema(SchemaWrapper):
    model = 'Model.Address'


class SerializationModelSchema(SchemaWrapper):
    model = MODEL

    class Schema:
        sender_address = Nested(AddressSchema)
        recipient_address = Nested(AddressSchema)


process = Service(name='update_state',
                  path='api/v1/shipments/update/label/{uuid}',
                  description='update state',
                  installed_blok=current_blok(),
                  factory=AnyBlokResourceFactory('shipments'),
                  permission='update')


@process.get()
def update_label_get(request):
    try:
        if request.matchdict['uuid'].upper() == 'ALL':
            request.anyblok.registry.Delivery.Shipment.get_labels_status()
        else:
            shipment = get_item(request, MODEL)
            shipment.get_label_status()
    except Exception as e:
        request.errors.add('body', '500 Internal error', str(e))
        request.errors.status = 500
        request.anyblok.registry.rollback()

    return {}


class ShipmentAdapter(Adapter):

    @Adapter.filter('sender_address.all_name', ['or-ilike'])
    def filter_by_sender_address_by_names(self, querystring, query, op, value, mode):
        values = value.split(',')
        Shipment = self.registry.Delivery.Shipment
        Address = self.registry.Address.aliased(name='sender_address')
        query = query.join(Address, Shipment.sender_address_uuid == Address.uuid)
        return self.filter_by_address_by_names(query, Address, values, mode)

    @Adapter.filter('recipient_address.all_name', ['or-ilike'])
    def filter_by_recipient_address_by_names(self, querystring, query, op, value, mode):
        values = value.split(',')
        Shipment = self.registry.Delivery.Shipment
        Address = self.registry.Address.aliased(name='recipient_address')
        query = query.join(Address, Shipment.recipient_address_uuid == Address.uuid)
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
    collection_path='/api/v1/shipments',
    path='/api/v1/shipment/{uuid}',
    installed_blok=current_blok()
)
class ShipmentResource(CrudResource):
    model = MODEL
    adapter_cls = ShipmentAdapter

    default_serialize_schema = SerializationModelSchema

    @classmethod
    def get_serialize_opts(self, rest_action):
        opts = super(ShipmentResource, self).get_serialize_opts(rest_action)
        opts['exclude'] = ['document']
        if rest_action == 'collection_get':
            opts['exclude'].append('properties')

        return opts
