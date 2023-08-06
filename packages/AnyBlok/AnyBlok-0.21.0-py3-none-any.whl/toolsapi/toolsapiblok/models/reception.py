from anyblok import Declarations
from anyblok.column import String, DateTime, Integer, Text
from anyblok.relationship import Many2One, Many2Many, One2One
from datetime import timedelta
from anyblok_bus.status import MessageStatus
# from anyblok_bus import bus_consumer
# from bus_schema import PlanedReceptionSchema
from bus_schema import CancelReceptionSchema, DoReceptionSchema
from datetime import datetime
from json import dumps

Model = Declarations.Model
Mixin = Declarations.Mixin


@Declarations.register(Model)
class Reception(Mixin.UuidColumn, Mixin.TrackModel, Mixin.WorkFlow):

    WORKFLOW = {
        'draft': {
            'default': True,
            'allowed_to': ['planned', 'started', 'done', 'canceled'],
        },
        'planned': {
            'allowed_to': ['started', 'canceled', 'done'],
        },
        'started': {
            'allowed_to': ['done'],
        },
        'done': {
            # 'readonly': True,
            # TODO check all operation is done and have not got line without expected or quantity
        },
        'canceled': {},  # 'readonly': True},
    }

    rest = One2One(model='Model.Reception', backref="rest_of")

    sender_address = Many2One(model=Model.Address, nullable=False)
    recipient_address = Many2One(model=Model.Address, nullable=False)

    pack = String()
    reason = String(nullable=False)
    notes = Text()

    reception_date = DateTime()

    carrier = Many2One(model=Model.Delivery.Carrier)
    tracking_number = String()

    # TODO history

    @classmethod
    def get_address(cls, **kwargs):
        Address = cls.registry.Address
        address = Address.query().filter(
            *[getattr(Address, field) == value
              for field, value in kwargs.items()]
        ).first()
        if address is None:
            address = Address.insert(**kwargs)

        return address

    # Deactivate consumer
    # @bus_consumer(queue_name='kehl_create_planned_reception',
    #               schema=PlanedReceptionSchema())
    def create_planned_reception(cls, body=None):
        if cls.query().filter_by(uuid=body['uuid']).count():
            # message already exist
            return MessageStatus.ACK

        body['sender_address'] = cls.get_address(**body['sender_address'])
        body['recipient_address'] = cls.get_address(**body['recipient_address'])
        if body.get('carrier'):
            body['carrier'] = cls.registry.Delivery.Carrier.query().filter_by(
                code=body['carrier']).one()

        lines = body.pop('lines', [])
        Type = cls.registry.Wms.PhysObj.Type
        for line in lines:
            line['physobj_type'] = Type.query().filter_by(code=line['physobj_type']).one()

        reception = cls.create(body, lines=lines)
        reception.state = 'planned'
        # check the flush before ACK, mean that the DB and workflow has verified
        # the arrival with planned state
        cls.registry.flush()
        return MessageStatus.ACK

    def update_state_to_done(self):
        self.reception_date = datetime.now()
        for line in self.lines:
            if not (line.operations or line.quantity):
                raise Exception('Unplanned line without quantity')

            rest_operations = line.update_operations(
                line.quantity - len(line.operations),
                cancel=False)
            if line.quantity == 0:
                rest = self.get_rest()
                line.reception = rest
            else:
                for op in line.operations:
                    op.execute()

                if rest_operations:
                    rest = self.get_rest()
                    self.registry.Reception.Line.create(
                        reception=rest,
                        physobj_type=line.physobj_type,
                        location_code=line.location_code,
                        operations=rest_operations)

        self.registry.flush()
        self.state = 'done'
        # self.push_in_bus_do_reception()

    def push_in_bus_do_reception(self):
        message = dict(
            uuid=str(self.uuid),
            pack=self.pack,
            tracking_number=self.tracking_number,
            notes=self.notes or '',
            carrier=self.carrier.name if self.carrier else '',
            lines=[dict(physobj_type=l.physobj_type.code, quantity=l.quantity)
                   for l in self.lines],
        )
        if self.rest:
            message['rest'] = str(self.rest.uuid)

        validator = DoReceptionSchema()
        error = validator.validate(message)
        if error:
            self.registry.rollback()
            raise Exception(
                "Invalid message to send with %r: %r" % (message, error))

        self.registry.Bus.publish(
            'tools_kehl_sensee_exchange',
            'erp_sensee.v1.do_reception',
            dumps(message).encode('utf-8'),
            "application/json"
        )

    def update_state_to_canceled(self):
        for line in self.lines:
            if not line.operations:
                continue

            while line.operations:
                op = line.operations.pop()
                op.cancel()

        self.registry.flush()
        self.state = 'canceled'
        # self.push_in_bus_cancel_reception()

    def push_in_bus_cancel_reception(self):
        message = dict(
            uuid=str(self.uuid),
            notes=self.notes or ''
        )
        validator = CancelReceptionSchema()
        error = validator.validate(message)
        if error:
            self.registry.rollback()
            raise Exception(
                "Invalid message to send with %r %r" % (message, error))

        self.registry.Bus.publish(
            'tools_kehl_sensee_exchange',
            'erp_sensee.v1.cancel_reception',
            dumps(message).encode('utf-8'),
            "application/json"
        )

    @classmethod
    def create(cls, params, lines=None):
        state_done = False
        state_canceled = False
        if params.get('state', None) == 'done':
            state_done = True
            del params['state']
        elif params.get('state', None) == 'cancel':
            state_canceled = True
            del params['state']

        reception = cls.insert(**params)
        for line in (lines or []):
            cls.registry.Reception.Line.create(reception=reception, **line)

        if state_done:
            cls.registry.flush()
            reception.update_state_to_done()
        elif state_canceled:
            reception.registry.flush()
            reception.update_state_to_canceled()
        elif reception.state in ('draft', 'planned') and reception.has_qty_filled():
            reception.state = 'started'

        return reception

    def get_rest(self):
        if not self.rest:
            self.__class__.insert(
                rest_of=self,
                sender_address=self.sender_address,
                recipient_address=self.recipient_address,
                reason=self.reason, state='planned')

        return self.rest

    def has_qty_filled(self):
        for line in self.lines:
            if line.quantity:
                return True

        return False

    def update(self, lines=None, **params):
        state_done = False
        state_canceled = False
        if params.get('state', None) == 'done':
            state_done = True
            del params['state']
        elif params.get('state', None) == 'canceled':
            state_canceled = True
            del params['state']

        if params:
            super(Reception, self).update(**params)

        for line in (lines or []):
            if not line.get('id'):
                self.registry.Reception.Line.create(reception=self, **line)
            else:
                aline = self.registry.Reception.Line.query().get(line['id'])
                del line['id']
                line.pop('reception', None)
                line.pop('operations', None)
                aline.update(**line)

        if state_done:
            self.registry.flush()
            self.update_state_to_done()
        elif state_canceled:
            self.registry.flush()
            self.update_state_to_canceled()
        elif self.state in ('draft', 'planned') and self.has_qty_filled():
            self.state = 'started'


