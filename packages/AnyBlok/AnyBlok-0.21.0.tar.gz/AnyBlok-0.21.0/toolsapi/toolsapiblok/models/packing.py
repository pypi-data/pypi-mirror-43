from anyblok import Declarations
from anyblok.column import String
from anyblok.relationship import Many2Many, Many2One
from anyblok_bus import bus_consumer
from bus_schema import PackingDocumentSchema
from datetime import datetime
from base64 import b64decode
import hashlib
from anyblok_bus.status import MessageStatus


@Declarations.register(Declarations.Model)
class Packing:
    pass


@Declarations.register(Declarations.Model.Packing)
class Document(Declarations.Mixin.UuidColumn,
               Declarations.Mixin.TrackModel):

    reason = String()
    pack = String()
    invoices = Many2Many(model='Model.Packing.Document.Line',
                         join_table='invoice_document_line')
    cerfas = Many2Many(model='Model.Packing.Document.Line',
                       join_table='cerfa_document_line')
    prescriptions = Many2Many(model='Model.Packing.Document.Line',
                              join_table='prescription_document_line')

    @bus_consumer(queue_name='create_packing_document',
                  schema=PackingDocumentSchema())
    def create_packing_document(cls, body=None):
        if cls.query().filter_by(uuid=body['uuid']).count():
            # message already exist
            return MessageStatus.ACK

        packing = cls.insert(
            uuid=body['uuid'],
            reason=body.get('reason'),
            pack=body.get('pack'),
        )
        for attr in ('invoices', 'cerfas', 'prescriptions'):
            for data in body[attr]:
                line = cls.get_line(data)
                line.print_document()
                if attr == 'invoices':
                    line.print_document()

                getattr(packing, attr).append(line)

        return MessageStatus.ACK

    @classmethod
    def get_line(cls, data):
        Document = cls.registry.Attachment.Document
        device_code = data['device_code']
        file_ = b64decode(data['binary'].encode('utf-8'))
        hash = hashlib.sha256()
        hash.update(file_)
        document = Document.insert(
            lobject=file_,
            file_added_at=datetime.now(),
            filename=data['name'],
            contenttype=data['mimestype'],
            filesize=len(file_),
            hash=hash.digest())
        Device = cls.registry.Device
        printer = Device.query().filter_by(code=device_code).one()
        return cls.registry.Packing.Document.Line.insert(
            printer=printer, latest_document=document)


@Declarations.register(Declarations.Model.Packing.Document)
class Line(Declarations.Mixin.IdColumn,
           Declarations.Mixin.LatestDocument):

    printer = Many2One(model=Declarations.Model.Device, nullable=True)

    def print_document(self):
        self.printer.action_print_document(
            str(self.printer.uuid),  # dramatiq d'ont suport uuid
            document_uuid=str(self.latest_document_uuid)
        )
