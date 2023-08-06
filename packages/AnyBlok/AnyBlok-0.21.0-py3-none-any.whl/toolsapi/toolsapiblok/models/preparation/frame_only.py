from anyblok import Declarations

Model = Declarations.Model
register = Declarations.register

Sensee = Model.Wms.Sensee


@register(Sensee)
class Preparation:

    @classmethod
    def get_preparation_types(cls):
        res = super(Preparation, cls).get_preparation_types()
        res.update(dict(FRAME_ONLY='Frame only'))
        return res


@register(
    Sensee.Preparation,
    tablename=Sensee.Preparation)
class FrameOnly(Sensee.Preparation):
    """Frame only preparation (Polymorphic model that overrides
    Model.Wms.Sensee.Preparation

    Namespace: Model.Wms.Sensee.Preparation.FrameOnly
    """
    PREPARATION_TYPE = "FRAME_ONLY"

    def plan_one(self, items):
        """
        plans preparation operations
        :return:
        """
        return True

    @classmethod
    def create(cls, **kwargs):
        """
        Creates the preparation and reservations
        :return:
        """
        preparation = cls.insert(**kwargs)
        req = preparation.request_frame_reservation()
        req.reserve()
        return preparation

    def push_status_in_bus(self):
        self.state = 'done'
        super(FrameOnly, self).push_status_in_bus()
