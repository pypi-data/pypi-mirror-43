from anyblok import Declarations
from anyblok.column import String, DateTime
from anyblok_postgres.column import Jsonb
from anyblok.relationship import Many2One

Model = Declarations.Model
register = Declarations.register


@register(Model.Wms)
class Inventory:
    """Overriding Wms.Inventory to add some fields
    """

    reason = String()
    """Reason of the inventory"""

    creator = Many2One(model="Model.User",
                       index=True)
    """Creator of the inventory"""

    date = DateTime(label="Inventory start date")
    """Date when the inventory starts"""

    excluded_types = Jsonb(default=["location", "TRAY", "TRAY/LL", "TRAY/RL"])
    """List of Physobj.Type codes to be excluded.
    Excluding tray related types by default
    """


@register(Model.Wms.Inventory)
class Action:
    def apply(self):
        """Perform Inventory Operations for the current Action.

        :return: tuple of the newly created Operations

        The new Operations will all point to the related Inventory.
        """
        Operation = self.registry.Wms.Operation
        inventory = self.node.inventory
        op_fields = dict(reason=inventory.reason,
                         state='done',
                         inventory=inventory)
        if self.type == 'app':
            return (
                Operation.Apparition.create(
                    physobj_type=self.physobj_type,
                    physobj_code=self.physobj_code,
                    physobj_properties=self.physobj_properties,
                    quantity=self.quantity,
                    location=self.location,
                    **op_fields),
            )

        # only Operations with (single) input remain
        avatars = self.choose_affected()
        if self.type == 'disp':
            Op = Operation.Disparition
        else:
            Op = Operation.Teleportation
            op_fields['new_location'] = self.destination

        return tuple(Op.create(input=av, **op_fields) for av in avatars)
