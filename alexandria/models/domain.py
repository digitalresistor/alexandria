import datetime

from pyramid.compat import (
        text_type,
        binary_type
        )

from .meta import (
        Base,
        DBSession,
        )

from sqlalchemy import (
        Column,
        DateTime,
        ForeignKey,
        Integer,
        String,
        Table,
        and_,
        text,
        )

from sqlalchemy.orm import (
        relationship,
        )

from sqlalchemy.ext.hybrid import (
        hybrid_property,
        Comparator,
        )

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import inspect

from .idna import IdnaComparator


class Domain(Base):
    __table__ = Table('domains', Base.metadata,
            Column('id', UUID(as_uuid=True), server_default=text('uuid_generate_v4()'), primary_key=True, unique=True),
            Column('owner_id', ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False, index=True),
            Column('domain', String(256), index=True, unique=True),
            Column('primary_ns', String(256)),
            Column('hostmaster', String(256)),
            Column('serial', Integer),
            Column('refresh', Integer, server_default=text('16384')),
            Column('retry', Integer, server_default=text('2048')),
            Column('expiration', Integer, server_default=text('1048576')),
            Column('min_ttl', Integer, server_default=text('300')),
            Column('created', DateTime, server_default=text('current_timestamp')),
            Column('updated', DateTime, server_default=text('current_timestamp'), server_onupdate=text('current_timestamp')),
            )

    _domain = __table__.c.domain
    _primary_ns  = __table__.c.primary_ns
    _hostmaster = __table__.c.hostmaster

    # cls.domain
    @hybrid_property
    def domain(self):
        if isinstance(self, Domain):
            return self._domain.encode('ascii').decode('idna')
        return self._domain

    @domain.setter
    def domain(self, value):
        if isinstance(value, text_type):
            self._domain = value.encode('idna').decode('utf-8').lower()
        elif isinstance(value, binary_type):
            self._domain = value
        else:
            raise ValueError("Unable to store value as requested.")

    @domain.comparator
    def domain(cls):
        return IdnaComparator(cls._domain)

    # cls.primary_ns
    @hybrid_property
    def primary_ns(self):
        if isinstance(self, Domain):
            return self._primary_ns.encode('ascii').decode('idna')
        return self._primary_ns

    @primary_ns.setter
    def primary_ns(self, value):
        if isinstance(value, text_type):
            self._primary_ns = value.encode('idna').decode('utf-8').lower()
        elif isinstance(value, binary_type):
            self._primary_ns = value
        else:
            raise ValueError("Unable to store value as requested.")

    @primary_ns.comparator
    def primary_ns(cls):
        return IdnaComparator(cls._primary_ns)

    # cls.hostmaster
    @hybrid_property
    def hostmaster(self):
        if isinstance(self, Domain):
            return self._hostmaster.encode('ascii').decode('idna').replace('.', '@', 1)
        return self._hostmaster

    @hostmaster.setter
    def hostmaster(self, value):
        if isinstance(value, text_type):
            self._hostmaster = value.encode('idna').decode('utf-8').lower().replace('@', '.', 1)
        elif isinstance(value, binary_type):
            self._hostmaster = value
        else:
            raise ValueError("Unable to store value as requested.")

    @hostmaster.comparator
    def hostmaster(cls):
        return IdnaComparator(cls._hostmaster)


    def to_appstruct(self, drop=None):
        if drop is None:
            drop = []

        mapper = inspect(self.__class__)
        columns = [column.key.strip('_') for column in mapper.attrs]

        appstruct = {}

        for column in columns:
            if column not in drop:
                appstruct[column] = getattr(self, column)

        return appstruct
