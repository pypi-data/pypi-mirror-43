def import_declarations(reload=None):
    from . import shipment
    if reload is not None:
        reload(shipment)
