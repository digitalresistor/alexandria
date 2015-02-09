import datetime

from .meta import (
        Base,
        )

from sqlalchemy import (
        Column,
        DateTime,
        ForeignKey,
        Index,
        Integer,
        PrimaryKeyConstraint,
        String,
        Table,
        Unicode,
        and_,
        text,
        )

from sqlalchemy.orm import (
        contains_eager,
        noload,
        relationship,
        )

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import UUID

from cryptacular.bcrypt import BCRYPTPasswordManager

class User(Base):
    __table__ = Table('users', Base.metadata,
            Column('id', UUID(as_uuid=True), server_default=text("uuid_generate_v4()"), primary_key=True, unique=True),
            Column('email', String(256), unique=True, index=True),
            Column('credentials', String(60))
            )

    _email = __table__.c.email
    _credentials = __table__.c.credentials

    @hybrid_property
    def credentials(self):
        return self._credentials

    @credentials.setter
    def credentials(self, value):
        manager = BCRYPTPasswordManager()
        self._credentials = manager.encode(value, rounds=14)

    @hybrid_property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value.lower().strip()

    def check_password(self, password):
        manager = BCRYPTPasswordManager()
        return manager.check(self.credentials, password)

    @classmethod
    def validate_user_password(cls, dbsession, email, password):
        user = dbsession.query(cls).filter(cls.email == email.lower()).first()

        if user is not None:
            if user.check_password(password):
                return user
        return None

class UserTickets(Base):
    __table__ = Table('user_tickets', Base.metadata,
            Column('ticket', String(128)),
            Column('user_id', ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE")),
            Column('remote_addr', String(45)),
            Column('created', DateTime, default=datetime.datetime.utcnow, nullable=False),

            PrimaryKeyConstraint('ticket', 'user_id'),
            Index('ix_ticket_userid', 'ticket', 'user_id'),
            )

    user = relationship("User", lazy="joined", backref='tickets')

    @classmethod
    def find_ticket_userid(cls, dbsession, ticket, userid):
        return dbsession.query(cls).join(
                User,
                and_(
                    User.email == userid.lower(),
                    User.id == cls.user_id
                    )
                ).filter(cls.ticket == ticket).options(
                            contains_eager('user')
                        ).first()

