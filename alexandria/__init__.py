import logging
log = logging.getLogger(__name__)

from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from models import DBSession

from sqlalchemy.exc import DBAPIError

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings)

    if not 'pyramid.sess.secret' in settings:
        log.error('pyramid.sess.secret is not set, unable to start.')
        exit(-1)

    if not 'pyramid.auth.secret' in settings:
        log.error('pyramid.auth.secret is not set. Refusing to start.')
        exit(-1)

    if not 'pyramid.upload_path' in settings:
        log.error('pyramid.upload_path us not set. Refusing to start.')
        exit(-1)

    _session_factory = UnencryptedCookieSessionFactoryConfig(settings['pyramid.sess.secret'],
            cookie_httponly=True,
            cookie_max_age=864000
            )

    _authn_policy = AuthTktAuthenticationPolicy(
            settings['pyramid.auth.secret'],
            max_age=864000,
            http_only=True,
            hashalg='sha512',
            callback=lambda x : None,
            )

    _authz_policy = ACLAuthorizationPolicy()


    config.set_session_factory(_session_factory)
    config.set_authentication_policy(_authn_policy)
    config.set_authorization_policy(_authz_policy)

    config.include(add_routes)
    config.include(add_views)
    config.include(add_events)

    return config.make_wsgi_app()

def add_routes(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('alexandria.home', '/')

def add_views(config):
    config.add_view('alexandria.views.home.home', route_name='alexandria.home',
            renderer='home.mako')

    # Error pages
    config.add_view('alexandria.views.errors.db_failed', context=DBAPIError, renderer='error_db_failed.mako')
    config.add_notfound_view('alexandria.views.errors.not_found', renderer='error_not_found.mako', append_slash=False)

def add_events(config):
    pass

