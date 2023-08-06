def import_declarations(reload=None):
    from . import packing
    from . import delivery
    delivery.import_declarations(reload=reload)
    from . import bus
    from . import preparation
    preparation.import_declarations(reload=reload)
    from . import reception
    from . import wms
    from . import user
    from . import odoo_utils
    if reload is not None:
        reload(packing)
        reload(delivery)
        reload(bus)
        reload(preparation)
        reload(reception)
        reload(wms)
        reload(user)
        reload(odoo_utils)
    from . import odoo8sync
    odoo8sync.import_declarations(reload=reload)
