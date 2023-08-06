from cornice import Service
from anyblok_pyramid.security import AnyBlokResourceFactory
from anyblok_pyramid import current_blok
from anyblok_pyramid_rest_api.crud_resource import get_items
from anyblok_marshmallow import SchemaWrapper
from anyblok_marshmallow.fields import Nested
from anyblok_pyramid_rest_api.schema import FullRequestSchema
from anyblok_pyramid_rest_api.validator import service_collection_get_validator
from pyramid.response import Response
from pyramid.security import remember

MODEL = "Model.Wms.Sensee.Preparation"

preparations = Service(name='get_preparations',
                       path='api/v1/wms/preparations',
                       description='get preparations',
                       installed_blok=current_blok(),
                       factory=AnyBlokResourceFactory('preparations'),
                       permission='authenticated')


class PreparationSchema(SchemaWrapper):
    model = MODEL


class PreparationRequestSchema(FullRequestSchema):
    path = Nested(PreparationSchema(only=['uuid']))


@preparations.get(
    validators=(service_collection_get_validator,),
    schema=PreparationRequestSchema
)
def preparations_collection_get(request):
    collection = get_items(request, MODEL)
    if not collection:
        return
    dschema = PreparationSchema()
    if dschema:
        return dschema.dump(
            collection,
            registry=request.anyblok.registry,
            many=True
        )
    else:
        return collection.to_dict()


tray_labels = Service(name='print_tray_labels',
                      path='api/v1/wms/preparations/print-labels',
                      description='print tray labels',
                      installed_blok=current_blok(),
                      factory=AnyBlokResourceFactory('preparations'),
                      permission='authenticated')


@tray_labels.get()
def preparations_print_tray_labels(request):
    try:
        registry = request.anyblok.registry
        params = dict(request.params)
        labels_type = params['labels_type']
        device_code = params['device_code']
        Preparation = registry.Wms.Sensee.Preparation
        document_uuid = Preparation.print_tray_labels(labels_type)
        Device = registry.Device
        printer = Device.query().filter_by(code=device_code).one()
        printer.action_print_document(
            str(printer.uuid),  # dramatiq d'ont suport uuid
            document_uuid=str(document_uuid)
        )
    except Exception as e:
        request.errors.add('body', '500 Internal error', str(e))
        request.errors.status = 500
        request.anyblok.registry.rollback()


barcode = Service(
    name='get-preparation-from-barcode',
    path='api/v1/wms/preparations/from-barcode',
    description='gets a preparation from the barcode scanned',
    installed_blok=current_blok(),
    factory=AnyBlokResourceFactory('preparations'),
    permission='read')


@barcode.get()
def preparations_get_preparation_from_barcode(request):
    registry = request.anyblok.registry
    params = dict(request.params)
    barcode = params['value']
    Preparation = registry.Wms.Sensee.Preparation
    query = Preparation.query()
    preparation_data = Preparation.properties['preparation_data']
    if "OF" in barcode:
        query = query.filter(
            preparation_data.comparator.contains({'odoo_name': barcode}))
    elif "P" in barcode:
        query = query.filter_by(code=barcode)
    else:
        query.filter(preparation_data.comparator.contains({'reason': barcode}))
    preparation = query.one_or_none()
    if preparation is None:
        request.errors.add('header', 'barcode',
                           'preparation not found')
        request.errors.status = 401
        return
    try:
        return dict(
            uuid=str(preparation.uuid),
            preparation_type=preparation.preparation_type
        )
    except Exception as e:
        request.errors.add('body', '500 Internal error', str(e))
        request.errors.status = 500
        request.anyblok.registry.rollback()


task = Service(
    name='get-next-task-data',
    path='api/v1/wms/preparations/next-task-data',
    description='gets needed data for the next task to accomplish',
    installed_blok=current_blok(),
    factory=AnyBlokResourceFactory('preparations'),
    permission='update')


@task.get()
def preparations_get_next_task_data(request):
    registry = request.anyblok.registry
    params = dict(request.params)
    Preparation = registry.Wms.Sensee.Preparation
    preparation = Preparation.query().filter_by(
        uuid=params['uuid']).one_or_none()
    if preparation is None:
        request.errors.add('header', 'uuid',
                           'preparation not found')
        request.errors.status = 401
        return
    try:
        if preparation.state in ['todo', 'picking_in_progress']:
            return preparation.get_picking_data()
        else:
            return dict()
    except Exception as e:
        request.errors.add('body', '500 Internal error', str(e))
        request.errors.status = 500
        request.anyblok.registry.rollback()


validate_picking = Service(
    name='validate_products_picking',
    path='api/v1/wms/preparations/validate-products-picking',
    description='validates products picking',
    installed_blok=current_blok(),
    factory=AnyBlokResourceFactory('preparations'),
    permission='update')


@validate_picking.post()
def preparations_validate_products_picking(request):
    Preparation = request.anyblok.registry.Wms.Sensee.Preparation
    params = request.json_body
    preparation_uuid = params['preparation_uuid']
    preparation = Preparation.query().filter_by(
        uuid=preparation_uuid).one_or_none()
    if preparation is None:
        request.errors.add('header', 'preparation_uuid',
                           'preparation not found')
        request.errors.status = 401
        return
    try:
        next_preparation = preparation.validate_picking(params)
        if next_preparation is None:
            next_uuid = ''
            next_preparation_type = ''
        else:
            next_uuid = str(next_preparation.uuid)
            next_preparation_type = next_preparation.preparation_type
        headers = remember(request, preparation_uuid)
        title_key = 'preparations.picking.message.picking_completed'
        preparation_data = preparation.properties['preparation_data']
        message_content = preparation_data['odoo_name']
        return Response(
            json_body={
                'message': {
                    'type': 'is-success',
                    'title_key': title_key,
                    'content': message_content,
                },
                'uuid': next_uuid,
                'preparation_type': next_preparation_type,
            },
            headers=headers
        )
    except Exception as e:
        request.errors.add('body', '500 Internal error', str(e))
        request.errors.status = 500
        request.anyblok.registry.rollback()
