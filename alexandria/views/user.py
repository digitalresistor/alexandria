from pyramid.view import (
        view_config,
        view_defaults,
        )

from pyramid.httpexceptions import (
        HTTPSeeOther,
        HTTPNotFound,
        HTTPUnprocessableEntity,
        )

from pyramid.security import (
        remember,
        forget,
        )

@view_defaults(accept='application/json', renderer='json', context='..traversal.User')
class User(object):
    def __init__(self, context, request):
        self.request = request
        self.context = context

        if self.request.body:
            try:
                self.cstruct = self.request.json_body
            except ValueError:
                raise HTTPUnprocessableEntity()

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
            headers = remember(self.request, "example@example.com")
            return HTTPSeeOther(location=self.request.route_url('main', traverse='user'), headers=headers)
        return {}

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