@Declarations.register(Model.Reception)
class Line(Mixin.IdColumn, Mixin.TrackModel):

    reception = Many2One(model=Model.Reception, nullable=False, one2many="lines")
    physobj_type = Many2One(model=Model.Wms.PhysObj.Type, nullable=False)
    quantity = Integer(default=0)
    broken_quantity = Integer(default=0)
    operations = Many2Many(model=Model.Wms.Operation.Arrival)
    location_code = String()

    @classmethod
    def create(cls, operations=None, **kwargs):
        expected_quantity = kwargs.pop('expected_quantity', None)
        self = cls.insert(**kwargs)
        if operations:
            self.operations.extend(operations)
        elif expected_quantity:
            self.create_operations(expected_quantity)

        return self

    def update(self, **kwargs):
        # TODO forbid the changement of physobj_type
        expected_quantity = kwargs.pop('expected_quantity', None)
        super(Line, self).update(**kwargs)
        if expected_quantity is not None:
            self.update_operations(expected_quantity - len(self.operations))

        return self

    def create_operations(self, quantity):
        storage_location = self.location_code
        dt_execution = self.create_date + timedelta(days=7)
        input_location = self.registry.Wms.PhysObj.query().filter_by(
                code="WH-KEHL-INPUT").one()
        for expected in range(quantity):
            arrival = self.registry.Wms.Operation.Arrival.create(
                reason=self.reception.reason,
                physobj_type=self.physobj_type,
                dt_execution=dt_execution,
                location=input_location,
                state='planned')

            if not storage_location:
                destination = self.physobj_type.get_default_storage_location()
            else:
                destination = self.registry.Wms.PhysObj.query().filter_by(
                    code=storage_location).one()

            if not destination:
                raise Exception("Cannot create Operation.Move for %s. Destination %s not found" %
                                (self.physobj_type, storage_location))

            self.registry.Wms.Operation.Move.create(
                reason=self.reception.reason,
                destination=destination, state='planned', input=arrival.outcomes[0],
                dt_execution=(dt_execution + timedelta(days=1)))

            self.operations.append(arrival)

    def update_operations(self, quantity, cancel=True):
        operations = []
        if quantity == 0:
            return operations
        elif quantity < 0:
            for x in range(- quantity):  # because quantity is negative
                operation = self.operations.pop(0)
                if cancel:
                    operation.cancel()
                    self.registry.flush()
                else:
                    operations.append(operation)
        else:
            self.create_operations(quantity)

        return operations
