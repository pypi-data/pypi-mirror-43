from anyblok import Declarations

Model = Declarations.Model
register = Declarations.register

Sensee = Model.Wms.Sensee


@register(Sensee)
class Preparation:

    @classmethod
    def get_preparation_types(cls):
        res = super(Preparation, cls).get_preparation_types()
        res.update(dict(NP_EYEWEAR='Np eyewear'))
        return res


@register(
    Sensee.Preparation,
    tablename=Sensee.Preparation)
class NpEyewear(Sensee.Preparation):
    """NpEyewear preparation (Polymorphic model that overrides
    Model.Wms.Sensee.Preparation

    Namespace: Model.Wms.Sensee.Preparation.NpEyewear
    """
    PREPARATION_TYPE = "NP_EYEWEAR"

    EXPECTED_PICKING_KEYS = ["frame_code",
                             "right_lens_code", "left_lens_code"]

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

    # TODO: should be changed when we work again on preparations UI, deprecated
    # def get_picking_data(self):
    #     """
    #     Returns picking data for front
    #     :return:
    #     """
    #     picking_operations = self.get_operations('picking')
    #     inputs = self.properties['bom']['inputs']
    #     expected_inputs = {}
    #     codes = []
    #     for k, v in inputs.items():
    #         if k in ['frame_code',
    #                  'right_lens_code',
    #                  'left_lens_code']:
    #             expected_inputs[k] = v
    #             codes.append(v)

    #     frame_code = inputs['frame_code']
    #     rlens_code = inputs['right_lens_code']
    #     llens_code = inputs['left_lens_code']

    #     refs = [op.input.obj.type.code
    #             for op in picking_operations
    #             if op.type == 'wms_move'
    #             and op.input.obj.type.code in codes
    #             and op.state == 'done']
    #     rlens_done = False
    #     llens_done = False
    #     if rlens_code in refs:
    #         rlens_done = True
    #         refs.remove(rlens_code)
    #     if llens_code in refs:
    #         llens_done = True

    #     return {
    #         'uuid': str(self.uuid),
    #         'expected_inputs': expected_inputs,
    #         'frame_code': frame_code if frame_code in refs else '',
    #         'right_lens_code': rlens_code if rlens_done else '',
    #         'left_lens_code': llens_code if llens_done else '',
    #     }

    # def get_expected_picking_references(self):
    #     inputs = self.properties['bom']['inputs']
    #     expected_references = {}
    #     for key, code in inputs.items():
    #         if key in self.EXPECTED_PICKING_KEYS:
    #             expected_references[key] = code
    #     return expected_references

    # def get_picking_move(self, key, code):
    #     if key not in self.EXPECTED_PICKING_KEYS:
    #         raise ValueError("key %s was not expected", key)
    #     expected_references = self.get_expected_picking_references()
    #     if code not in expected_references.values():
    #         raise ValueError("code %s was not expected", code)

    #     operations = self.get_operations('picking', 'wms_move')
    #     for op in operations:
    #         obj = op.input.obj
    #         if obj.type.code != code:
    #             continue
    #         if (obj.properties is not None
    #                 and obj.properties.get('eye') is not None
    #                 and obj.properties.get('eye') in key):
    #             return op
    #         elif obj.properties is None:
    #             return op

    # def validate_picking(self, params):
    #     """
    #     Validates the picking of the items passed for npeyewear
    #     :return:
    #     """
    #     posted_references = {}
    #     for key, code in params.items():
    #         if key in self.EXPECTED_PICKING_KEYS and code != "":
    #             posted_references[key] = code

    #     for key, code in posted_references.items():
    #         op = self.get_picking_move(key=key, code=code)
    #         op.execute()

    #     if len(self.EXPECTED_PICKING_KEYS) == len(posted_references.keys()):
    #         picking_operations = self.get_operations('picking')
    #         for op in picking_operations:
    #             op.execute()
    #         self.update(**dict(state='assembly_in_progress'))
    #     else:
    #         self.update(**dict(state='picking_in_progress'))

    #     if params['next_preparation'] != "":
    #         return self.registry.Wms.Sensee.Preparation.query().filter_by(
    #             code=params['next_preparation']).one_or_none()

    @classmethod
    def create(cls, **kwargs):
        """
        Creates the preparation and reservations
        :param properties:
        :return:
        """
        preparation = cls.insert(**kwargs)
        preparation.request_frame_reservation()
        req = preparation.request_lenses_reservation()
        req.reserve()
        return preparation
