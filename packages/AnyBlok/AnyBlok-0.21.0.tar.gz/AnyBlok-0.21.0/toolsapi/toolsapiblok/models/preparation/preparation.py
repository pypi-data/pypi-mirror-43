import os
from datetime import datetime

from anyblok import Declarations
from anyblok.blok import BlokManager
from anyblok.column import Selection, Sequence, String
from anyblok.relationship import Many2Many
from anyblok_postgres.column import Jsonb
from logging import getLogger

from sqlalchemy import or_

from anyblok_bus.status import MessageStatus
from anyblok_bus import bus_consumer
from bus_schema.preparation import (
    PreparationSchema, PreparationOpticalSchema, PreparationStateSchema)
from json import dumps


logger = getLogger(__name__)

Model = Declarations.Model
Mixin = Declarations.Mixin
register = Declarations.register


@register(Model.Wms)
class Sensee:
    """Namespace for Sensee's Wms specification
    """


class PreparationSchemaWrapper:

    schemas = dict(
        UNIFOCAL_GLASSES=PreparationOpticalSchema,
        PROGRESSIVE_GLASSES=PreparationOpticalSchema,
        NP_EYEWEAR=PreparationOpticalSchema,
        FRAME_ONLY=PreparationSchema,
        LENS_ONLY=PreparationOpticalSchema,
        HOME_TRIAL_FRAMES=PreparationSchema,
        SIMPLE=PreparationSchema,
    )

    def __init__(self):
        self.context = dict()

    def load(self, message):
        preparation_type = message.get('preparation_type')
        schema = self.schemas.get(preparation_type)(context=self.context)
        return schema.load(message)


