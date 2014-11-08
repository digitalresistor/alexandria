import logging
log = logging.getLogger(__name__)

from pyramid.view import (
        view_config,
        view_defaults,
        )

from pyramid.exceptions import BadCSRFToken

from pyramid.httpexceptions import (
        HTTPSeeOther,
        HTTPNotFound,
        HTTPBadRequest,
        )

from pyramid.security import (
        remember,
        forget,
        )

from pyramid.session import check_csrf_token

import colander

from .. import models as m
from .. import schemas as s


@view_defaults(
        explicit_accept='application/json',
        renderer='json',
        context='..traversal.Domains',
        effective_principals='system.Authenticated',
        )
class Domains(object):
    def __init__(self, context, request):
        self.request = request
        self.context = context

        if self.request.body:
            try:
                self.cstruct = self.request.json_body
            except ValueError:
                raise HTTPBadRequest()

    def csrf_valid(self):
        if check_csrf_token(self.request, raises=False) == False:
            log.debug('CSRF token did not match.')
            log.debug('Expected token: {}'.format(self.request.session.get_csrf_token()))
            log.debug('Got token: {}'.format(self.request.headers['x-csrf-token'] if 'x-csrf-token' in self.request.headers else None))

            raise BadCSRFToken()

    @view_config()
    def info(self):
        users_domains = m.DBSession.query(m.Domain).filter(m.Domain.owner_id == self.request.user.user.id).all()

        domains = []

        for domain in users_domains:
            d = {
                    'domain': domain.domain,
                    'primary_ns': domain.primary_ns,
                    'hostmaster': domain.hostmaster,
                    'serial': domain.serial,
                    'refresh': domain.refresh,
                    'retry': domain.retry,
                    'expiration': domain.expiration,
                    'min_ttl': domain.min_ttl,
                    'created': domain.created,
                    'updated': domain.updated,
                    }
        return domains

    @view_config(
            context=HTTPNotFound,
            containment='..traversal.Domains'
            )
    def not_found(self):
        self.request.response.status = 404
        return self.request.response



