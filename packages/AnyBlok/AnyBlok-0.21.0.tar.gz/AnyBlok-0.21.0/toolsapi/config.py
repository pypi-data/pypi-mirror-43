from anyblok.config import Configuration
from anyblok_pyramid import config  # noqa for update config
import os


Configuration.add_application_properties('pyramid', ['debug'])
Configuration.add_application_properties('gunicorn', ['debug'], add_default_group=False)
Configuration.add_application_properties('bus', ['dramatiq-broker'])


@Configuration.add('auth')
def update_plugins(group):
    group.set_defaults(
        pyramid_authentication_method='pyramid.authentication:SessionAuthenticationPolicy')


@Configuration.add('debug', label="Http server - debug",
                   must_be_loaded_by_unittest=True)
def define_http_debug(group):
    group.add_argument(
        '--debug-backend', action="store_true",
        default=(os.environ.get('TOOLS_KEHL_API_DEBUG_BACKEND') or False),
        help="Unminimify the javascript backend"
    )


@Configuration.add('inventory', label="Inventory")
def define_inventory(group):
    group.add_argument('--inventory-input-file')
    group.add_argument('--inventory-output-file', default='inventory-output-%(now)s.csv')
    group.add_argument('--inventory-batch-size', default=50, type=int)
    group.add_argument('--inventory-quotechar', default='"')
    group.add_argument('--inventory-delimiter', default=',')
