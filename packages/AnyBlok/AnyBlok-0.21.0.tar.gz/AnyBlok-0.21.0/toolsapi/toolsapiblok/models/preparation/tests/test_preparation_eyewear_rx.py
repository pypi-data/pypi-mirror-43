from .test_preparation_eyewear import TestPreparationEyewear


class TestPreparationEyewearRx(TestPreparationEyewear):

    @staticmethod
    def get_preparation_data():
        return {
            'preparation_type': 'PROGRESSIVE_GLASSES',
            'properties': {
                'preparation_data': {
                    'quantity': 1,
                    'reason': 'BC2018SHO-PAR-RAMEQWOXK',
                    'sale_channel_code': 'WEB',
                    'odoo_name': u'OF0000023924',
                },
                'bom': {
                    'inputs': {
                        'frame_code': 'AH16-ECAILLE2-32',
                        'right_lens_code': 'SPG-ORGA-160-G11-RX-L',
                        'left_lens_code': 'SPG-ORGA-160-G11-RX-L',
                    },
                },
            }
        }

    def test_plan_lenses_arrival_and_reserve(self):
        self.create_eyewear_preparation()
        inputs = self.get_preparation_inputs()

        req = self.preparation.get_reservation_request(purpose=['PREPARATION',
                                                       self.preparation.code])
        self.assertEqual(self.Reservation.query().count(), 2)
        self.assertFalse(req.reserved)

        frame_gt = self.PhysObjType.query().filter_by(
            code=inputs['frame_code']).one()
        frame_location = frame_gt.get_default_storage_location()
        self.Operation.Arrival.create(
            goods_type=frame_gt,
            location=frame_location,
            state='done')

        self.assertTrue(req.reserve())
        self.assertEqual(self.Reservation.query().count(), 3)

    def test_plan_mrblue_operations(self):
        self.create_eyewear_preparation()

        tray_avatar = self.preparation.plan_arrival_tray_with_lenses_slots()

        avatars = self.fill_tray()
        frame = avatars[0].obj

        tray_avatar = self.preparation.plan_mrblue_operations(
            tray_avatar=tray_avatar,
            frame_avatar=avatars[0],
        )

        # assert tray avatars exists in se9090 locations
        tray = tray_avatar.obj
        tray_avs = self.Avatar.query().filter_by(obj=tray).all()
        self.assertEqual({av.location for av in tray_avs},
                         {self.stock, self.mrblue_todo,
                          self.mrblue, self.mrblue_done})
        # assert 1 observation for the frame and 2 for each lens
        observations = self.Operation.Observation.query().filter_by(
            reason=self.preparation.code).all()
        frame_observations = [
            op for op in observations if op.input.obj == frame
        ]
        self.assertEqual(len(frame_observations), 1)
