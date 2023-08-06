from anyblok import Declarations
from anyblok.column import String
from anyblok.relationship import Many2Many, Many2One


@Declarations.register(Declarations.Model)
class User:

    email = String(nullable=False)
    # warehouse = Many2One(model=Declarations.Model.Wms.Warehouse)
    # warehouses = Many2Many(model=Declarations.Model.Wms.Warehouse)
