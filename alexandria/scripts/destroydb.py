import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker as sqla_sessionmaker

from ..models import *

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)

    # Configure sqlalchemy engine
    engine = engine_from_config(settings, 'sqlalchemy.')

    # Create a sessionmaker
    sessionmaker = sqla_sessionmaker()
    sessionmaker.configure(bind=engine)

    # Get us a dbsession
    dbsession = sessionmaker()

    # Register said dbsession against the transaction manager
    zope.sqlalchemy.register(dbsession, transaction_manager=transaction.manager)

    # Drop all tables/everything
    Base.metadata.drop_all(engine)

