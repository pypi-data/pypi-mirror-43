from anyblok import Declarations

Model = Declarations.Model
register = Declarations.register

Sensee = Model.Wms.Sensee


@register(Sensee)
class Preparation:

    @classmethod
    def get_preparation_types(cls):
        res = super(Preparation, cls).get_preparation_types()
        res.update(dict(PROGRESSIVE_GLASSES='Progressive glasses'))
        return res


@register(
    Sensee.Preparation,
    tablename=Sensee.Preparation)
class ProgressiveGlasses(Sensee.Preparation):
    """Progressive glasses preparation (Polymorphic model that overrides
    Model.Wms.Sensee.Preparation

    Namespace: Model.Wms.Sensee.Preparation.ProgressiveGlasses
    """
    PREPARATION_TYPE = "PROGRESSIVE_GLASSES"

    def plan_one(self, items):
        """
        plans preparation operations
        :return:
        """
        kwargs = dict(
            frame=items[0].physobj,
            right_lens=items[1].physobj,
            left_lens=items[2].physobj
        )
        self.plan_rx(**kwargs)

    @classmethod
    def create(cls, **kwargs):
        """
        Creates the preparation and reservations
        :return:
        """
        preparation = cls.insert(**kwargs)
        req = preparation.request_frame_reservation()
        preparation.plan_lenses_arrival_and_reserve()
        req.reserve()
        return preparation
