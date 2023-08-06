import json
from uuid import uuid1

from anyblok_wms_base.testing import WmsTestCase
from anyblok_bus.status import MessageStatus


class TestOdoo8SyncFabPacking(WmsTestCase):
    """Tests for the Operations that are created as counterparts of Odoo side
    """

    def setUp(self):
        super().setUp()
        self.Sync = self.registry.Bus.Odoo8Sync.FabPacking
        self.Arrival = self.Operation.Arrival
        self.Departure = self.Operation.Departure
        POT = self.POT = self.PhysObj.Type

        self.assembled_type = POT.query().filter_by(
            code='UNIFOCAL_GLASSES').one()

        self.frame_code = 'IAH01-NOIR-12'
        self.frame_type = POT.query().filter_by(code=self.frame_code).one()
        self.lens1_code = 'SO-4-ARGF-11-3+000+000'
        self.lens1_type = POT.query().filter_by(code=self.lens1_code).one()
        self.lens2_code = 'SO-3-VERS-11-3+000+000'
        self.lens2_type = POT.query().filter_by(code=self.lens2_code).one()

        self.loc_codes = ('KEHL_A_02_03_01',
                          'KEHL_B_04_03_01',
                          'KEHL_C_02_01_01',
                          'KEHL_D_02_03_01')
        self.locs = [self.PhysObj.query().filter_by(code=code).one()
                     for code in self.loc_codes]

    def test_assembly_all_ok(self):
        loc_codes, locs = self.loc_codes, self.locs
        self.Arrival.create(physobj_type=self.frame_type,
                            physobj_code='monty-python',
                            location=locs[0],
                            dt_execution=self.dt_test1,
                            state='done')
        self.Arrival.create(physobj_type=self.lens1_type,
                            physobj_code='monty-python',
                            location=locs[1],
                            dt_execution=self.dt_test1,
                            state='done')
        self.Arrival.create(physobj_type=self.lens2_type,
                            physobj_code='monty-python',
                            location=locs[2],
                            dt_execution=self.dt_test1,
                            state='done')

        consumed = (dict(type_code=self.frame_code,
                         location_code=loc_codes[0],
                         phobj_code='monty-python'),
                    dict(type_code=self.lens1_code,
                         location_code=loc_codes[1],
                         phobj_code='monty-python'),
                    dict(type_code=self.lens2_code,
                         location_code=loc_codes[2],
                         phobj_code='monty-python'))
        produced = dict(type_code=self.assembled_type.code,
                        phobj_code='monty-python',
                        props=dict(foo=3),
                        location_code=loc_codes[3])
        ass, missing = self.Sync.odoo_final_assembly_done(
            consumed, produced,
            dt_execution=self.dt_test2,
            reason='OF1234')

        out_av = self.assert_singleton(ass.outcomes)
        self.assertEqual(out_av.location, locs[3])
        self.assertEqual(out_av.state, 'present')
        phobj = out_av.obj
        self.assertEqual(phobj.code, 'monty-python')
        self.assertEqual(phobj.type, self.assembled_type)
        self.assertEqual(phobj.get_property('foo'), 3)

        self.assertEqual(len(missing), 0)
        for loc in locs[:3]:
            self.assert_quantity(0, goods_type=None, location=loc)
            self.assert_quantity(1, goods_type=None, location=loc,
                                 additional_states=['past'],
                                 at_datetime=self.dt_test1)

    def test_assembly_by_bus(self):
        loc_codes, locs = self.loc_codes, self.locs
        self.Arrival.create(physobj_type=self.frame_type,
                            physobj_code='monty-python',
                            location=locs[0],
                            dt_execution=self.dt_test1,
                            state='done')
        self.Arrival.create(physobj_type=self.lens1_type,
                            physobj_code='monty-python',
                            location=locs[1],
                            dt_execution=self.dt_test1,
                            state='done')
        self.Arrival.create(physobj_type=self.lens2_type,
                            physobj_code='monty-python',
                            location=locs[2],
                            dt_execution=self.dt_test1,
                            state='done')
        msg = dict(
            msg_type=self.Sync.MSG_FINAL_ASSEMBLY_DONE,
            reason='OF1234',
            inputs=[dict(odoo_product_code=self.frame_code,
                         location_code=loc_codes[0],
                         odoo_production_lot_name='monty-python'),
                    dict(odoo_product_code=self.lens1_code,
                         location_code=loc_codes[1],
                         odoo_production_lot_name='monty-python'),
                    dict(odoo_product_code=self.lens2_code,
                         location_code=loc_codes[2],
                         odoo_production_lot_name='monty-python')],
            outcome=dict(odoo_product_code=self.assembled_type.code,
                         location_code=loc_codes[3]))
        self.assertEqual(self.Sync.msg_fab_packing(json.dumps(msg)),
                         MessageStatus.ACK)

        phobj = self.single_result(self.PhysObj.query().filter_by(
            type=self.assembled_type))
        avatar = self.single_result(self.PhysObj.Avatar.query().filter_by(
            obj=phobj))
        assembly = avatar.outcome_of
        self.assertIsInstance(assembly, self.Operation.Assembly)
        self.assertEqual(assembly.state, 'done')
        self.assertEqual(avatar.state, 'present')
        self.assertEqual(assembly.reason, 'OF1234')

    def test_assembly_by_bus_multi_quantity(self):
        loc_codes, locs = self.loc_codes, self.locs
        quantity = 5
        for x in range(quantity):
            self.Arrival.create(physobj_type=self.frame_type,
                                physobj_code='monty-python',
                                location=locs[0],
                                dt_execution=self.dt_test1,
                                state='done')
            self.Arrival.create(physobj_type=self.lens1_type,
                                physobj_code='monty-python',
                                location=locs[1],
                                dt_execution=self.dt_test1,
                                state='done')
            self.Arrival.create(physobj_type=self.lens2_type,
                                physobj_code='monty-python',
                                location=locs[2],
                                dt_execution=self.dt_test1,
                                state='done')
        msg = dict(
            msg_type=self.Sync.MSG_FINAL_ASSEMBLY_DONE,
            reason='OF1234',
            quantity=quantity,
            inputs=[dict(odoo_product_code=self.frame_code,
                         location_code=loc_codes[0],
                         odoo_production_lot_name='monty-python'),
                    dict(odoo_product_code=self.lens1_code,
                         location_code=loc_codes[1],
                         odoo_production_lot_name='monty-python'),
                    dict(odoo_product_code=self.lens2_code,
                         location_code=loc_codes[2],
                         odoo_production_lot_name='monty-python')],
            outcome=dict(odoo_product_code=self.assembled_type.code,
                         location_code=loc_codes[3]))
        self.assertEqual(self.Sync.msg_fab_packing(json.dumps(msg)),
                         MessageStatus.ACK)

        self.assertEqual(
            self.PhysObj.query().filter_by(type=self.assembled_type).count(),
            quantity
        )

    def test_assembly_by_bus_missing_input(self):

        loc_codes, locs = self.loc_codes, self.locs
        self.Arrival.create(physobj_type=self.frame_type,
                            physobj_code='monty-python',
                            location=locs[0],
                            dt_execution=self.dt_test1,
                            state='done')
        self.Arrival.create(physobj_type=self.lens1_type,
                            physobj_code='monty-python',
                            location=locs[1],
                            dt_execution=self.dt_test1,
                            state='done')
        msg = dict(
            msg_type=self.Sync.MSG_FINAL_ASSEMBLY_DONE,
            reason='OF1234',
            inputs=[dict(odoo_product_code=self.frame_code,
                         location_code=loc_codes[0],
                         odoo_production_lot_name='monty-python'),
                    dict(odoo_product_code=self.lens1_code,
                         location_code=loc_codes[1],
                         odoo_production_lot_name='monty-python'),
                    dict(odoo_product_code=self.lens2_code,
                         location_code=loc_codes[2],
                         odoo_production_lot_name='monty-python')],
            outcome=dict(odoo_product_code=self.assembled_type.code,
                         location_code=loc_codes[3]))

        with self.assertRaises(LookupError) as arc:
            self.Sync.msg_fab_packing(json.dumps(msg))

        self.assertEqual(arc.exception.args[0], "msg_final_assembly_done")
        self.assertEqual(
            arc.exception.args[1],
            "Some inputs not found. Assembly not created.")

        missing_input = arc.exception.args[2][0]
        self.assertEqual(missing_input[0], dict(type_code=self.lens2_code,
                                                phobj_code='monty-python',
                                                location_code=loc_codes[2]))
        self.assertIsInstance(missing_input[1], LookupError)
        self.assertEqual(missing_input[1].args, ('avatar', 'nowhere'))

    def test_assembly_missing_input(self):
        """An input is missing, but its type and location exist"""
        loc_codes, locs = self.loc_codes, self.locs
        self.Arrival.create(physobj_type=self.frame_type,
                            location=locs[0],
                            physobj_code='monty-python',
                            dt_execution=self.dt_test1,
                            state='done')
        self.Arrival.create(physobj_type=self.lens1_type,
                            physobj_code='monty-python',
                            location=locs[1],
                            dt_execution=self.dt_test1,
                            state='done')

        consumed = (dict(type_code=self.frame_code,
                         phobj_code='monty-python',
                         location_code=loc_codes[0]),
                    dict(type_code=self.lens1_code,
                         phobj_code='monty-python',
                         location_code=loc_codes[1]),
                    dict(type_code=self.lens1_code,
                         phobj_code='monty-python',
                         location_code=loc_codes[2]))
        produced = dict(type_code=self.assembled_type.code,
                        phobj_code='monty-python',
                        location_code=loc_codes[3])
        ass, missing = self.Sync.odoo_final_assembly_done(
            consumed, produced,
            reason='OF1234')

        out_av = self.assert_singleton(ass.outcomes)
        self.assertEqual(out_av.location, locs[3])
        self.assertEqual(out_av.state, 'present')
        phobj = out_av.obj
        self.assertEqual(phobj.code, 'monty-python')
        self.assertEqual(phobj.type, self.assembled_type)

        miss_report = self.assert_singleton(missing)
        self.assertEqual(miss_report[0],
                         dict(type_code=self.lens1_code,
                              phobj_code='monty-python',
                              location_code=loc_codes[2]))
        # can't compare LookupErrors !
        self.assertIsInstance(miss_report[1], LookupError)
        self.assertEqual(miss_report[1].args, ('avatar', 'nowhere'))

        for loc in locs[:2]:
            self.assert_quantity(0, goods_type=None, location=loc)
            self.assert_quantity(1, goods_type=None, location=loc,
                                 additional_states=['past'],
                                 at_datetime=self.dt_test1)

    def test_assembly_missing_input_type(self):
        """An input has unknown type but its location exists"""
        loc_codes, locs = self.loc_codes, self.locs
        self.Arrival.create(physobj_type=self.frame_type,
                            physobj_code='monty-python',
                            location=locs[0],
                            dt_execution=self.dt_test1,
                            state='done')
        self.Arrival.create(physobj_type=self.lens1_type,
                            physobj_code='monty-python',
                            location=locs[1],
                            dt_execution=self.dt_test1,
                            state='done')

        consumed = (dict(type_code=self.frame_code,
                         phobj_code='monty-python',
                         location_code=loc_codes[0]),
                    dict(type_code=self.lens1_code,
                         phobj_code='monty-python',
                         location_code=loc_codes[1]),
                    dict(type_code="No this doesn't exist",
                         phobj_code='monty-python',
                         location_code=loc_codes[2]))
        produced = dict(type_code=self.assembled_type.code,
                        phobj_code='monty-python',
                        location_code=loc_codes[3])
        ass, missing = self.Sync.odoo_final_assembly_done(
            consumed, produced,
            reason='OF1234')

        out_av = self.assert_singleton(ass.outcomes)
        self.assertEqual(out_av.location, locs[3])
        self.assertEqual(out_av.state, 'present')
        phobj = out_av.obj
        self.assertEqual(phobj.code, 'monty-python')
        self.assertEqual(phobj.type, self.assembled_type)

        miss_report = self.assert_singleton(missing)
        self.assert_singleton(missing)
        self.assertEqual(miss_report[0],
                         dict(type_code="No this doesn't exist",
                              phobj_code='monty-python',
                              location_code=loc_codes[2]))
        # can't compare LookupErrors !
        self.assertIsInstance(miss_report[1], LookupError)
        self.assertEqual(miss_report[1].args,
                         ('type', "No this doesn't exist"))

        for loc in locs[:2]:
            self.assert_quantity(0, goods_type=None, location=loc)
            self.assert_quantity(1, goods_type=None, location=loc,
                                 additional_states=['past'],
                                 at_datetime=self.dt_test1)

    def test_assembly_missing_input_location(self):
        """An input has unknown location but its type exists"""
        loc_codes, locs = self.loc_codes, self.locs
        self.Arrival.create(physobj_type=self.frame_type,
                            physobj_code='monty-python',
                            location=locs[0],
                            dt_execution=self.dt_test1,
                            state='done')
        self.Arrival.create(physobj_type=self.lens1_type,
                            physobj_code='monty-python',
                            location=locs[1],
                            dt_execution=self.dt_test1,
                            state='done')

        consumed = (dict(type_code=self.frame_code,
                         phobj_code='monty-python',
                         location_code=loc_codes[0]),
                    dict(type_code=self.lens1_code,
                         phobj_code='monty-python',
                         location_code=loc_codes[1]),
                    dict(type_code=self.lens2_code,
                         phobj_code='monty-python',
                         location_code="Nowhere"))
        produced = dict(type_code=self.assembled_type.code,
                        phobj_code='monty-python',
                        location_code=loc_codes[3])
        ass, missing = self.Sync.odoo_final_assembly_done(
            consumed, produced,
            reason='OF1234')

        out_av = self.assert_singleton(ass.outcomes)
        self.assertEqual(out_av.location, locs[3])
        self.assertEqual(out_av.state, 'present')
        phobj = out_av.obj
        self.assertEqual(phobj.code, 'monty-python')
        self.assertEqual(phobj.type, self.assembled_type)

        miss_report = self.assert_singleton(missing)
        self.assertEqual(miss_report[0],
                         dict(type_code=self.lens2_code,
                              phobj_code='monty-python',
                              location_code="Nowhere"))
        # can't compare LookupErrors !
        self.assertIsInstance(miss_report[1], LookupError)
        self.assertEqual(miss_report[1].args,
                         ('location', "Nowhere"))

        for loc in locs[:2]:
            self.assert_quantity(0, goods_type=None, location=loc)
            self.assert_quantity(1, goods_type=None, location=loc,
                                 additional_states=['past'],
                                 at_datetime=self.dt_test1)

    def test_assembly_missing_outcome_type(self):
        """Failure of Assembly creation due to unknown outcome type"""
        produced = dict(type_code="FANTAISISTE",
                        phobj_code='monty-python',
                        location_code=self.loc_codes[3])

        with self.assertRaises(LookupError) as arc:
            self.Sync.odoo_final_assembly_done([], produced)

        self.assertEqual(arc.exception.args, ('outcome_type', 'FANTAISISTE'))

    def test_assembly_missing_outcome_location(self):
        """Failure of Assembly creation due to unknown outcome location"""
        produced = dict(type_code=self.assembled_type.code,
                        phobj_code='monty-python',
                        location_code='NOWHERE')

        with self.assertRaises(LookupError) as arc:
            self.Sync.odoo_final_assembly_done([], produced)

        self.assertEqual(arc.exception.args, ('outcome_location', 'NOWHERE'))

    def test_departure_type_only(self):
        loc = self.locs[0]
        arrival = self.Arrival.create(physobj_type=self.assembled_type,
                                      location=loc,
                                      dt_execution=self.dt_test1,
                                      state='done')
        # single outcome mixin not available yet
        glasses_av = next(iter(arrival.outcomes))

        self.Sync.odoo_departure(self.assembled_type.code,
                                 location_code=self.loc_codes[0])
        self.assertEqual(glasses_av.state, 'past')

        dep = self.assert_singleton(arrival.followers)
        self.assertIsInstance(dep, self.Departure)
        self.assertEqual(dep.state, 'done')
        self.assertEqual(dep.input, glasses_av)

        self.assert_quantity(0, goods_type=self.assembled_type, location=loc)
        self.assert_quantity(1, goods_type=self.assembled_type, location=loc,
                             additional_states=['past'],
                             at_datetime=self.dt_test1)

    def test_departure_type_and_code(self):
        loc = self.locs[0]
        for code in ("A41", "A42"):
            self.Arrival.create(physobj_type=self.assembled_type,
                                physobj_code=code,
                                location=loc,
                                dt_execution=self.dt_test1,
                                state='done')

        self.Sync.odoo_departure(self.assembled_type.code,
                                 location_code=self.loc_codes[0],
                                 physobj_code="A42",
                                 dt_execution=self.dt_test2)

        # browsing history in a different way that in test_departure_type_only
        # so that we have better testing of actual consistency
        dep = self.single_result(self.Departure.query())
        self.assertEqual(dep.state, 'done')
        self.assertEqual(dep.dt_execution, self.dt_test2)
        dep_av = dep.input
        self.assertEqual(dep_av.obj.code, "A42")

        self.assert_quantity(1, goods_type=self.assembled_type, location=loc)
        self.assert_quantity(2, goods_type=self.assembled_type, location=loc,
                             additional_states=['past'],
                             at_datetime=self.dt_test1)

        # normally these would be redundant, but in these sync primitives
        # we have a tendency to go low-level, so let's do these assertions
        # that are not related to the lookup by physobj code
        self.assertEqual(dep_av.state, 'past')
        self.assertEqual(dep_av.dt_until, self.dt_test2)
        self.assert_singleton(dep.follows, value=dep_av.outcome_of)

    def test_departure_missing(self):
        """Failure of Assembly creation due to unknown outcome location"""
        with self.assertRaises(LookupError) as arc:
            self.Sync.odoo_departure(self.assembled_type.code,
                                     location_code=self.loc_codes[0])
        self.assertEqual(arc.exception.args, ('avatar', 'nowhere'))

    def test_departure_by_bus_default_qty_one(self):
        loc = self.locs[0]
        arrival = self.Arrival.create(physobj_type=self.assembled_type,
                                      location=loc,
                                      dt_execution=self.dt_test1,
                                      state='done')
        # single outcome mixin not available yet
        glasses_av = next(iter(arrival.outcomes))

        msg = dict(
            uuid=str(uuid1()),
            msg_type=self.Sync.MSG_DEPARTURE,
            reason='SO-456',
            odoo_product_code=self.assembled_type.code,
            location_code=loc.code)

        self.assertEqual(self.Sync.msg_fab_packing(json.dumps(msg)),
                         MessageStatus.ACK)

        self.assertEqual(glasses_av.state, 'past')

        dep = self.assert_singleton(arrival.followers)
        self.assertIsInstance(dep, self.Departure)
        self.assertEqual(dep.state, 'done')
        self.assertEqual(dep.input, glasses_av)

        self.assert_quantity(0, goods_type=self.assembled_type, location=loc)
        self.assert_quantity(1, goods_type=self.assembled_type, location=loc,
                             additional_states=['past'],
                             at_datetime=self.dt_test1)

    def test_departure_by_bus_several(self):
        loc = self.locs[0]
        for i in range(2):
            self.Arrival.create(physobj_type=self.assembled_type,
                                location=loc,
                                dt_execution=self.dt_test1,
                                state='done')

        msg = dict(
            uuid=str(uuid1()),
            msg_type=self.Sync.MSG_DEPARTURE,
            reason='SO-456',  # TODO check with jssuzanne UUID ?
            quantity=2,
            odoo_product_code=self.assembled_type.code,
            location_code=loc.code)

        self.assertEqual(self.Sync.msg_fab_packing(json.dumps(msg)),
                         MessageStatus.ACK)

        self.assert_quantity(0, goods_type=self.assembled_type, location=loc)
        self.assert_quantity(2, goods_type=self.assembled_type, location=loc,
                             additional_states=['past'],
                             at_datetime=self.dt_test1)
