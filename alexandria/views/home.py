from pyramid.view import (
        view_config,
        notfound_view_config,
        )

# Always send the default index.html
@notfound_view_config(renderer='templates/index.mako', xhr=False, accept='text/html')
@view_config(renderer='templates/index.mako', xhr=False, accept='text/html')
def index(request):
    return {}

