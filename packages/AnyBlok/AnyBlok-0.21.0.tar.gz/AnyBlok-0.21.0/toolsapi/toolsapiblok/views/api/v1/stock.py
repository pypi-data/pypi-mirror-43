from pyramid.response import Response
from cornice.resource import view as cornice_view
from anyblok_pyramid_rest_api.crud_resource import (
    CrudResource, resource, saved_errors_in_request,
    update_from_query_string, collection_get_validator)
from anyblok_pyramid_rest_api.adapter import Adapter
from anyblok_pyramid import current_blok
from marshmallow.schema import Schema
from anyblok_marshmallow.fields import Nested, Integer
from .physobj_schemas import PhysObjSchema, PhysObjTypeSerializeSchema
from sqlalchemy import func, or_
from datetime import datetime
import csv
import tempfile


class StockLocationSchema(Schema):
    location = Nested(PhysObjSchema)
    physobj_type = Nested(PhysObjTypeSerializeSchema)
    quantity = Integer()


class StockLocationAdapter(Adapter):

    @Adapter.filter('physobj_type.code', ['or-ilike'])
    def filter_by_goods_type_code(self, querystring, query, operator, value, mode):
        values = value.split(',')
        filters = [self.registry.Wms.PhysObj.Type.code.ilike('%' + v + '%')
                   for v in values]
        if len(filters) > 1:
            filters = or_(*filters)
        else:
            filters = filters[0]

        if mode == 'exclude':
            filters = ~ filters

        return query.filter(filters)

    @Adapter.filter('location.code', ['or-ilike'])
    def filter_by_location_code(self, querystring, query, operator, value, mode):
        values = value.split(',')
        filters = ["location.code ilike '%" + v + "%'" for v in values]
        if len(filters) > 1:
            filters = or_(*filters)
        else:
            filters = filters[0]

        if mode == 'exclude':
            filters = ~ filters

        return query.filter(filters)

    @Adapter.filter('quantity', ['eq', 'lt', 'gt'])
    def filter_by_quantity(self, querystring, query, operator, value, mode):
        leftpart = func.count('wms_physobj_avatar.id')
        if operator == 'eq':
            condition = leftpart == value
        elif operator == 'lt':
            condition = leftpart < value
        elif operator == 'gt':
            condition = leftpart > value

        if mode == 'exclude':
            condition = ~ condition

        return query.having(condition)

    @Adapter.filter('at_date', ['eq'])
    def filter_by_date(self, querystring, query, operator, value, mode):
        return query

    @Adapter.filter('at_datetime', ['eq'])
    def filter_by_datetime(self, querystring, query, operator, value, mode):
        return query

    @Adapter.order_by('quantity')
    def order_by_quantity(self, querystring, query, op):
        order_by = getattr(func.count('wms_physobj_avatar.id'), op)()
        return query.order_by(order_by)

    @Adapter.order_by('physobj_type.code')
    def order_by_physobj_type_code(self, querystring, query, op):
        return query.order_by('wms_physobj_type.code %s' % op)

    @Adapter.order_by('location.code')
    def order_by_location_code(self, querystring, query, op):
        return query.order_by('location.code %s' % op)


@resource(
    collection_path="/api/v1/wms/stock/locations",
    path="/api/v1/wms/stock/locations/{id}",
    installed_blok=current_blok()
)
class StockByLocationsResource(CrudResource):
    model = "Model.Wms"
    adapter_cls = StockLocationAdapter

    @cornice_view(validators=(collection_get_validator,), permission="read")
    def collection_get(self):
        request = self.request
        if request.errors:
            return []

        with saved_errors_in_request(request):
            registry = request.anyblok.registry
            at_datetime = None
            if 'filter[at_date][eq]' in request.params:
                at_datetime = datetime.strptime(
                    request.params['filter[at_date][eq]'] + ' 23:59:59',
                    '%d/%m/%Y %H:%M:%S')
            if 'filter[at_datetime][eq]' in request.params:
                at_datetime = datetime.strptime(
                    request.params['filter[at_datetime][eq]'],
                    '%d/%m/%Y %H:%M:%S')
            query = registry.Wms.grouped_quantity_query(joined=True,
                                                        at_datetime=at_datetime)
            query = query.filter(registry.Wms.PhysObj.Type.query_is_storable())
            adapter = StockLocationAdapter(registry, None)
            adapter.load_decorators()
            query = update_from_query_string(request, None, query, adapter)
            if query.count():
                res = [{'quantity': qty, 'physobj_type': physobj_type,
                        'location': location}
                       for qty, location, physobj_type in query.all()]
                schema = StockLocationSchema(context=dict(registry=registry),
                                             many=True)
                return schema.dump(res)

            return []

    @CrudResource.service('get_csv', collection=True, permission='read')
    def get_csv_from_querystring(self):
        data = self.collection_get()
        if len(data) == 0:
            return
        Parameter = self.registry.System.Parameter
        warehouse_code = Parameter.get('warehouse_code')
        dict_data = []
        for row in data:
            if 'product_category' not in row['physobj_type']['properties']:
                continue
            dict_data.append({
                'warehouse': warehouse_code,
                'location': row['location']['code'],
                'sku': row['physobj_type']['code'],
                'label': row['physobj_type']['label'].replace(',', ''),
                'quantity': row['quantity'],
                'type': row['physobj_type']['parent']['code'],
                'category': row['physobj_type']['properties']['product_category'],
                'cost_price': round(row['physobj_type']['properties']['cost_price'], 2),
                'valo': round(row['quantity'] * row['physobj_type']['properties']['cost_price'], 2)
            })
        content = __class__.write_stock_to_csv(csv_columns=[*dict_data[0]], dict_data=dict_data)
        filename = 'stock_by_locations.%s.csv' % datetime.now().strftime("%d%m%Y%H%M%S")
        return Response(
            request=self.request,
            content_type='text/csv',
            content_length=len(content),
            content_disposition='attachment; filename="%s"' % (
                filename
            ),
            body=content
        )

    @staticmethod
    def write_stock_to_csv(csv_columns, dict_data):
        try:
            with tempfile.TemporaryFile(mode='r+') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=csv_columns, delimiter=";")
                writer.writeheader()
                for data in dict_data:
                    writer.writerow(data)
                csv_file.seek(0)
                content = csv_file.read()
                csv_file.close()
                return content
        except IOError as err:
            errno, strerror = err.args
            print("I/O error({0}): {1}".format(errno, strerror))
        return
