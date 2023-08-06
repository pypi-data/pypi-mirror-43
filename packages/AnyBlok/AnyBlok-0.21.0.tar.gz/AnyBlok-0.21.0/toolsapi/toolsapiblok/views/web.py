"""Views that renders html
"""
from pyramid.view import view_config

from anyblok.config import Configuration
from anyblok_pyramid import current_blok
from pyramid.httpexceptions import HTTPMovedPermanently


@view_config(route_name='web_backend',
             installed_blok=current_blok(),
             renderer='templates/backend.jinja2')
def backend(request):
    """No authentication is required
    """
    vals = request.matchdict.copy()
    vals.update(
        debug_backend=Configuration.get('debug_backend')
    )
    return vals


@view_config(route_name='web_homepage')
def web_homepage(request):
    if 'LANG' in request.environ.keys() and request.environ['LANG']:
        locale = request.environ['LANG'][:2]
    else:
        locale = 'en'
    return HTTPMovedPermanently(
        request.route_url(
            "web_backend",
            locale=locale,
        )
    )
