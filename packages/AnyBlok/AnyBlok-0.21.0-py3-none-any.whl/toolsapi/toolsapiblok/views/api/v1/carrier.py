from cornice.resource import resource
from anyblok_pyramid_rest_api.crud_resource import CrudResource
from anyblok_pyramid import current_blok


MODEL = "Model.Delivery.Carrier"


@resource(
    collection_path='/api/v1/delivery/carriers',
    path='/api/v1/delivery/carrier/{uuid}',
    installed_blok=current_blok()
)
class DeliveryCarrierResource(CrudResource):
    model = MODEL
