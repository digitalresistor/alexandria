from sqlalchemy.orm import sessionmaker as sqla_sessionmaker
from sqlalchemy import engine_from_config
import zope.sqlalchemy
import transaction

from .meta import Base

from .user import (
            User,
            UserTickets,
        )

from .domain import Domain
from .record import Record

from .types import (
        type_to_value,
        value_to_type,
        )

def includeme(config):
    settings = config.get_settings()
    sessionmaker = build_sessionmaker(settings)

    config.add_request_method(
                lambda r: get_dbsession(r, sessionmaker),
                'dbsession',
                reify=True,
            )

    # Include the transaction manager
    if 'tm.manager_hook' not in settings:
        config.add_settings({
            'tm.manager_hook': lambda _: transaction.TransactionManager(),
            })
    config.include('pyramid_tm')

def get_dbsession(request, sessionmaker):
    dbsession = sessionmaker()
    zope.sqlalchemy.register(dbsession, transaction_manager=request.tm)
    return dbsession

def build_sessionmaker(settings, prefix='sqlalchemy.'):
    engine = engine_from_config(settings, prefix)
    sessionmaker = sqla_sessionmaker()
    sessionmaker.configure(bind=engine)
    return sessionmaker
