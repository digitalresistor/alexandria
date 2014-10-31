from pyramid.view import (
        view_config,
        view_defaults,
        )

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

    @view_config(name='login', check_csrf=True, request_method='POST')
    def login(self):
        try:
            schema = s.UserSchema.create_schema(self.request)
            deserialized = schema.deserialize(self.cstruct)

            headers = remember(self.request, "example@example.com")
            token = self.request.session.new_csrf_token()

            response = HTTPSeeOther(location=self.request.route_url('main', traverse='user'), headers=headers)
            response.set_cookie('CSRF-Token', token, max_age=864000, overwrite=True)

            return response
        except colander.Invalid as e:
            self.request.response.status = 406
            return {
                    'errors': e.asdict(),
                    }

    @view_config(name='logout', check_csrf=True, request_method='POST')
    def logout(self):
        headers = forget(self.request)
        return HTTPSeeOther(location=self.request.route_url('main', traverse='user'), headers=headers)

    @view_config(
                context=HTTPNotFound,
                containment='..traversal.User'
            )
    def not_found(self):
        self.request.response.status = 404
        return self.request.response
