from pyramid.view import (
        view_config,
        notfound_view_config,
        )

# Always send the default index.html
@notfound_view_config(renderer='templates/index.mako')
@view_config(renderer='templates/index.mako')
def index(request):
    return {}

