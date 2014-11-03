import logging
log = logging.getLogger(__name__)

from pyramid.view import (
        view_config,
        view_defaults,
        )

from pyramid.exceptions import BadCSRFToken

from pyramid.httpexceptions import (
        HTTPSeeOther,
        HTTPNotFound,
        HTTPUnprocessableEntity,
        HTTPBadRequest,
        )

from pyramid.security import (
        remember,
        forget,
        )

from pyramid.session import check_csrf_token

import colander

from .. import schemas as s

@view_defaults(accept='application/json', renderer='json', context='..traversal.User')
class User(object):
    def __init__(self, context, request):
        self.request = request
        self.context = context

        if self.request.body:
            try:
                self.cstruct = self.request.json_body
            except ValueError:
                raise HTTPBadRequest()

    def csrf_valid(self):
        if check_csrf_token(self.request, raises=False) == False:
            log.debug('CSRF token did not match.')
            log.debug('Expected token: {}'.format(self.request.session.get_csrf_token()))
            log.debug('Got token: {}'.format(self.request.headers['x-csrf-token'] if 'x-csrf-token' in self.request.headers else None))

            raise BadCSRFToken()

    @view_config()
    def info(self):
        if self.request.authenticated_userid is None:
            ret = {
                    'authenticated': False,
                    }
        else:
            ret = {
                    'authenticated': True,
                    'user': {
                            'username': self.request.user.user.email,
                        }
                    }
        return ret

    @view_config(name='login', request_method='POST')
    def login(self):
        self.csrf_valid()

        try:
            schema = s.UserSchema.create_schema(self.request)
            deserialized = schema.deserialize(self.cstruct)

            headers = remember(self.request, deserialized['email'])
            token = self.request.session.new_csrf_token()

            response = HTTPSeeOther(location=self.request.route_url('main', traverse='user'), headers=headers)
            response.set_cookie('CSRF-Token', token, max_age=864000, overwrite=True)

            return response
        except colander.Invalid as e:
            self.request.response.status = 422

            form_error = None
            field_errors = e.asdict()

            if 'email' in field_errors and 'password' in field_errors:
                if field_errors['email'] == field_errors['password']:
                    form_error = "Username or password is incorrect."

            return {
                    'errors': field_errors,
                    'form_error': form_error,
                    }

    @view_config(name='logout', request_method='POST')
    def logout(self):
        self.csrf_valid()

        headers = forget(self.request)
        return HTTPSeeOther(location=self.request.route_url('main', traverse='user'), headers=headers)

    @view_config(
                context=HTTPNotFound,
                containment='..traversal.User'
            )
    def not_found(self):
        self.request.response.status = 404
        return self.request.response

    @view_config(
            context=BadCSRFToken,
            containment='..traversal.User',
            renderer='json',
            )
    def bad_csrf(self):
        response = self.request.response
        response.status = 400

        token = self.request.session.new_csrf_token()
        response.set_cookie('CSRF-Token', token, max_age=864000, overwrite=True)

        log.debug('New CSRF token: {}'.format(token));

        return {
                'errors': {
                    'csrf': 'Invalid CSRF token. Please try again.'
                    },
                }
