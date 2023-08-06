from anyblok import Declarations

Model = Declarations.Model
register = Declarations.register

Sensee = Model.Wms.Sensee


@register(Sensee)
class Preparation:

    @classmethod
    def get_preparation_types(cls):
        res = super(Preparation, cls).get_preparation_types()
        res.update(dict(SIMPLE='Simple'))
        return res


@register(
    Sensee.Preparation,
    tablename=Sensee.Preparation)
class Simple(Sensee.Preparation):
    """Simple preparation (Polymorphic model that overrides
    Model.Wms.Sensee.Preparation

    Namespace: Model.Wms.Sensee.Preparation.Simple
    """
    PREPARATION_TYPE = "SIMPLE"

    def request_simple_reservation(self):
        """
        reserves the frame
        :return:
        """
        req = self.get_reservation_request(purpose=['PREPARATION', self.code])
        return req

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
        preparation.request_simple_reservation()
        return preparation

    def push_status_in_bus(self):
        self.state = 'done'
        super(Simple, self).push_status_in_bus()
