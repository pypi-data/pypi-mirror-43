from anyblok import Declarations

Model = Declarations.Model
register = Declarations.register

Sensee = Model.Wms.Sensee


@register(Sensee)
class Preparation:

    @classmethod
    def get_preparation_types(cls):
        res = super(Preparation, cls).get_preparation_types()
        res.update(dict(UNIFOCAL_GLASSES='Unifocal glasses'))
        return res


@register(
    Sensee.Preparation,
    tablename=Sensee.Preparation)
class UnifocalGlasses(Sensee.Preparation):
    """Unifocal glasses preparation (Polymorphic model that overrides
    Model.Wms.Sensee.Preparation

    Namespace: Model.Wms.Sensee.Preparation.UnifocalGlasses
    """
    PREPARATION_TYPE = "UNIFOCAL_GLASSES"

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
        self.plan_stocked(**kwargs)

    @classmethod
    def create(cls, **kwargs):
        """
        Creates the preparation and reservations
        :return:
        """
        preparation = cls.insert(**kwargs)
        preparation.request_frame_reservation()
        req = preparation.request_lenses_reservation()
        req.reserve()
        return preparation