@register(Model.Wms.Sensee)
class Preparation(Mixin.UuidColumn, Mixin.TrackModel):
    """Namespace for Preparation related models and transversal methods.
    """
    PREPARATION_TYPE = None

    code = Sequence(unique=True, formater="P{seq:010d}")
    preparation_type = Selection(selections='get_preparation_types', nullable=False)
    state = String(default='todo', nullable=False)
    properties = Jsonb(label="properties")

    operations = Many2Many(model=Model.Wms.Operation)

    # vision card
    # photos

    def __str__(self):
        return ('{self.code}').format(self=self)

    def __repr__(self):
        msg = ('<Sensee.Preparation.{self.preparation_type}: {self.code}>')
        return msg.format(self=self)

    @classmethod
    def define_mapper_args(cls):
        mapper_args = super(Preparation, cls).define_mapper_args()
        if cls.__registry_name__ == 'Model.Wms.Sensee.Preparation':
            mapper_args.update({'polymorphic_on': cls.preparation_type})

        mapper_args.update({'polymorphic_identity': cls.PREPARATION_TYPE})
        return mapper_args

    @classmethod
    def query(cls, *args, **kwargs):
        query = super(Preparation, cls).query(*args, **kwargs)
        if cls.__registry_name__.startswith('Model.Wms.Sensee.Preparation.'):
            query = query.filter(cls.preparation_type == cls.PREPARATION_TYPE)

        return query

    @classmethod
    def get_preparation_types(cls):
        return dict()

    @classmethod
    def get_class_from_code(cls, code):
        Preparation = cls.registry.Wms.Sensee.Preparation
        mapping = {
            'UNIFOCAL_GLASSES': Preparation.UnifocalGlasses,
            'PROGRESSIVE_GLASSES': Preparation.ProgressiveGlasses,
            'NP_EYEWEAR': Preparation.NpEyewear,
            'FRAME_ONLY': Preparation.FrameOnly,
            'LENS_ONLY': Preparation.LensOnly,
            'HOME_TRIAL_FRAMES': Preparation.HomeTrial,
            'SIMPLE': Preparation.Simple,
        }
        specific_class = mapping.get(code)
        if specific_class is None:
            raise Exception("Preparation type %s unknown" % code)
        return specific_class

    @bus_consumer(queue_name='kehl_create_requested_preparation',
                  schema=PreparationSchemaWrapper())
    def create_requested_preparation(cls, body=None):
        if cls.query().filter_by(uuid=body['uuid']).count():
            # message already exist
            return MessageStatus.ACK

        preparation = cls.create(**body)
        preparation.push_status_in_bus()
        return MessageStatus.ACK

    def push_status_in_bus(self):
        message = dict(
            uuid=str(self.uuid),
            code=self.code,
            state=self.state,
        )

        validator = PreparationStateSchema()
        error = validator.validate(message)
        if error:
            self.registry.rollback()
            raise Exception(
                "Invalid message to send with %r: %r" % (message, error))

        self.registry.Bus.publish(
            'tools_kehl_sensee_exchange',
            'erp_sensee.v1.preparation_state',
            dumps(message).encode('utf-8'),
            "application/json"
        )

    @classmethod
    def create(cls, **kwargs):
        if cls.__registry_name__ != 'Model.Wms.Sensee.Preparation':
            raise Exception("create method is not callable from %s" %
                            cls.__registry_name__)
        specific = cls.get_class_from_code(kwargs.get('preparation_type'))
        return specific.create(**kwargs)

    @classmethod
    def plan_preparation(cls, **kwargs):
        """ Take on reservation request, claim reservation items
            and plan the operations
        :return:
        """
        Reservation = cls.registry.Wms.Reservation
        Request = Reservation.Request
        RequestItem = Reservation.RequestItem
        Preparation = cls.registry.Wms.Sensee.Preparation
        with Request.claim_reservations(planned=False, **kwargs) as req_id:
            if req_id is None:
                return False
            req = Request.query().get(req_id)
            items = Reservation.query().join(
                Reservation.request_item).filter(RequestItem.request ==
                                                 req).all()
            if not items:
                return False

            if req.purpose[0] == 'PREPARATION':
                preparation = Preparation.query().filter_by(
                                                    code=req.purpose[1]).one()
                preparation.plan_one(items)
                req.planned = True

            return True

    @classmethod
    def print_tray_labels(cls, labels_type):
        """
        TODO: Add the possibility to pass specific preparations ids
        Creates the tray labels document with the preparations ready
        :param labels_type:
        :return:
        """
        if labels_type:
            Preparation = cls.registry.Wms.Sensee.Preparation
            template = cls.registry.Attachment.Template.query().filter_by(
                name="tray_labels").one()
            preparations = Preparation.query().filter_by(state='todo').all()
            uuids = [str(elem.uuid) for elem in preparations]
            document = cls.registry.Attachment.Document.insert(
                template=template,
                data={'uuids': uuids},
            )
            return document.uuid

    @classmethod
    def get_tray_config(cls):
        """
        Returns the PhysObj.Type TRAY configuration dict
        :return:
        """
        return dict(
            label="Tray",
            code="TRAY",
            behaviours=dict(
                container=dict(),
                default_storage_locations=["WH-KEHL-STOCK"],
            )
        )

    def get_reservation_request(self, **kwargs):
        """
        creates a reservation request
        :param purpose:
        :return:
        """
        Reservation = self.registry.Wms.Reservation
        Request = Reservation.Request
        req = Request.query().filter_by(preparation=self,
                                        purpose=kwargs['purpose']).one_or_none()
        if req is None:
            req = Request.insert(preparation=self, **kwargs)
        return req

    def get_input_type(self, _input):
        """
        return the PhysObj.Type for an input key (ex: frame_code)
        :param _input:
        :return:
        """
        PhysObjType = self.registry.Wms.PhysObj.Type
        inputs = self.properties.get('bom').get('inputs')
        return PhysObjType.query().filter_by(code=inputs.get(_input)).one()

    def request_frame_reservation(self):
        """
        reserves the frame
        :return:
        """
        Reservation = self.registry.Wms.Reservation
        RequestItem = Reservation.RequestItem

        req = self.get_reservation_request(purpose=['PREPARATION', self.code])
        gt = self.get_input_type('frame_code')
        RequestItem.insert(
            goods_type=gt,
            quantity=1,
            request=req,
        )
        return req

    def request_lenses_reservation(self):
        """
        reserves the lenses
        :return:
        """
        Reservation = self.registry.Wms.Reservation
        RequestItem = Reservation.RequestItem

        req = self.get_reservation_request(purpose=['PREPARATION', self.code])
        keys = ['right_lens_code', 'left_lens_code']
        for key in keys:
            gt = self.get_input_type(key)
            RequestItem.insert(
                goods_type=gt,
                quantity=1,
                request=req,
            )
        return req

    def plan_arrival_tray_with_lenses_slots(self):
        """
        plans to create the labeled TRAY with two slots TRAY/RL and TRAY/LL
        :return:
        """
        stock = self.registry.Wms.PhysObj.query().filter_by(
            code="WH-KEHL-STOCK").one()

        Arrival = self.registry.Wms.Operation.Arrival
        PhysObj = self.registry.Wms.PhysObj
        op = Arrival.create(
            reason=self.code,
            goods_type=PhysObj.Type.query().filter_by(code="TRAY").one(),
            goods_code=self.code,
            location=stock,
            state="planned",
            dt_execution=datetime.now()
        )
        self.operations.append(op)

        tray_avatar = op.outcomes[0]
        tray = tray_avatar.obj
        for code in ("TRAY/RL", "TRAY/LL"):
            op = Arrival.create(
                   reason=self.code,
                   goods_type=PhysObj.Type.query().filter_by(code=code).one(),
                   goods_code=self.code,
                   location=tray,
                   state="planned",
                   dt_execution=datetime.now()
                )
            self.operations.append(op)

        return tray_avatar

    def get_obj_eventual_avatar(self, obj):
        """
        Return the eventual avatar of an obj.
        The only avatar which is not an input of an operation
        :param obj:
        :return:
        """
        Avatar = self.registry.Wms.PhysObj.Avatar
        return Avatar.query().filter_by(obj=obj, dt_until=None).first()

    def get_tray(self, code="TRAY"):
        """
        TODO: Pouvoir récupérer le TRAY en passant l'avatar en paramètre
        TODO: Modifier requête en utilisant un join sur PhysObj.Type
        Returns the tray associated to the preparation
        :param code:
        :return:
        """
        PhysObj = self.registry.Wms.PhysObj
        tray_gt = PhysObj.Type.query().filter_by(code=code).one()
        return PhysObj.query().filter_by(code=self.code, type=tray_gt).one()

    def get_avatars_in_tray(self):
        PhysObj = self.registry.Wms.PhysObj

        tray = self.get_tray()
        right_slot = self.get_tray("TRAY/RL")
        left_slot = self.get_tray("TRAY/LL")
        return PhysObj.Avatar.query().join(PhysObj.Avatar.obj).join(
                        PhysObj.type).filter(
                            PhysObj.Type.behaviours.comparator.has_key(
                                'storable'),  # noqa
                            or_(PhysObj.Avatar.location == tray,
                                PhysObj.Avatar.location == right_slot,
                                PhysObj.Avatar.location == left_slot),
                            PhysObj.Avatar.dt_until == None).order_by(  # noqa
                            PhysObj.Avatar.id).all()

    def plan_move_frame_to_tray(self, frame):
        """
        plans to move the frame to TRAY
        :return:
        """

        tray = self.get_tray()
        frame_avatar = self.get_obj_eventual_avatar(obj=frame)
        op = self.registry.Wms.Operation.Move.create(
                reason=self.code,
                state="planned",
                input=frame_avatar,
                destination=tray,
                dt_execution=datetime.now(),
            )
        self.operations.append(op)
        return op.outcomes[0]

    def plan_move_lenses_to_tray_slots(self, right_lens, left_lens):
        """
        plans to move the lenses to the respective slot (TRAY/RL or TRAY/LL)
        :return:
        """
        slots = {
            "TRAY/RL": right_lens,
            "TRAY/LL": left_lens
        }
        lens_avatars = []
        for slot_code, lens in slots.items():
            slot = self.get_tray(code=slot_code)
            avatar = self.get_obj_eventual_avatar(obj=lens)
            op = self.registry.Wms.Operation.Move.create(
                    reason=self.code,
                    state="planned",
                    input=avatar,
                    destination=slot,
                    dt_execution=datetime.now(),
                )
            self.operations.append(op)
            lens_avatars.append(op.outcomes[0])
        return lens_avatars

    def plan_se9090_operations(self,
                               tray_avatar,
                               frame_avatar,
                               right_lens_avatar,
                               left_lens_avatar):
        """
        plans to process SE9090 operations
        :param tray_avatar:
        :param frame_avatar:
        :param right_lens_avatar:
        :param left_lens_avatar:
        :return:
        """
        PhysObj = self.registry.Wms.PhysObj
        # plans to move the tray to SE9090001_FEEL_CENTER_TODO
        se9090_feel_center_todo = PhysObj.query().filter_by(
            code="WH-KEHL_SE9090001_FEEL_CENTER_TODO").one()
        op = self.registry.Wms.Operation.Move.create(
            reason=self.code,
            state="planned",
            input=tray_avatar,
            destination=se9090_feel_center_todo,
            dt_execution=datetime.now(),
        )
        self.operations.append(op)

        lens_avatars = [right_lens_avatar, left_lens_avatar]
        # plan to move TRAY from SE9090001_FEEL_CENTER_TODO
        # to SE9090001_FEEL_CENTER_IN_PROGRESS
        se9090_feel_center = PhysObj.query().filter_by(
            code="WH-KEHL_SE9090001_FEEL_CENTER_IN_PROGRESS").one()
        op = self.registry.Wms.Operation.Move.create(
               reason=self.code,
               state="planned",
               input=op.outcomes[0],
               destination=se9090_feel_center,
               dt_execution=datetime.now(),
        )
        self.operations.append(op)

        # plan to feel the frame (Observation) - felt=True
        # TODO: Pouvoir définir à l'avance les observed_properties attendues
        obs = self.registry.Wms.Operation.Observation.create(
                  reason=self.code,
                  name="frame_se9090_feel",
                  state="planned",
                  input=frame_avatar,
                  dt_execution=datetime.now(),
              )
        self.operations.append(obs)

        # plan to center the lenses (Observation) - centered = True
        centered_lenses_avatars = []
        for avatar in lens_avatars:
            obs = self.registry.Wms.Operation.Observation.create(
                    reason=self.code,
                    name="lens_se9090_center",
                    state="planned",
                    input=avatar,
                    dt_execution=datetime.now(),
                )
            self.operations.append(obs)
            centered_lenses_avatars.append(obs.outcomes[0])

        # plan to move the tray to SE9090001_FEEL_CENTER_DONE
        se9090_feel_center_done = PhysObj.query().filter_by(
            code="WH-KEHL_SE9090001_FEEL_CENTER_DONE").one()
        op = self.registry.Wms.Operation.Move.create(
            reason=self.code,
            state="planned",
            input=op.outcomes[0],
            destination=se9090_feel_center_done,
            dt_execution=datetime.now(),
        )
        self.operations.append(op)

        # plan to move the tray to SE9090001_CUT_TODO
        se9090_cut_todo = PhysObj.query().filter_by(
            code="WH-KEHL_SE9090001_CUT_TODO").one()
        op = self.registry.Wms.Operation.Move.create(
            reason=self.code,
            state="planned",
            input=op.outcomes[0],
            destination=se9090_cut_todo,
            dt_execution=datetime.now(),
        )
        self.operations.append(op)

        # plan to move the tray to SE9090001_CUT_IN_PROGRESS)
        se9090_cut = PhysObj.query().filter_by(
            code="WH-KEHL_SE9090001_CUT").one()
        op = self.registry.Wms.Operation.Move.create(
            reason=self.code,
            state="planned",
            input=op.outcomes[0],
            destination=se9090_cut,
            dt_execution=datetime.now(),
        )
        self.operations.append(op)

        # plan to cut the lenses (Observation) cut=True
        for avatar in centered_lenses_avatars:
            obs = self.registry.Wms.Operation.Observation.create(
                      reason=self.code,
                      name="lens_se9090_cut",
                      state="planned",
                      input=avatar,
                      dt_execution=datetime.now(),
                  )
            self.operations.append(obs)

        # plan to move the tray to SE9090001_CUT_DONE)
        se9090_cut_done = PhysObj.query().filter_by(
            code="WH-KEHL_SE9090001_CUT_DONE").one()
        op = self.registry.Wms.Operation.Move.create(
            reason=self.code,
            state="planned",
            input=op.outcomes[0],
            destination=se9090_cut_done,
            dt_execution=datetime.now(),
        )
        self.operations.append(op)
        return op.outcomes[0]

    def plan_lenses_arrival_and_reserve(self):
        """
        plans to receive lenses and reserve them
        :return:
        """
        req = self.get_reservation_request(reserved=True,
                                           purpose=["PREPARATION", self.code])
        lenses = dict()
        for key in ['right_lens_code', 'left_lens_code']:
            gt = self.get_input_type(key)
            arrival_location = gt.get_default_storage_location()
            op = self.registry.Wms.Operation.Arrival.create(
                    reason=self.code,
                    state="planned",
                    goods_type=gt,
                    location=arrival_location,
                    dt_execution=datetime.now(),
            )
            self.operations.append(op)
            req_item = self.registry.Wms.Reservation.RequestItem.insert(
                request=req,
                goods_type=gt,
                quantity=1)
            lens = op.outcomes[0].obj
            self.registry.Wms.Reservation.insert(physobj=lens,
                                                 quantity=1,
                                                 request_item=req_item)
            lenses.update({key[:-5]: lens})
        req.reserve()
        return lenses

    def create_order_supply(self, lens_avatars):
        """
        create the order supply
        :return:
        """
        pass

    def plan_mrblue_operations(self, tray_avatar, frame_avatar):
        """
        plans to process MRBLUE001 operations
        :return:
        """
        PhysObj = self.registry.Wms.PhysObj
        Operation = self.registry.Wms.Operation

        # plans to move the tray to MRBLUE001_TODO
        se9090_mrblue_todo = PhysObj.query().filter_by(
            code="WH-KEHL_MRBLUE001_TODO").one()
        op = Operation.Move.create(
            reason=self.code,
            state="planned",
            input=tray_avatar,
            destination=se9090_mrblue_todo,
            dt_execution=datetime.now()
        )
        self.operations.append(op)
        # plan to move the tray from MRBLUE001_TODO
        # to MRBLUE001_IN_PROGRESS
        mrblue = PhysObj.query().filter_by(
            code="WH-KEHL_MRBLUE001_IN_PROGRESS").one()
        op = Operation.Move.create(
            reason=self.code,
            state="planned",
            input=op.outcomes[0],
            destination=mrblue,
            dt_execution=datetime.now()
        )
        self.operations.append(op)

        # plan to feel the frame (Observation)
        obs = Operation.Observation.create(
                  reason=self.code,
                  name="frame_mrblue_feel",
                  state="planned",
                  input=frame_avatar,
                  dt_execution=datetime.now()
              )
        self.operations.append(obs)

        # plan to move the tray to MRBLUE001_DONE
        mrblue_done = PhysObj.query().filter_by(
            code="WH-KEHL_MRBLUE001_DONE").one()
        op = Operation.Move.create(
            reason=self.code,
            state="planned",
            input=op.outcomes[0],
            destination=mrblue_done,
            dt_execution=datetime.now()
        )
        self.operations.append(op)

        # plan to move the tray to a location waiting for lenses
        return op.outcomes[0]

    def plan_move_tray_to_waiting_location(self, tray_avatar):
        PhysObj = self.registry.Wms.PhysObj
        Operation = self.registry.Wms.Operation
        waiting_location = PhysObj.query().filter_by(
            code="WH-KEHL_ATELIER_ATTENTE").one()
        op = Operation.Move.create(
            reason=self.code,
            state="planned",
            input=tray_avatar,
            destination=waiting_location,
            dt_execution=datetime.now()
        )
        self.operations.append(op)
        return op.outcomes[0]

    def plan_move_tray_to_assembly_todo(self, tray_avatar):
        """
        plans to move the tray to the assembly location
        :return:
        """
        PhysObj = self.registry.Wms.PhysObj
        assembly_todo = PhysObj.query().filter_by(
            code="WH-KEHL_ATELIER_MONTAGE_TODO").one()

        op = self.registry.Wms.Operation.Move.create(
            reason=self.code,
            state="planned",
            input=tray_avatar,
            destination=assembly_todo,
            dt_execution=datetime.now()
        )
        self.operations.append(op)
        return op.outcomes[0]

    def plan_move_tray_to_assembly_workshop(self, tray_avatar):
        """
        plans to move the tray to the assembly location
        :return:
        """
        PhysObj = self.registry.Wms.PhysObj
        Operation = self.registry.Wms.Operation
        assembly = PhysObj.query().filter_by(
            code="WH-KEHL_ATELIER_MONTAGE_INPROGRESS").one()
        op = Operation.Move.create(
                reason=self.code,
                state="planned",
                input=tray_avatar,
                destination=assembly,
                dt_execution=datetime.now()
            )
        self.operations.append(op)
        return op.outcomes[0]

    def reserve_eyewear_for_shipping(self):
        """
        reserves the eyewear
        :return:
        """
        Reservation = self.registry.Wms.Reservation
        RequestItem = Reservation.RequestItem

        req = self.get_reservation_request(purpose=['SHIPPING', self.code])
        gt = self.registry.Wms.PhysObj.Type.query().filter_by(
            code=self.preparation_type).one()
        RequestItem.insert(
            goods_type=gt,
            quantity=1,
            request=req,
        )
        req.reserve()
        return req

    def compute_eyewear_code(self):
        """
        computes the eyewear code that will be given to the goods
        :return:
        """
        frame_gt = self.get_input_type('frame_code')
        right_lens_gt = self.get_input_type('right_lens_code')
        if self.preparation_type == "NP_EYEWEAR":
            return frame_gt.code + "_" + right_lens_gt.code
        if self.preparation_type == "UNIFOCAL_GLASSES":
            return frame_gt.code + "_" + right_lens_gt.code
        if self.preparation_type == "PROGRESSIVE_GLASSES":
            return frame_gt.code + "_" + right_lens_gt.code

    def plan_final_assembly(self):
        """
        plans to assemble the final product and reserves it for shipping
        :return:
        """
        PhysObj = self.registry.Wms.PhysObj
        Operation = self.registry.Wms.Operation

        eyewear_gt = PhysObj.Type.query().filter_by(
            code=self.preparation_type).one()
        inputs = self.get_avatars_in_tray()
        op = Operation.Assembly.create(
            reason=self.code,
            name="final",
            state="planned",
            inputs=inputs,
            outcome_type=eyewear_gt,
            dt_execution=datetime.now()
        )
        self.operations.append(op)
        op.outcomes[0].obj.code = self.compute_eyewear_code()
        return op.outcomes[0]

    def plan_move_tray_to_quality_todo(self, tray_avatar):
        """
        plans to move the tray to the quality to do location
        :return:
        """
        PhysObj = self.registry.Wms.PhysObj
        quality_todo = PhysObj.query().filter_by(
            code="WH-KEHL_ATELIER_QUALITY_TODO").one()
        op = self.registry.Wms.Operation.Move.create(
            reason=self.code,
            state="planned",
            input=tray_avatar,
            destination=quality_todo,
            dt_execution=datetime.now()
        )
        self.operations.append(op)
        return op.outcomes[0]

    def plan_move_tray_to_quality(self, tray_avatar):
        """
        plans to move the tray to the quality location
        :return:
        """
        PhysObj = self.registry.Wms.PhysObj
        quality = PhysObj.query().filter_by(
            code="WH-KEHL_ATELIER_QUALITY_INPROGRESS").one()
        op = self.registry.Wms.Operation.Move.create(
                 reason=self.code,
                 state="planned",
                 input=tray_avatar,
                 destination=quality,
                 dt_execution=datetime.now()
             )
        self.operations.append(op)
        return op.outcomes[0]

    def plan_quality_observation(self, eyewear_avatar):
        """
        plans to control the final product quality
        :return:
        """
        Operation = self.registry.Wms.Operation

        op = Operation.Observation.create(
                reason=self.code,
                name="eyewear_quality_control",
                state="planned",
                input=eyewear_avatar,
                dt_execution=datetime.now()
            )
        self.operations.append(op)
        return op.outcomes[0]

    def plan_stocked(self, **kwargs):
        """
        plans stocked eyewear's preparation operations
        :return:
        """
        tray_avatar = self.plan_arrival_tray_with_lenses_slots()
        frame_avatar = self.plan_move_frame_to_tray(frame=kwargs['frame'])
        lens_avatars = self.plan_move_lenses_to_tray_slots(
            right_lens=kwargs['right_lens'],
            left_lens=kwargs['left_lens'])
        tray_avatar = self.plan_se9090_operations(
            tray_avatar=tray_avatar,
            frame_avatar=frame_avatar,
            right_lens_avatar=lens_avatars[0],
            left_lens_avatar=lens_avatars[1],
        )
        tray_avatar = self.plan_move_tray_to_assembly_todo(
            tray_avatar=tray_avatar)
        tray_avatar = self.plan_move_tray_to_assembly_workshop(
            tray_avatar=tray_avatar)
        eyewear_avatar = self.plan_final_assembly()
        tray_avatar = self.plan_move_tray_to_quality_todo(
            tray_avatar=tray_avatar)
        self.plan_move_tray_to_quality(tray_avatar=tray_avatar)
        self.plan_quality_observation(eyewear_avatar=eyewear_avatar)
        self.reserve_eyewear_for_shipping()

    def plan_rx(self, **kwargs):
        """
        plans RX eyewear's preparation operations
        :return:
        """
        tray_avatar = self.plan_arrival_tray_with_lenses_slots()
        frame_avatar = self.plan_move_frame_to_tray(frame=kwargs['frame'])
        tray_avatar = self.plan_mrblue_operations(
            tray_avatar=tray_avatar,
            frame_avatar=frame_avatar)
        tray_avatar = self.plan_move_tray_to_waiting_location(
            tray_avatar=tray_avatar)
        lens_avatars = self.plan_move_lenses_to_tray_slots(
            right_lens=kwargs['right_lens'],
            left_lens=kwargs['left_lens'])
        self.create_order_supply(lens_avatars=lens_avatars)
        tray_avatar = self.plan_move_tray_to_assembly_todo(
            tray_avatar=tray_avatar)
        tray_avatar = self.plan_move_tray_to_assembly_workshop(
            tray_avatar=tray_avatar)
        eyewear_avatar = self.plan_final_assembly()
        tray_avatar = self.plan_move_tray_to_quality_todo(
            tray_avatar=tray_avatar)
        self.plan_move_tray_to_quality(tray_avatar=tray_avatar)
        self.plan_quality_observation(eyewear_avatar=eyewear_avatar)
        self.reserve_eyewear_for_shipping()


@register(Model.Wms.Sensee.Preparation)
class Parser(Model.Attachment.Parser):

    @classmethod
    def serialize(cls, model, data):
        Model = cls.registry.get(model)
        return {
            'static_path': os.path.join(BlokManager.getPath(
                'toolsapiblok'),
                'templates',
                'static'),
            'data': Model.query().filter(
                            Model.uuid.in_(data['uuids'])).all().to_dict(),
        }

    def check_if_file_must_be_generated(self, *args, **kwargs):
        return True
