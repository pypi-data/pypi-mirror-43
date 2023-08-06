def anyblok_init_config(unittest=False):
    from anyblok.config import Configuration  # noqa for import order
    from anyblok_pyramid.config import Configuration  # noqa for import order
    from . import config  # noqa to update configuration
