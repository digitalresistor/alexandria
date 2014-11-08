import logging
log = logging.getLogger(__name__)

import datetime
import uuid

from pyramid.renderers import JSON

def includeme(config):
    json_renderer = JSON()

    def datetime_adapter(obj, request):
        return obj.isoformat()
    json_renderer.add_adapter(datetime.datetime, datetime_adapter)

    def uuid_adapter(obj, request):
        return str(obj)
    json_renderer.add_adapter(uuid.UUID, uuid_adapter)

    config.add_renderer('json', json_renderer)

