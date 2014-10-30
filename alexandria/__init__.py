import logging
log = logging.getLogger(__name__)

from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import DBSession

required_settings = [
        'pyramid.secret.session',
        'pyramid.secret.auth',
        ]

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings)

    do_start = True

    for _req in required_settings:
        if _req not in settings:
            log.error('{} is not set in configuration file.'.format(_req))
            do_start = False

    if do_start is False:
        log.error('Unable to start due to missing configuration')
        exit(-1)

    # Include the transaction manager
    config.include('pyramid_tm')

    config.include('.session')
    config.include('.security')

    config.add_static_view('css', 'alexandria:static/css', cache_max_age=3600)
    config.add_static_view('js', 'alexandria:static/js', cache_max_age=3600)
    config.add_static_view('html', 'alexandria:static/html', cache_max_age=3600)
    config.add_static_view('img', 'alexandria:static/img', cache_max_age=3600)
    config.add_static_view('static', 'alexandria:static', cache_max_age=3600)

    config.add_route('main',
            '/*traverse',
            factory='.traversal.Root',
            use_global_views=True
            )

    # Scan the views sub-module
    config.scan('.views')

    return config.make_wsgi_app()

