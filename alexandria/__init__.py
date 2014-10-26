import logging
log = logging.getLogger(__name__)

from pyramid.config import Configurator
from sqlalchemy import engine_from_config



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings)



        exit(-1)


    config.add_static_view('static', 'static', cache_max_age=3600)




