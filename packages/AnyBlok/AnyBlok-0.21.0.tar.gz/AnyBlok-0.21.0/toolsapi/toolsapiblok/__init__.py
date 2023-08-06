"""Toolsapi blok definitions
"""
from anyblok.blok import Blok
from anyblok_io.blok import BlokImporter
from sqlalchemy.orm.attributes import flag_modified

from .data import Location
from anyblok.blok import BlokManager
from os.path import join
import os


class Toolsapiblok(BlokImporter, Blok):
    """Toolsapiblok's Blok class definition
    """
    version = "0.3.5"
    author = "Franck Bret"
    required = [
        'anyblok-core',
        'backend',
        'anyblok-io-csv',
        'device_rest_api',
        'delivery_colissimo',
        'bus',
        'vision_card',
        'sensee_data_wms',
        'attachment_postgres',
        'anyblok-workflow',
        'wms-inventory',
    ]

    @classmethod
    def import_declaration_module(cls):
        """Python module to import in the given order at start-up
        """
        from . import models
        models.import_declarations()

    @classmethod
    def reload_declaration_module(cls, reload):
        """Python module to import while reloading server (ie when
        adding Blok at runtime)
        """
        from . import models
        reload(models)
        models.import_declarations(reload=reload)

    @classmethod
    def pyramid_load_config(cls, config):
        """Pyramid http server configuration / initialization
        """
        # Static resources
        config.add_static_view(
            'static',
            '%s/toolsapi/toolsapiblok/static/' % os.getcwd(),
            cache_max_age=3600)

        # Scan available views
        views_path = cls.__module__ + '.views'
        priority_packages = [
            views_path + '.api.v1.operation_move',
            views_path + '.api.v1.inventory_node',
        ]
        ignored_packages = []
        for pp in priority_packages:
            config.scan(pp)
            ignored_packages.append(pp)

        config.scan(views_path, ignore=ignored_packages)

        # Rest Api
        config.include("anyblok_device.bloks.rest_api", route_prefix="/api/v1/")

    def setup_bus_profiles(self):
        Profile = self.registry.Bus.Profile
        if not Profile.query().count():
            Profile.insert(name='dev',
                           url='amqp://guest:guest@localhost:5672/%2F')
            Profile.insert(name='local',
                           url='amqp://guest:guest@localhost:5672/%2F')
            Profile.insert(name='integ',
                           url='amqp://admin:admin@erp.dev.sensee:5672/%2Fdev')

    def setup_warehouse(self, latest_version):
        Parameter = self.registry.System.Parameter
        Mapping = self.registry.IO.Mapping
        PhysObj = self.registry.Wms.PhysObj
        if latest_version is None or latest_version < '0.2.0':
            Parameter.set('warehouse_code', 'WH-KEHL')
            address = self.registry.Address.insert(
                first_name=' ', last_name='Kehl', company_name='Sensee',
                street1='Otto Hahn Strasse, 10', zip_code='77694',
                city='Kehl Auenheim', country="DEU")
            Parameter.set('warehouse_address', str(address.uuid))
            location = PhysObj.query().filter_by(code='WH-KEHL').one()
            Parameter.set('warehouse_root_location', location.id)

        if Mapping.get(key='kehl_address', model='Model.Address') is None:
            self.registry.IO.Mapping.insert(
                primary_key={'uuid': Parameter.get('warehouse_address')},
                model='Model.Address', key='kehl_address')

        if Mapping.get(key='kehl_root_location', model='Model.Wms.PhysObj') is None:
            Mapping.set('kehl_root_location',
                        PhysObj.query().get(Parameter.get('warehouse_root_location')))

        self.import_file_xml('Model.Wms.Warehouse', 'data', 'warehouses.xml')

    def update(self, latest_version):
        self.setup_bus_profiles()
        if latest_version is None or latest_version <= "0.1.20":
            path = BlokManager.getPath(self.name)
            file_path = join(path, 'data', 'import_location.csv')
            Location(self.registry).import_locations_as_goods(
                file_path, delimiter=',')

        self.setup_warehouse(latest_version)

        if latest_version is None:
            page = self.registry.Attachment.WkHtml2Pdf.Page.insert(
                label="tray_labels", size="A4")
            wkhtml2pdf = self.registry.Attachment.WkHtml2Pdf.insert(
                label="tray_labels",
                page=page,
                margin_top=5,
                margin_bottom=4,
                margin_left=3,
                margin_right=3,
                dpi=90,
            )
            self.registry.Attachment.Template.Jinja.insert(
                name="tray_labels",
                template_path='toolsapiblok#=#templates/report/tray_labels.jinja2',
                jinja_paths='toolsapiblok#=#templates/report',
                wkhtml2pdf_configuration=wkhtml2pdf,
                contenttype='application/pdf',
                model='Model.Wms.Sensee.Preparation',
                parser_model='Model.Wms.Sensee.Preparation.Parser',
                filename='mypage.html')

    def post_migration(self, latest_version):
        if latest_version is None:
            return
        if latest_version > '0.1.0':
            if latest_version < '0.3.0':
                self.migr_avatar_reason_to_outcome_of()
            if latest_version < '0.3.1':
                self.migr_phobj_type_sensee_assembly_name()

    def migr_avatar_reason_to_outcome_of(self):
        execute = self.registry.execute

        execute("UPDATE wms_physobj_avatar "
                "SET outcome_of_id = reason_id")
        execute("ALTER TABLE wms_physobj_avatar "
                "DROP COLUMN reason_id")

    def migr_phobj_type_sensee_assembly_name(self):
        """Update assembly name in ``behaviours`` of ``PhysObj.Type`` from
           `sensee_assembly` to `final`

        """
        current_name = "sensee_assembly"
        new_name = "final"
        PhysObjType = self.registry.Wms.PhysObj.Type
        gts = PhysObjType.query().filter(
                PhysObjType.behaviours['assembly'].comparator.has_key(current_name)).all()  # noqa
        for gt in gts:
            assembly_content = gt.behaviours['assembly'].pop(current_name)
            gt.behaviours['assembly'][new_name] = assembly_content
            flag_modified(gt, '__anyblok_field_behaviours')
