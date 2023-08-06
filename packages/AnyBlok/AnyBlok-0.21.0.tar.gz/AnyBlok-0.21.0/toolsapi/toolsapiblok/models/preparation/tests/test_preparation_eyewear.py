from uuid import uuid1
from json import dumps
from unittest.mock import patch

from anyblok_bus.status import MessageStatus

from .test_preparation_base import TestPreparationBase


class TestPreparationEyewear(TestPreparationBase):

    def setUp(self):
        super(TestPreparationEyewear, self).setUp()
        # shorcuts
        self.Customer = self.registry.Customer
        self.Address = self.registry.Address
        self.VisionCard = self.registry.VisionCard
        self.Sale = self.registry.Sale
        self.Wms = self.registry.Wms
        self.PhysObj = self.Wms.PhysObj
        self.PhysObjType = self.Wms.PhysObj.Type
        self.Avatar = self.Wms.PhysObj.Avatar
        self.Operation = self.Wms.Operation
        self.Reservation = self.Wms.Reservation
        self.Request = self.Reservation.Request
        self.RequestItem = self.Reservation.RequestItem
        self.Sensee = self.Wms.Sensee
        self.Preparation = self.Sensee.Preparation
        self.npeyewear_gt = self.PhysObjType.query().filter_by(
            code="NP_EYEWEAR").one()
        self.tray_gt = self.PhysObjType.query().filter_by(
            code="TRAY").one()
        self.tray_rs_gt = self.PhysObjType.query().filter_by(
            code="TRAY/RL").one()
        self.tray_ls_gt = self.PhysObjType.query().filter_by(
            code="TRAY/LL").one()
        self.stock = self.PhysObj.query().filter_by(
            code="WH-KEHL-STOCK").one()
        self.se9090_feel_center_todo = self.PhysObj.query().filter_by(
            code="WH-KEHL_SE9090001_FEEL_CENTER_TODO").one()
        self.se9090_feel_center = self.PhysObj.query().filter_by(
            code="WH-KEHL_SE9090001_FEEL_CENTER_IN_PROGRESS").one()
        self.se9090_feel_center_done = self.PhysObj.query().filter_by(
            code="WH-KEHL_SE9090001_FEEL_CENTER_DONE").one()
        self.se9090_cut_todo = self.PhysObj.query().filter_by(
            code="WH-KEHL_SE9090001_CUT_TODO").one()
        self.se9090_cut = self.PhysObj.query().filter_by(
            code="WH-KEHL_SE9090001_CUT").one()
        self.se9090_cut_done = self.PhysObj.query().filter_by(
            code="WH-KEHL_SE9090001_CUT_DONE").one()
        self.mrblue_todo = self.PhysObj.query().filter_by(
            code="WH-KEHL_MRBLUE001_TODO").one()
        self.mrblue = self.PhysObj.query().filter_by(
            code="WH-KEHL_MRBLUE001_IN_PROGRESS").one()
        self.mrblue_done = self.PhysObj.query().filter_by(
            code="WH-KEHL_MRBLUE001_DONE").one()
        self.waiting_location = self.PhysObj.query().filter_by(
            code="WH-KEHL_ATELIER_ATTENTE").one()
        self.assembly_todo = self.PhysObj.query().filter_by(
            code="WH-KEHL_ATELIER_MONTAGE_TODO").one()
        self.assembly = self.PhysObj.query().filter_by(
            code="WH-KEHL_ATELIER_MONTAGE_INPROGRESS").one()
        self.quality_todo = self.PhysObj.query().filter_by(
            code="WH-KEHL_ATELIER_QUALITY_TODO").one()
        self.quality = self.PhysObj.query().filter_by(
            code="WH-KEHL_ATELIER_QUALITY_INPROGRESS").one()

    @staticmethod
    def get_preparation_data():
        return {
            'preparation_type': 'NP_EYEWEAR',
            'properties': {
                'preparation_data': {
                    'quantity': 1,
                    'reason': 'SO-TEST-00001',
                    'sale_channel_code': 'WEB',
                    'odoo_name': 'OF000000001',
                },
                'bom': {
                    'inputs': {
                        'frame_code': 'IAH01-NOIR-12',
                        'right_lens_code': 'SO-4-ARGF-11-3+000+000',
                        'left_lens_code': 'SO-4-ARGF-11-3+000+000',
                    }
                }
            }
        }

    def create_eyewear_preparation(self):
        data = self.get_preparation_data()
        inputs = self.get_preparation_inputs()

        self.quantities = {}
        for k, v in inputs.items():
            qty = self.quantities[v] if v in self.quantities.keys() else 0
            self.quantities[v] = qty + 1

        self.preparation = self.Preparation.create(**data)

        self.assertIsInstance(self.preparation,
                              self.Preparation.get_class_from_code(
                                  data["preparation_type"])
                              )
        req_query = self.Request.query().filter_by(
            purpose=['PREPARATION', self.preparation.code])
        self.assertEqual(req_query.count(), 1)

    def test_create_eyewear_preparation(self):
        self.create_eyewear_preparation()

    def test_create_preparation_by_bus(self):
        uuid = uuid1()
        data = self.get_preparation_data()
        message = dict(
            uuid=str(uuid),
            **data
        )
        with patch('anyblok_bus.bloks.bus.bus.Bus.publish'):
            self.Preparation.create_requested_preparation(body=dumps(message))

    def test_create_preparation_by_bus_message_already_exists(self):
        uuid = uuid1()
        data = self.get_preparation_data()
        message = dict(
            uuid=str(uuid),
            **data
        )
        with patch('anyblok_bus.bloks.bus.bus.Bus.publish'):
            self.assertEqual(self.Preparation.create_requested_preparation(body=dumps(message)),
                             MessageStatus.ACK)
            self.assertEqual(self.Preparation.create_requested_preparation(body=dumps(message)),
                             MessageStatus.ACK)

    def test_plan_arrival_tray_with_lenses_slots(self):
        self.create_eyewear_preparation()
        tray_avatar = self.preparation.plan_arrival_tray_with_lenses_slots()

        arrival_query = self.Operation.Arrival.query()
        self.assertEqual(
            arrival_query.filter_by(goods_type=self.tray_gt).count(),
            1)
        self.assertEqual(
            arrival_query.filter_by(goods_type=self.tray_rs_gt).count(),
            1)
        self.assertEqual(
            arrival_query.filter_by(goods_type=self.tray_ls_gt).count(),
            1)

        self.assertEqual(tray_avatar.state, "future")
        self.assertEqual(tray_avatar.location, self.stock)

        slot_avs = self.Avatar.query().filter_by(
            location=tray_avatar.obj).all()
        self.assertEqual(len(slot_avs), 2)
        self.assertEqual({av.obj.type for av in slot_avs}, {self.tray_rs_gt,
                                                            self.tray_ls_gt})

        self.assertEqual(self.preparation.get_tray(), tray_avatar.obj)
        self.assertEqual(
            {self.preparation.get_tray(gt.code) for gt in (self.tray_rs_gt,
                                                           self.tray_ls_gt)},
            {av.obj for av in slot_avs})

    def fill_tray(self, return_avatar=None):
        inputs = self.get_preparation_inputs()
        frame_gt = self.PhysObjType.query().filter_by(
            code=inputs["frame_code"]).one()
        arrival_av = self.plan_obj_arrival(gt=frame_gt)
        frame = arrival_av.obj
        frame_avatar = self.preparation.plan_move_frame_to_tray(frame=frame)
        if return_avatar == "frame":
            return frame_avatar

        right_lens_gt = self.PhysObjType.query().filter_by(
            code=inputs["right_lens_code"]).one()
        left_lens_gt = self.PhysObjType.query().filter_by(
            code=inputs["left_lens_code"]).one()
        arrival_av = self.plan_obj_arrival(gt=right_lens_gt)
        right_lens = arrival_av.obj
        arrival_av = self.plan_obj_arrival(gt=left_lens_gt)
        left_lens = arrival_av.obj
        lens_avatars = self.preparation.plan_move_lenses_to_tray_slots(
            right_lens=right_lens, left_lens=left_lens)
        if return_avatar == "lens":
            return lens_avatars

        return [frame_avatar] + lens_avatars

    def test_plan_move_frame_to_tray(self):
        self.create_eyewear_preparation()
        self.preparation.plan_arrival_tray_with_lenses_slots()

        frame_avatar = self.fill_tray(return_avatar="frame")

        tray = self.preparation.get_tray()
        self.assertEqual(frame_avatar.location, tray)

    def test_plan_move_lenses_to_tray_slots(self):
        self.create_eyewear_preparation()
        self.preparation.plan_arrival_tray_with_lenses_slots()

        lens_avatars = self.fill_tray(return_avatar="lens")

        self.assertEqual(
            {self.preparation.get_tray(gt.code) for gt in (self.tray_rs_gt,
                                                           self.tray_ls_gt)},
            {av.location for av in lens_avatars})

    def test_plan_move_tray_to_assembly_todo(self):
        self.create_eyewear_preparation()
        tray_avatar = self.preparation.plan_arrival_tray_with_lenses_slots()

        tray_avatar = self.preparation.plan_move_tray_to_assembly_todo(
            tray_avatar=tray_avatar)

        self.assertEqual(tray_avatar.location, self.assembly_todo)

    def test_plan_move_tray_to_assembly_workshop(self):
        self.create_eyewear_preparation()
        tray_avatar = self.preparation.plan_arrival_tray_with_lenses_slots()

        tray_avatar = self.preparation.plan_move_tray_to_assembly_workshop(
            tray_avatar=tray_avatar)

        self.assertEqual(tray_avatar.location, self.assembly)

    def test_compute_npeyewear_code(self):
        self.create_eyewear_preparation()
        inputs = self.get_preparation_inputs()
        code = self.preparation.compute_eyewear_code()

        self.assertEqual(
            inputs['frame_code'] + "_" + inputs['right_lens_code'],
            code)

    def test_plan_final_assembly_and_reserve_for_shipping(self):
        self.create_eyewear_preparation()
        self.preparation.plan_arrival_tray_with_lenses_slots()
        avatars = self.fill_tray()

        eyewear_av = self.preparation.plan_final_assembly()

        self.assertEqual(eyewear_av.location,
                         self.preparation.get_tray())
        self.assertEqual({av for av in avatars if av.dt_until is None}, set())

    def test_reserve_eyewear_for_shipping(self):
        self.create_eyewear_preparation()

        self.preparation.plan_arrival_tray_with_lenses_slots()
        self.fill_tray()

        self.preparation.plan_final_assembly()

        req = self.preparation.reserve_eyewear_for_shipping()
        self.assertEqual(req.reserved, True)

    def test_plan_move_tray_to_quality_todo(self):
        self.create_eyewear_preparation()
        tray_avatar = self.preparation.plan_arrival_tray_with_lenses_slots()
        tray_avatar = self.preparation.plan_move_tray_to_quality_todo(
            tray_avatar=tray_avatar)

        self.assertEqual(tray_avatar.location, self.quality_todo)

    def test_plan_move_tray_to_quality(self):
        self.create_eyewear_preparation()
        tray_avatar = self.preparation.plan_arrival_tray_with_lenses_slots()
        tray_avatar = self.preparation.plan_move_tray_to_quality(
            tray_avatar=tray_avatar)

        self.assertEqual(tray_avatar.location, self.quality)

    def test_plan_quality_observation(self):
        self.create_eyewear_preparation()
        self.preparation.plan_arrival_tray_with_lenses_slots()
        self.fill_tray()

        eyewear_av = self.preparation.plan_final_assembly()

        self.preparation.plan_quality_observation(
            eyewear_avatar=eyewear_av)

        observation = self.Operation.Observation.query().filter_by(
            reason=self.preparation.code).one_or_none()
        self.assertNotEqual(observation, None)
        self.assertEqual(observation.input, eyewear_av)
        self.assertEqual(observation.state, "planned")

    def test_plan_move_tray_to_waiting_location(self):
        self.create_eyewear_preparation()
        tray_avatar = self.preparation.plan_arrival_tray_with_lenses_slots()
        tray_avatar = self.preparation.plan_move_tray_to_waiting_location(
            tray_avatar=tray_avatar)

        self.assertEqual(tray_avatar.location, self.waiting_location)

    def create_many_eyewear_preparations(self, nb_preparations=1):
        data = self.get_preparation_data()

        preps_list = []
        for x in range(0, nb_preparations):
            prep = self.Preparation.create(**data)
            preps_list.append(prep)

        return preps_list

    def simulate_arrival_of_reserved_items(self, preparation):
        inputs = self.get_preparation_inputs()
        gts = {}
        for code in inputs.values():
            gt = self.PhysObjType.query().filter_by(code=code).one()
            gts[code] = gt

        for req in preparation.requests:
            req_items = self.RequestItem.query().filter_by(request=req).all()
            for item in req_items:
                arrival_gt = gts.get(item.goods_type.code)
                arrival_location = arrival_gt.get_default_storage_location()
                self.Operation.Arrival.create(
                    goods_type=arrival_gt,
                    location=arrival_location,
                    state='done')

    @staticmethod
    def reserve_preparation_requests(preparations_list):
        for preparation in preparations_list:
            for request in preparation.requests:
                request.reserve()

    def test_plan_many_eyewear(self):
        nb_preparations = 20
        preps_list = self.create_many_eyewear_preparations(nb_preparations)
        # Trying to reserve the obj before having some in stock
        self.reserve_preparation_requests(preparations_list=preps_list)

        # No reservation is 'reserved'
        self.assertEqual(self.Request.query().filter_by(reserved=True,
                                                        planned=False).count(),
                         0)
        # Simulating arrival of obj for the reservation to be reserved
        for prep in preps_list:
            self.simulate_arrival_of_reserved_items(prep)
        # Now the stock have enough obj to please all the reservations
        self.reserve_preparation_requests(preparations_list=preps_list)
        # The reservations are now 'reserved'
        self.assertEqual(
            self.Request.query().filter(
                self.Request.purpose.comparator.contains(["PREPARATION"])
            ).filter_by(
                reserved=True,
                planned=False).count(),
            nb_preparations)

        # Claim reserved items and plan the operations for every preparation
        for x in range(0, nb_preparations):
            self.Preparation.plan_preparation()

        self.assertEqual(
            self.Request.query().filter(
                self.Request.purpose.comparator.contains(["PREPARATION"])
            ).filter_by(
                reserved=True,
                planned=True).count(),
            nb_preparations)
        self.assertEqual(
            self.Request.query().filter(
                self.Request.purpose.comparator.contains(["SHIPPING"])
            ).filter_by(
                reserved=True,
                planned=False).count(),
            nb_preparations)

    def test_plan_many_eyewear_with_partial_stock(self):
        nb_preparations = 20
        preps_list = self.create_many_eyewear_preparations(nb_preparations)
        # Trying to reserve the obj before having some in stock
        self.reserve_preparation_requests(preparations_list=preps_list)

        # No reservation is 'reserved'
        self.assertEqual(self.Request.query().filter_by(reserved=True,
                                                        planned=False).count(),
                         0)

        # Simulating arrival of obj for the reservation to be reserved
        nb_reservable = 5
        for i in range(0, nb_reservable):
            self.simulate_arrival_of_reserved_items(preps_list[i])

        # Now the stock have enough obj to please {nb_reservable} preparations
        self.reserve_preparation_requests(preparations_list=preps_list)

        # The reservations are now 'reserved'
        self.assertEqual(
            self.Request.query().filter(
                self.Request.purpose.comparator.contains(["PREPARATION"])
            ).filter_by(
                reserved=True,
                planned=False).count(),
            nb_reservable)

        # Claim reserved items and plan the operations for every preparation
        for x in range(0, nb_preparations):
            self.Preparation.plan_preparation()

        self.assertEqual(
            self.Request.query().filter(
                self.Request.purpose.comparator.contains(["PREPARATION"])
            ).filter_by(
                reserved=True,
                planned=True).count(),
            nb_reservable)
        self.assertEqual(
            self.Request.query().filter(
                self.Request.purpose.comparator.contains(["SHIPPING"])
            ).filter_by(
                reserved=True,
                planned=False).count(),
            nb_reservable)
