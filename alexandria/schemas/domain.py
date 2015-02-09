from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('alexandria')

import colander

from .. import models as m

@colander.deferred
def _new_domain(node, kw):
    request = kw.get('request')

    if request is None:
        raise KeyError('Require bind: request')

    def new_domain(form, value):
        d = request.dbsession.query(m.Domain).filter(m.Domain.domain == value['domain']).first()

        if d is not None:
            exc = colander.Invalid(form)
            exc['domain'] = _("Domain already exists")

            if 'id' in value:
                if d.id != value['id']:
                    raise exc
            else:
                raise exc

    return new_domain


def hostmaster_periods(node, value):
    mailbox = value

    if '@' in value:
        if value.count('@') > 1:
            raise colander.Invalid(node, "Email address can't contain multiple @ symbols")

        (mailbox, fqdn) = value.split('@')

    if mailbox.count('.') > 0:
        raise colander.Invalid(node, "Mailbox part in email address may not contain any periods")


class DomainSchema(colander.Schema):
    """The schema for a domain"""

    @classmethod
    def create_schema(cls, request):
        return cls(validator=_new_domain).bind(request=request)

    id = colander.SchemaNode(colander.String(), missing=colander.drop)
    owner_id = colander.SchemaNode(colander.String(), missing=colander.drop)
    domain = colander.SchemaNode(colander.String(), validator=colander.Length(max=256))
    primary_ns = colander.SchemaNode(colander.String(), validator=colander.Length(max=256))
    hostmaster = colander.SchemaNode(colander.String(), validator=colander.All(colander.Length(max=256), hostmaster_periods))
    serial = colander.SchemaNode(colander.Integer(), missing=colander.drop)
    refresh = colander.SchemaNode(colander.Integer(), missing=colander.drop)
    retry = colander.SchemaNode(colander.Integer(), missing=colander.drop)
    expiration = colander.SchemaNode(colander.Integer(), missing=colander.drop)
    min_ttl = colander.SchemaNode(colander.Integer(), missing=colander.drop)
    created = colander.SchemaNode(colander.DateTime(), missing=colander.drop)
    updated = colander.SchemaNode(colander.DateTime(), missing=colander.drop)

class DomainsSchema(colander.SequenceSchema):
    """The domains schema form"""

    domains = DomainSchema()
