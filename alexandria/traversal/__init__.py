class Root(object):
    """ 
    The main root object for any traversal
    """

    __name__ = None
    __parent__ = None

    def __init__(self, request):
        pass

    def __getitem__(self, key):
        next_ctx = None

        if key == 'user':
            next_ctx = User()

        if next_ctx is None:
            raise KeyError

        next_ctx.__parent__ = self

        return next_ctx

class User(object):
    __name__ = 'user'
    __parent__ = None

    def __init__(self):
        pass

    def __getitem__(self, key):
        raise KeyError

class Domains(object):
    __name__ = 'domains'
    __parent__ = None

    def __init__(self):
        pass

    def __getitem__(self, key):
        raise KeyError