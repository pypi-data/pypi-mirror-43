from .test_preparation_eyewear import TestPreparationEyewear


class TestPreparationEyewearStocked(TestPreparationEyewear):

    def test_plan_se9090_operations(self):
        self.create_eyewear_preparation()
        tray_avatar = self.preparation.plan_arrival_tray_with_lenses_slots()

        avatars = self.fill_tray()
        frame = avatars[0].obj
        right_lens = avatars[1].obj
        left_lens = avatars[2].obj

        tray_avatar = self.preparation.plan_se9090_operations(
            tray_avatar=tray_avatar,
            frame_avatar=avatars[0],
            right_lens_avatar=avatars[1],
            left_lens_avatar=avatars[2]
        )

        # assert tray avatars exists in se9090 locations
        tray = tray_avatar.obj
        tray_avs = self.Avatar.query().filter_by(obj=tray).all()
        self.assertEqual({av.location for av in tray_avs},
                         {self.stock, self.se9090_feel_center_todo,
                          self.se9090_feel_center, self.se9090_feel_center_done,
                          self.se9090_cut_todo, self.se9090_cut,
                          self.se9090_cut_done})
        # assert 1 observation for the frame and 2 for each lens
        observations = self.Operation.Observation.query().filter_by(
            reason=self.preparation.code).all()
        frame_observations = [
            op for op in observations if op.input.obj == frame
        ]
        self.assertEqual(len(frame_observations), 1)
        right_lens_observations = [
            op for op in observations if op.input.obj == right_lens
        ]
        self.assertEqual(len(right_lens_observations), 2)
        left_lens_observations = [
            op for op in observations if op.input.obj == left_lens
        ]
        self.assertEqual(len(left_lens_observations), 2)
