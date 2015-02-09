import datetime

from pyramid.compat import (
        text_type,
        binary_type
        )

from .meta import Base

from sqlalchemy import (
        Column,
        DateTime,
        Enum,
        ForeignKey,
        Integer,
        String,
        Table,
        Text,
        and_,
        text,
        )

from sqlalchemy.orm import (
        contains_eager,
        noload,
        relationship,
        )

from sqlalchemy.ext.hybrid import (
        hybrid_property,
        Comparator,
        )

from sqlalchemy.dialects.postgresql import UUID

from .idna import IdnaComparator
from .types import type_to_value


class Record(Base):
    __table__ = Table('records', Base.metadata,
            Column('id', UUID(as_uuid=True), server_default=text('uuid_generate_v4()'), primary_key=True, unique=True),
            Column('domain_id', ForeignKey('domains.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False, index=True),
            Column('resource', String(256), index=True, unique=True),
            Column('ttl', Integer, server_default=text('3600')),
            Column('class', String(10), default=u"IN"),
            Column('type', Enum(*type_to_value.keys(), name='resource_type')),
            Column('record', Text),
            Column('priority', Integer, server_default=text('0'), nullable=True),
            Column('created', DateTime, server_default=text('current_timestamp')),
            Column('updated', DateTime, server_default=text('current_timestamp'), server_onupdate=text('current_timestamp')),
            )

    _resource = __table__.c.resource

    # cls.resource
    @hybrid_property
    def resource(self):
        if isinstance(self, Domain):
            return self._resource.encode('ascii').decode('idna')
        return self._resource

    @resource.setter
    def resource(self, value):
        if isinstance(value, text_type):
            self._resource = value.encode('idna').decode('utf-8').lower()
        elif isinstance(value, binary_type):
            self._resource = value
        else:
            raise ValueError("Unable to store value as requested.")

    @resource.comparator
    def resource(cls):
        return IdnaComparator(cls._resource)

