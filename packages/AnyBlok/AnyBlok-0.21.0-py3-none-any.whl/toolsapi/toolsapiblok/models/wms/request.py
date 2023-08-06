from anyblok import Declarations
from anyblok.relationship import Many2One

Model = Declarations.Model
register = Declarations.register


@register(Model.Wms.Reservation)
class Request:

    preparation = Many2One(model=Model.Wms.Sensee.Preparation,
                           one2many="requests")

    def is_preparation(self):
        if not isinstance(self.purpose, (list, tuple)):
            return False
        return self.purpose[0] == "PREPARATION"

    def reserve(self):
        """Try and perform reservation for all RequestItems.

        :return: ``True`` if all reservations are now taken
        :rtype: bool

        if the request concerns a preparation, the request attribute 'reserved'
        will be True only if the number of RequestItems equals 3 (frame,
        right_lens, left_lens).
        It's useful because if we only have the frame RequestItem, we don't want
        to plan any operation while we don't have the lenses RequestItems

        It also indicates to a possible worker (reserver process) if the request
        needs to be considered to perform reservations.
        """
        Item = self.registry.Wms.Reservation.RequestItem
        # could use map() and all(), but it's not recommended style
        # if there are strong side effects.
        all_reserved = True
        req_items = Item.query().filter(Item.request == self).all()
        for item in req_items:
            all_reserved = all_reserved and item.reserve()
        if not self.is_preparation():
            self.reserved = all_reserved
        else:
            self.reserved = len(req_items) == 3 and all_reserved

        return all_reserved
