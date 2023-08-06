from anyblok import Declarations
from anyblok.column import String
from anyblok.relationship import Many2One

Model = Declarations.Model
Mixin = Declarations.Mixin
register = Declarations.register


@register(Model.Wms)
class Warehouse(Mixin.TrackModel):

    code = String(nullable=False, primary_key=True)
    label = String(nullable=False)
    address = Many2One(model=Model.Address, nullable=False)
    root_location = Many2One(model=Model.Wms.PhysObj, nullable=False)
