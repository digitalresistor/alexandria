import logging
log = logging.getLogger(__name__)

from pyramid.config import Configurator

required_settings = [
        'pyramid.secret.session',
        'pyramid.secret.auth',
        ]

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    do_start = True

    for _req in required_settings:
        if _req not in settings:
            log.error('{} is not set in configuration file.'.format(_req))
            do_start = False

    if do_start is False:
        log.error('Unable to start due to missing configuration')
        exit(-1)

    config = Configurator(settings=settings)
    config.include('.models')
    config.include('.session')
    config.include('.security')
    config.include('.renderer')

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


    class ExplicitAcceptPredicate(object):
        def __init__(self, val, config):
            self.val = val

        def text(self):
            return 'explicit_accept = %s' % (self.val,)

        phash = text

        def __call__(self, context, request):
            return self.val in [accept for accept in request.accept]

    config.add_view_predicate('explicit_accept', ExplicitAcceptPredicate)

    # Scan the views sub-module
    config.scan('.views')

    return config.make_wsgi_app()

