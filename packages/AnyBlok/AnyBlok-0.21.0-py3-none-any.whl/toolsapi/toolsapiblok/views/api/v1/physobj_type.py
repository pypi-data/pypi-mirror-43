from sqlalchemy import or_
from cornice.resource import resource
from anyblok_pyramid_rest_api.crud_resource import CrudResource
from anyblok_pyramid_rest_api.adapter import Adapter
from anyblok_pyramid import current_blok
from .physobj_schemas import PhysObjTypeSchema, PhysObjTypeSerializeSchema

MODEL = "Model.Wms.PhysObj.Type"


class PhysObjTypeAdapter(Adapter):

    @Adapter.filter('code', ['eq', 'ilike', 'like'])
    def filter_by_code_or_supplier_code(self, querystring, query,
                                        operator, value, mode):
        """Filter Storable PhysObj.Type per code or supplier code through
        SupplierPhysObjMapping
        """
        PhysObjType = self.registry.Wms.PhysObj.Type
        SupplierPhysObjMapping = self.registry.Supplier.PhysObjMapping
        old_enable_assertions = query._enable_assertions
        try:
            query._enable_assertions = False
            query = query.select_from(SupplierPhysObjMapping).join(
                SupplierPhysObjMapping.physobj_type, full=True)
        finally:
            query._enable_assertions = old_enable_assertions

        if operator == 'eq':
            condition = PhysObjType.code == value
            condition2 = PhysObjType.label == value
        elif operator in ('ilike', 'like'):
            condition = getattr(PhysObjType.code, operator)("%" + value + "%")
            condition2 = getattr(PhysObjType.label, operator)("%" + value + "%")

        query = query.filter(
            PhysObjType.behaviours.contains({'storable': True}),
            or_(
                condition,
                condition2,
                SupplierPhysObjMapping.code == value,
            )
        )

        return query.order_by(PhysObjType.code)

    @Adapter.tag('parent is lens')
    def tag_parent_is_lens(self, querystring, query):
        """
        Filter by parent code 'lens'
        :param querystring:
        :param query:
        :return:
        """
        PhysObjType = self.registry.Wms.PhysObj.Type
        lens_gt = PhysObjType.query().filter_by(code='LENS').one()
        query = query.filter(PhysObjType.parent == lens_gt)
        return query

    @Adapter.tag('parent is frame')
    def tag_parent_is_frame(self, querystring, query):
        """
        Filter by parent code 'frame'
        :param querystring:
        :param query:
        :return:
        """
        PhysObjType = self.registry.Wms.PhysObj.Type
        frame_gt = PhysObjType.query().filter_by(code='FRAME').one()
        query = query.filter(PhysObjType.parent == frame_gt)
        return query

    @Adapter.tag('parent is np eyewear')
    def tag_parent_is_np_eyewear(self, querystring, query):
        """
        Filter by parent code 'np_eyewear'
        :param querystring:
        :param query:
        :return:
        """
        PhysObjType = self.registry.Wms.PhysObj.Type
        np_eyewear_gt = PhysObjType.query().filter_by(code='NP_EYEWEAR').one()
        query = query.filter(PhysObjType.parent == np_eyewear_gt)
        return query

    @Adapter.tag('parent is simple')
    def tag_parent_is_simple(self, querystring, query):
        """
        Filter by parent code 'simple'
        :param querystring:
        :param query:
        :return:
        """
        PhysObjType = self.registry.Wms.PhysObj.Type
        simple_gt = PhysObjType.query().filter_by(code='SIMPLE').one()
        query = query.filter(PhysObjType.parent == simple_gt)
        return query

    @Adapter.tag('parent is consumable')
    def tag_parent_is_consumable(self, querystring, query):
        """
        Filter by parent code 'consumable'
        :param querystring:
        :param query:
        :return:
        """
        PhysObjType = self.registry.Wms.PhysObj.Type
        consumable_gt = PhysObjType.query().filter_by(code='CONSUMABLE').one()
        query = query.filter(PhysObjType.parent == consumable_gt)
        return query


@resource(
    collection_path='/api/v1/wms/physobj/types',
    path='/api/v1/wms/physobj/types/{id}',
    installed_blok=current_blok()
)
class PhysObjTypeResource(CrudResource):
    model = MODEL
    adapter_cls = PhysObjTypeAdapter
    default_schema = PhysObjTypeSchema
    serialize_schema = PhysObjTypeSerializeSchema
    serialize_get = PhysObjTypeSerializeSchema

    def update_collection_get_filter(self, query):
        Model = self.get_model('collection_get')
        return query.filter(Model.query_is_storable())
