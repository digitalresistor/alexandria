from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('alexandria')

import colander

from ..models import User

@colander.deferred
def login_username_password(node, kw):
    request = kw.get('request')

    if request is None:
        raise KeyError('Require bind: request')

    def username_password(form, value):
        user = User.validate_user_password(request.dbsession, value['email'],
                value['password'])

        if user is None:
            exc = colander.Invalid(form, _("Username or password is incorrect"))
            exc['email'] = ''
            exc['password'] = ''
            raise exc

        value['email'] = user.email

    return username_password

class UserSchema(colander.Schema):
    """The user login form."""

    @classmethod
    def create_schema(cls, request):
        return cls(validator=login_username_password).bind(request=request)

    email = colander.SchemaNode(colander.String())
    password = colander.SchemaNode(colander.String(), validator=colander.Length(min=4))


