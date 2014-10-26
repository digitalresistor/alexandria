from pyramid.response import Response
from pyramid.view import view_config

def home(request):
    return {'info': "alexandria"}

