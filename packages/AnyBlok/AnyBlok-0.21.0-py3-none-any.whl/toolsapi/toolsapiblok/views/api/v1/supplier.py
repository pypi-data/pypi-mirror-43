from anyblok_marshmallow import SchemaWrapper
from cornice.resource import resource
from anyblok_pyramid_rest_api.crud_resource import CrudResource
from anyblok_pyramid import current_blok

MODEL = "Model.Supplier"


class SupplierSchema(SchemaWrapper):
    model = MODEL


@resource(
    collection_path='/api/v1/suppliers',
    path='/api/v1/supplier/{uuid}',
    installed_blok=current_blok()
)
class SupplierResource(CrudResource):
    model = MODEL
