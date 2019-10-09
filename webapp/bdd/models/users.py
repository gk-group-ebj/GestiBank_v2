from flask import current_app, url_for
from datetime import datetime
import jwt
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash
from time import time

from webapp.bdd.models.utils import PaginatedAPIMixin
from webapp.extensions import db


class User(db.Model, PaginatedAPIMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(64), index=True)
    firstname = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), unique=True)
    phone = db.Column(db.String(20))
    _password = db.Column("password_hash", db.String(128))
    # Colonne type qui permettra de faire le lien entre les différentes tables
    type = db.Column(db.String(50))

    # Argument permettant de parametrer les tables polymorphiques
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @hybrid_property
    def password_hash(self):
        return self._password

    @password_hash.setter
    def password_hash(self, password):
        self._password = generate_password_hash(password)

    def checkpass(self, password):
        if self.password_hash is not None:
            return check_password_hash(self.password, password)
        return False

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_mdp': self.id,
             'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('utf-8')

    def __repr__(self):
        return "<User : {}>".format(self.lastname)

    def to_dict(self, endpoint):
        data = {
            'id': self.id,
            'username': self.username,
            '_links': {
                'self': url_for(endpoint, id=self.id)
            }
        }
        return data

    @staticmethod
    def from_dict(cls, data, p_object=None, new_object=False):
        if data.json:
            data = data.json
        elif data.args:
            data = data.args
        else:
            return None

        if p_object is not None:
            my_object = p_object
        else:
            my_object = User()

        my_attr_dict = dict(User)
        my_attr_dict.remove("password_hash")

        for field in my_attr_dict:
            if field in data:
                setattr(my_object, field, data[field])

        if new_object and 'password_hash' in data:
            my_object.password_hash(data['password_hash'])


class Admin(User):
    __tablename__ = 'admin'

    # Argument permettant de parametrer les tables polymorphiques
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    admin_id = db.Column(db.Integer, primary_key=True, unique=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
        'inherit_condition': (id == User.id)
    }

    def __init__(self, **kwargs):
        super(Admin, self).__init__(**kwargs)
        self.admin_id = self.id

    def __repr__(self):
        return "<Admin : {}>".format(self.lastname)


class Manager(User):
    __tablename__ = 'manager'

    # Argument permettant de parametrer les tables polymorphiques
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    manager_id = db.Column(db.Integer, primary_key=True, unique=True)
    mle = db.Column(db.Integer)
    entry_date = db.Column(db.DateTime, default=datetime.utcnow)
    # One Manager to many Clients.
    clients = db.relationship(
        'Client',
        primaryjoin="(Manager.manager_id==Client.manager_id)",
        backref=backref('manager'),
        lazy='dynamic'
    )

    # Argument permettant de parametrer les tables polymorphiques
    __mapper_args__ = {'polymorphic_identity': 'manager',
                       'inherit_condition': (id == User.id)}

    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.manager_id = self.id
        self.entry_date = datetime.utcnow()

    def __repr__(self):
        return "<Manager : {}>".format(self.lastname)


class Client(User):
    __tablename__ = 'client'

    # Argument permettant de parametrer les tables polymorphiques
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    client_id = db.Column(db.Integer, primary_key=True, unique=True)
    # One Manager to many Clients
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.manager_id'))
    nb_street = db.Column(db.String(10))
    street = db.Column(db.String(250))
    city = db.Column(db.String(120))
    zip = db.Column(db.String(60))
    nb_child = db.Column(db.Integer)
    marital_status = db.Column(db.String(20))

    # Argument permettant de parametrer les tables polymorphiques
    __mapper_args__ = {
        'polymorphic_identity': 'client',
        'inherit_condition': (id == User.id)
    }

    def __init__(self, **kwargs):
        super(Client, self).__init__(**kwargs)
        self.client_id = self.id

    def __repr__(self):
        return "<Client : {}>".format(self.lastname)
