from pyramid.view import (
        view_config,
        view_defaults,
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

    @view_config()
    def info(self):
        if self.request.authenticated_userid is None:
            ret = {
                    'authenticated': False,
                    }
        return ret

    @view_config(name='login')
    def login(self):
        if self.request.body:
            print(self.request.json_body)
            headers = remember(self.request, "example@example.com")
            self.request.response.headers.extend(headers)
        return {}

    @view_config(name='logout')
    def logout(self):
        if self.request.body:
            print(self.request.json_body)
        return {}

