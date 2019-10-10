from flask import current_app, url_for
from datetime import datetime
import jwt
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from time import time

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

from webapp.bdd.models.utils import PaginatedAPIMixin
from webapp.extensions import db


@as_declarative()
class Base(db.Model, object):
    """Base class which provides automated table name
    and surrogate primary key column.

    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(64), index=True)
    firstname = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), unique=True)
    phone = db.Column(db.String(20))
    _password = db.Column("password_hash", db.String(128))


class ClientAssociation(Base):
    __tablename__ = 'client_association'

    discriminator = db.Column(db.String(120))
    """Refers to the type of parent."""

    __mapper_args__ = {"polymorphic_on": discriminator}


class Client(Base):
    """The Address class.

    This represents all address records in a
    single table.

    """

    association_id = db.Column(db.Integer, ForeignKey("client_association.id"))
    nb_street = db.Column(db.String(10))
    street = db.Column(db.String(250))
    city = db.Column(db.String(120))
    zip = db.Column(db.String(60))
    nb_child = db.Column(db.Integer)
    marital_status = db.Column(db.String(20))
    association = relationship("ClientAssociation", backref="clients")

    parent = association_proxy("association", "parent")

    def __repr__(self):
        return "%s(nb_street=%r, street=%r, city=%r, zip=%r, nb_child=%r, marital_status=%r)" % (
            self.__class__.__name__,
            self.nb_street,
            self.street,
            self.city,
            self.zip,
            self.nb_child,
            self.marital_status,
        )


class HasClients(object):
    """HasAddresses mixin, creates a relationship to
    the address_association table for each parent.

    """

    @declared_attr
    def client_association_id(cls):
        return db.Column(db.Integer, ForeignKey("client_association.id"))

    @declared_attr
    def client_association(cls):
        name = cls.__name__
        discriminator = name.lower()

        assoc_cls = type(
            "%sClientAssociation" % name,
            (ClientAssociation,),
            dict(
                __tablename__=None,
                __mapper_args__={"polymorphic_identity": discriminator},
            ),
        )

        cls.clients = association_proxy(
            "client_association",
            "clients",
            creator=lambda clients: assoc_cls(clients=clients),
        )
        return relationship(
            assoc_cls, backref=backref("parent", uselist=False)
        )


class Manager(HasClients, Base):
    mle = db.Column(db.Integer)
    entry_date = db.Column(db.DateTime, default=datetime.utcnow)


class Admin(Base):
    mle = db.Column(db.Integer)
    entry_date = db.Column(db.DateTime, default=datetime.utcnow)
