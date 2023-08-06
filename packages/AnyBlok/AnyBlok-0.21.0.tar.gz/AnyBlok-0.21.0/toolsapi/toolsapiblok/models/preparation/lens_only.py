from anyblok import Declarations

Model = Declarations.Model
register = Declarations.register

Sensee = Model.Wms.Sensee


@register(Sensee)
class Preparation:

    @classmethod
    def get_preparation_types(cls):
        res = super(Preparation, cls).get_preparation_types()
        res.update(dict(LENS_ONLY='Lens only'))
        return res


@register(
    Sensee.Preparation,
    tablename=Sensee.Preparation)
class LensOnly(Sensee.Preparation):
    """Lens only preparation (Polymorphic model that overrides
    Model.Wms.Sensee.Preparation

    Namespace: Model.Wms.Sensee.Preparation.LensOnly
    """
    PREPARATION_TYPE = "LENS_ONLY"

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
        req = preparation.request_lenses_reservation()
        req.reserve()
        return preparation
