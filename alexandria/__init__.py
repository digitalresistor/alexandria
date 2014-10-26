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

    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('main',
            '/*traverse',
            use_global_views=True
            )


    return config.make_wsgi_app()

