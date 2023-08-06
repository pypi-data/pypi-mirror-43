from anyblok_pyramid import current_blok
from cornice import Service


global_ = Service(name='get_global_init',
                  path='api/v1/init/global',
                  description='get global data for backend initialization',
                  installed_blok=current_blok())


@global_.get()
def get_global_init(request):
    registry = request.anyblok.registry
    country = registry.loaded_namespaces_first_step[
        'Model.Address']['country']
    status = registry.loaded_namespaces_first_step[
        'Model.Delivery.Shipment']['status']
    Role = registry.User.Role
    Device = registry.Device
    roles = [x.to_dict('name', 'label') for x in Role.query().all()]
    printers = [
        x.to_dict('name', 'code')
        for x in Device.query().filter(Device.device_type.ilike('%printer%')).all()
    ]
    default_tray_labels_device_code = 'tray2.prn1.kehl.sensee'
    if request.authenticated_userid is None:
        user = {
            'login': '',
            'label': '',
            'roles': [],
        }
    else:
        user = registry.User.query().get(request.authenticated_userid)
        user = {
            'login': user.login,
            'label': user.name,
            'roles': registry.User.get_roles(user.login),
            'warehouse': user.warehouse and user.warehouse.code or '',
            'warehouses': {w.code: w.label for w in user.warehouses},
        }

    return {
        'global': {
            'selection_labels': {
                'countries': country.choices,
                'shipment_states': status.selections,
                'device_types': registry.Device.get_device_types(),
                'preparation_types': registry.Wms.Sensee.Preparation.get_preparation_types(),
            },
            'roles': roles,
            'printers': printers,
            'default_tray_labels_device_code': default_tray_labels_device_code,
        },
        'user': user,
    }
