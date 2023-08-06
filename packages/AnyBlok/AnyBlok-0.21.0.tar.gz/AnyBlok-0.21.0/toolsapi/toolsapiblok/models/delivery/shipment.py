from anyblok import Declarations
from anyblok.column import String
from anyblok_bus import bus_consumer
from bus_schema import CreateShipmentSchema, ShipmentTrackingNumberSchema
from anyblok_bus.status import MessageStatus
from json import dumps
from logging import getLogger


logger = getLogger(__name__)


@Declarations.register(Declarations.Model.Delivery)
class Shipment:

    device_code = String()

    @bus_consumer(queue_name='kehl_create_shipment', schema=CreateShipmentSchema())
    def create_shipment(cls, body=None):
        if cls.query().filter_by(uuid=body['uuid']).count():
            # message already exist
            return MessageStatus.ACK

        service = cls.get_service(**body['service'])
        sender_address = cls.get_address(**body['sender_address'])
        recipient_address = cls.get_address(**body['recipient_address'])
        device_code = body['device_code']
        shipment = cls.insert(
            uuid=body['uuid'],
            service=service, sender_address=sender_address,
            recipient_address=recipient_address,
            reason=body.get('reason'),
            pack=body.get('pack'),
            device_code=device_code
        )
        try:
            cls.get_and_print_label(str(shipment.uuid), device_code)
        except Exception as e:
            logger.exception("Can not print : %r" % e)
            raise

        return MessageStatus.ACK

    @classmethod
    def get_and_print_label(cls, shipment_uuid, device_code):
        shipment = cls.query().get(shipment_uuid)
        shipment.create_label()
        Device = cls.registry.Device
        printer = Device.query().filter_by(code=device_code).one()
        printer.action_print_document(
            str(printer.uuid),  # dramatiq d'ont suport uuid
            document_uuid=str(shipment.document_uuid)
        )
        shipment.push_in_bus_tracking_number()
        shipment.status = 'label'

    @classmethod
    def get_service(cls, product_code=None, carrier_code=None, **kwargs):
        Service = cls.registry.Delivery.Carrier.Service
        return Service.query().filter(
            Service.product_code == product_code,
            Service.carrier_code == carrier_code
        ).one()

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

    def take_by_the_carrier(self):
        """Todo return to odoo that the status change"""
        self.status = "transit"

    def delivered_by_the_carrier(self):
        """Todo return to odoo that the status change"""
        self.status = "delivered"

    def push_in_bus_tracking_number(self):
        message = dict(
            uuid=str(self.uuid),
            reason=self.reason,
            pack=self.pack,
            tracking_number=self.tracking_number,
        )
        validator = ShipmentTrackingNumberSchema()
        error = validator.validate(message)
        if error:
            raise Exception(
                "Invalid message to send with %r" % message)

        self.registry.Bus.publish(
            'tools_kehl_sensee_exchange',
            'erp_sensee.v1.update_tracking_number',
            dumps(message).encode('utf-8'),
            "application/json"
        )
