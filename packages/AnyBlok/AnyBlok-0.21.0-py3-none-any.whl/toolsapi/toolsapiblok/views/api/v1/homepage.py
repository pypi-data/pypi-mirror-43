from anyblok_pyramid import current_blok
from cornice import Service


homepage = Service(name='get_homepage_date',
                   path='api/v1/homepage',
                   description='get homepage data',
                   installed_blok=current_blok())


@homepage.get()
def get_global_init(request):
    registry = request.anyblok.registry
    return {
        'bus_messages': registry.Bus.Message.query().count()
    }
