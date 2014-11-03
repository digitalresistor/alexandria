import logging
log = logging.getLogger(__name__)

from pyramid.view import (
        view_config,
        notfound_view_config,
        )

from pyramid.exceptions import (
        BadCSRFToken,
        PredicateMismatch,
        )

# Always send the default index.html
@notfound_view_config(renderer='templates/index.mako', xhr=False, accept='text/html')
@view_config(renderer='templates/index.mako', xhr=False, accept='text/html')
def index(request):
    token = request.session.get_csrf_token()
    response = request.response
    response.set_cookie('CSRF-Token', token, max_age=864000, overwrite=True)
    return {}

@notfound_view_config(route_name='__static/')
@notfound_view_config(route_name='__img/')
@notfound_view_config(route_name='__css/')
@notfound_view_config(route_name='__js/')
@notfound_view_config(route_name='__html/')
def not_found(request):
    request.response.status = 404
    return request.response

@view_config(
        context=BadCSRFToken,
        containment='..traversal.Root',
        renderer='json',
        )
def bad_csrf(request):
    response = request.response
    response.status = 400

    token = request.session.new_csrf_token()
    response.set_cookie('CSRF-Token', token, max_age=864000, overwrite=True)

    log.debug('New CSRF token: {}'.format(token));

    return {
            'errors': {
                'csrf': 'Invalid CSRF token. Please try again.'
                },
            }

@view_config(
        context=PredicateMismatch,
        containment='..traversal.Root',
        effective_principals='system.Everyone',
        )
def not_authorized(request):
    response = request.response

    if request.authenticated_userid is not None:
        response.status = 403
    else:
        response.status = 401

    return response
