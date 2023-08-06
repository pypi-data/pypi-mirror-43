from anyblok import Declarations

Model = Declarations.Model
register = Declarations.register

Sensee = Model.Wms.Sensee


@register(Sensee)
class Preparation:

    @classmethod
    def get_preparation_types(cls):
        res = super(Preparation, cls).get_preparation_types()
        res.update(dict(HOME_TRIAL_FRAMES='Home trial'))
        return res


@register(
    Sensee.Preparation,
    tablename=Sensee.Preparation)
class HomeTrial(Sensee.Preparation):
    """Home trial preparation (Polymorphic model that overrides
    Model.Wms.Sensee.Preparation

    Namespace: Model.Wms.Sensee.Preparation.HomeTrial
    """
    PREPARATION_TYPE = "HOME_TRIAL_FRAMES"

    def get_frame_types(self):
        PhysObjType = self.registry.Wms.PhysObj.Type
        inputs = self.properties.get('bom').get('inputs').get('frame_codes')
        types = []
        for inp in inputs:
            gt = PhysObjType.query().filter_by(code=inp).first()
            types.append(gt)
        return types

    def request_frame_reservations(self):
        """
        reserves the frame
        :return:
        """
        Reservation = self.registry.Wms.Reservation
        RequestItem = Reservation.RequestItem

        req = self.get_reservation_request(purpose=['PREPARATION', self.code])
        gts = self.get_frame_types()
        for gt in gts:
            RequestItem.insert(
                goods_type=gt,
                quantity=1,
                request=req,
            )
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
        req = preparation.request_frame_reservations()
        req.reserve()
        return preparation

    def push_status_in_bus(self):
        self.state = 'done'
        super(HomeTrial, self).push_status_in_bus()
