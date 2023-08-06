from cornice.resource import resource
from anyblok_pyramid_rest_api.crud_resource import CrudResource
from anyblok_marshmallow import SchemaWrapper
from anyblok_marshmallow.fields import Nested, String
from marshmallow.schema import Schema
from anyblok_pyramid import current_blok
from bloks_sensee.bloks.backend.views.api.v1.devices import DeviceSchema

MODEL = "Model.Packing.Document"


class AttachmentDocumentSchema(Schema):
    filename = String()


class PackingDocumentLineSchema(SchemaWrapper):
    model = 'Model.Packing.Document.Line'

    class Schema:
        printer = Nested(DeviceSchema)
        latest_document = Nested(AttachmentDocumentSchema)


class SerializationPackingDocumentSchema(SchemaWrapper):
    model = MODEL

    class Schema:
        invoices = Nested(PackingDocumentLineSchema, many=True)
        cerfas = Nested(PackingDocumentLineSchema, many=True)
        prescriptions = Nested(PackingDocumentLineSchema, many=True)


@resource(
    collection_path='/api/v1/packing/documents',
    path='/api/v1/packing/documents/{uuid}',
    installed_blok=current_blok()
)
class PackingDocumentResource(CrudResource):
    model = MODEL
    has_collection_post = False
    has_put = False
    has_patch = False
    has_delete = False

    default_serialize_schema = SerializationPackingDocumentSchema
