# This file is a part of the AnyBlok project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import anyblok
from anyblok.release import version
from anyblok.config import Configuration
from logging import getLogger
from csv import DictReader, DictWriter
from datetime import datetime

logger = getLogger(__name__)

Configuration.add_application_properties(
    'convert_attachment_from_lb_to_lo',
    [
        'logging',
        'dramatiq-broker',
    ],
    prog='AnyBlok update label status, version %r' % version,
    description="Update label status"
)

Configuration.add_application_properties(
    'import_inventory',
    [
        'logging',
        'dramatiq-broker',
        'inventory',
    ],
    prog='Sensee import inventory, version %r' % version,
    description="Import inventory csv"
)


def convert_attachment_from_lb_to_lo():
    registry = anyblok.start('convert_attachment_from_lb_to_lo')
    if registry:
        Document = registry.Attachment.Document
        query = Document.query()
        query = query.filter(Document.file.isnot(None))
        nb_doc = query.count()
        executed = 0
        offset = 0
        limit = 10
        failed = 0
        done = 0
        while executed < nb_doc:
            query = Document.query()
            query = query.filter(Document.file.isnot(None))
            query = query.offset(offset).limit(limit)
            try:
                cursor = registry.session.connection().connection.cursor()
                query_count = query.count()
                for doc in query.all():
                    lobj = cursor.connection.lobject(0, 'wb')
                    lobj.write(doc.file)
                    query = """
                        UPDATE attachment_document
                        SET file = null,
                            lobject = %s
                        where uuid = %r
                              AND version = %r
                        """ % (lobj.oid, str(doc.uuid), doc.version)
                    registry.execute(query)
                    done += 1
                    logger.debug('Document %r(%r) is converted',
                                 doc.filename or doc.uuid, doc.version)
            except Exception as e:
                failed += query_count
                offset += limit
                logger.exception('Failed to convert : %r' % e)
                registry.rollback()
            finally:
                cursor.close()
                executed += query_count
                logger.info('%d / %d : %d documents converted, %d failed',
                            executed, nb_doc, done, failed)
                registry.commit()

        registry.close()


def import_inventory():
    registry = anyblok.start('import_inventory')
    if registry:
        inputcsvfile = Configuration.get('inventory_input_file')
        outputcsvfile = Configuration.get('inventory_output_file') % {'now': datetime.now()}
        delimiter = Configuration.get('inventory_delimiter')
        quotechar = Configuration.get('inventory_quotechar')
        batch_size = Configuration.get('inventory_batch_size')
        PhysObj = registry.Wms.PhysObj
        Type = registry.Wms.PhysObj.Type
        Apparition = registry.Wms.Operation.Apparition
        locations = {
            l.code: l
            for l in PhysObj.query().filter(Type.query_is_a_container()).all()}
        logger.info('Pre load %d locations' % len(locations))
        types = {
            t.code: t
            for t in Type.query().filter(Type.query_is_storable()).all()}
        logger.info('Pre load %d storable PhysObj.Type' % len(types))
        running = True
        nb_batch = 0
        nb_done_batch = 0
        with open(inputcsvfile, 'r') as finput:
            reader = DictReader(finput, delimiter=delimiter, quotechar=quotechar)
            headers = reader.fieldnames
            with open(outputcsvfile, 'w') as foutput:
                writer = DictWriter(foutput, delimiter=delimiter, quotechar=quotechar,
                                    fieldnames=headers)
                writer.writeheader()
                while running:
                    rows = []
                    nb_batch += 1
                    try:
                        for _ in range(batch_size):
                            rows.append(next(reader))
                    except StopIteration:
                        running = False

                    try:
                        for row in rows:
                            location = locations.get(row['loc_code'],
                                                     locations.get('WH-' + row['loc_code']))
                            if location is None:
                                raise KeyError(row['loc_code'])

                            physobj_type = types[row['physobj_type_code']]
                            quantity = int(eval(row['quantity']))
                            Apparition.create(
                                location=location, state='done', quantity=quantity,
                                physobj_type=physobj_type)

                        registry.commit()
                        nb_done_batch += 1
                        logger.info('batch %d done / %d: %d lines / %d', nb_done_batch, nb_batch,
                                    ((nb_done_batch - 1) * batch_size) + len(rows),
                                    ((nb_done_batch - 1) * batch_size) + len(rows))
                    except Exception:
                        logger.exception('Save batch %d: %d lines', nb_batch, len(rows))
                        registry.rollback()
                        writer.writerows(rows)

        logger.info('Import finish with %d bacth, %d batch done, %d batch with errors',
                    nb_batch, nb_done_batch, nb_batch - nb_done_batch)
