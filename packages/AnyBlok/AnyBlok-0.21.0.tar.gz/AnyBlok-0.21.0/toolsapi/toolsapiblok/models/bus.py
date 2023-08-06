from anyblok import Declarations
from marshmallow import Schema, fields
from anyblok_bus import bus_consumer
from anyblok_bus.status import MessageStatus
from logging import getLogger


logger = getLogger(__name__)


class PingSchema(Schema):

    exchange = fields.String(required=True)
    routing_key = fields.String(required=True)
    properties = fields.Dict(required=True)


@Declarations.register(Declarations.Model.Bus)
class Profile:

    @bus_consumer(queue_name='blok_tools_ping', schema=PingSchema())
    def ping(self, body=None):
        logger.info('Received ping with body %s', body)
        return MessageStatus.ACK
