from pyramid.view import (
        view_config,
        notfound_view_config,
        )

# Always send the default index.html
@notfound_view_config(renderer='templates/index.mako', xhr=False, accept='text/html')
@view_config(renderer='templates/index.mako', xhr=False, accept='text/html')
def index(request):
    return {}

@notfound_view_config(route_name='__css/')
@notfound_view_config(route_name='__js/')
@notfound_view_config(route_name='__html/')
def not_found(request):
    request.response.status = 404
    return request.response
