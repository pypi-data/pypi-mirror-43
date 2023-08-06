from anyblok_pyramid_rest_api.adapter import Adapter
from cornice.resource import resource
from anyblok_pyramid_rest_api.crud_resource import CrudResource
from anyblok_pyramid import current_blok
from .physobj_schemas import PhysObjSchema

MODEL = "Model.Wms.PhysObj"


class PhysObjLocationAdapter(Adapter):

    @Adapter.filter('parent_location.id', ['or-ilike'])
    def filter_by_parent_location(self, querystring, query, operator, value, mode):
        PhysObj = self.registry.Wms.PhysObj
        parent_ids = [val for val in value.split(',')]
        query = (query
                 .join(PhysObj.Avatar.obj)
                 .join(PhysObj.type)
                 .filter(PhysObj.Type.code == 'location',
                         PhysObj.Avatar.location_id.in_(parent_ids))
                 .order_by(PhysObj.code))
        return query


@resource(
    collection_path='/api/v1/wms/physobj/locations',
    path='/api/v1/wms/physobj/locations/{id}',
    installed_blok=current_blok()
)
class PhysObjLocationResource(CrudResource):
    model = MODEL
    default_schema = PhysObjSchema
    adapter_cls = PhysObjLocationAdapter

    def update_collection_get_filter(self, query):
        PhysObj = self.registry.Wms.PhysObj
        if self.adapter.has_filter_for('parent_location.id', 'or-ilike'):
            return query
        query = query.join(PhysObj.type)
        return query.filter(PhysObj.Type.query_is_a_container())
