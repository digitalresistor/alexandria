from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('alexandria')

import colander

from ..models import Domain

class DomainSchema(colander.Schema):
    """The schema for a domain"""

    @classmethod
    def create_schema(cls, request):
        return cls().bind(request=request)

    id = colander.SchemaNode(colander.String(), missing=colander.drop)
    owner_id = colander.SchemaNode(colander.String(), missing=colander.drop)
    domain = colander.SchemaNode(colander.String(), validator=colander.Length(max=256))
    primary_ns = colander.SchemaNode(colander.String(), validator=colander.Length(max=256))
    hostmaster = colander.SchemaNode(colander.String(), validator=colander.Length(max=256))
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
