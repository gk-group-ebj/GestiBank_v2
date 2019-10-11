# coding: utf-8

from datetime import datetime
from time import time

import jwt
import sqlalchemy

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref

from werkzeug.security import generate_password_hash, check_password_hash

from flask import current_app, url_for
from flask_login import UserMixin

from webapp.bdd.models.utils import PaginatedAPIMixin, same_as, store_data, commit_data
from webapp.extensions import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, PaginatedAPIMixin, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {
        'extend_existing': True
    }

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    lastname = db.Column(db.String(64))
    firstname = db.Column(db.String(64))
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    _password = db.Column("password_hash", db.String(128))

    # Colonne type qui permettra de faire le lien entre les différentes tables
    type = db.Column(db.String(50))

    # Argument permettant de parametrer les tables polymorphiques
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    @hybrid_property
    def password_hash(self):
        return self._password

    @password_hash.setter
    def password_hash(self, password):
        if (self.password_hash is None) or (UserPassword.verify_old_password(self.id, password) is False):
            self.password_hash = generate_password_hash(password)
            store_data(
                [UserPassword(user_id=self.id, password_hash=self.password_hash)])
            commit_data()
            return True
        return False

    def checkpass(self, password):
        if self.password_hash is not None:
            return check_password_hash(self.password_hash, password)
        return False

    def get_reset_password_token(self, expires_in=None):
        if expires_in is None:
            expires_in = current_app.config['EXPIRES_IN']

        return jwt.encode(
            {'reset_mdp': self.id,
             'pwd_hash': self.password_hash,
             'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('utf-8')

    def to_dict(self, endpoint):
        data = {
            'id': self.id,
            'username': self.username,
            '_links': {
                'self': url_for(endpoint, id=self.id)
            }
        }
        return data

    def __str__(self):
        return "<{}[{}:{}:{}:{}]>".format(
                                    self.__class__.__name__,
                                    self.username,
                                    self.email,
                                    self.lastname,
                                    self.firstname
                                )

    def __repr__(self):
        return self.__str__()


class Admin(User):
    __tablename__ = 'admin'
    __table_args__ = {
        'extend_existing': True
    }

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    # Argument permettant de parametrer les tables polymorphiques
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
        'inherit_condition': (id == User.id)
    }


class Manager(User):
    __tablename__ = 'manager'
    __table_args__ = {
        'extend_existing': True
    }

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    mle = db.Column(db.Integer)
    entry_date = db.Column(db.DateTime, default=datetime.utcnow)
    clients = db.relationship(  # One Manager to many Clients.
        'Client',
        primaryjoin="(Manager.id==Client.manager_id)",
        backref=backref('manager'),
        lazy='dynamic'
    )

    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)

        if self.entry_date is not None:
            self.entry_date = datetime.utcnow()

    # Argument permettant de parametrer les tables polymorphiques
    __mapper_args__ = {
        'polymorphic_identity': 'manager',
        'inherit_condition': (id == User.id)
    }


class Client(User):
    __tablename__ = 'client'
    __table_args__ = {
        'extend_existing': True
    }

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    client_id = db.Column(db.Integer, primary_key=True, unique=True, default=same_as('id'))
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'), index=True)  # One Manager to many Clients
    nb_street = db.Column(db.String(10))
    street = db.Column(db.String(250))
    city = db.Column(db.String(120))
    zip = db.Column(db.String(60))
    nb_child = db.Column(db.Integer)
    marital_status = db.Column(db.String(20))

    def __init__(self, **kwargs):
        super(Client, self).__init__(**kwargs)
        self.client_id = self.id

    # Argument permettant de parametrer les tables polymorphiques
    __mapper_args__ = {
        'polymorphic_identity': 'client',
        'inherit_condition': (id == User.id)
    }


class UserPassword(db.Model):
    __tablename__ = "user_pwd"
    __table_args__ = {
        'extend_existing': True
    }

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # Integer
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Integer Foreign_key
    password_hash = db.Column(db.String(128))

    @staticmethod
    def verify_old_password(p_id, p_pwd, p_nb_pwd=None):
        if (p_id is not None) and (p_pwd is not None):
            if p_nb_pwd is None:
                p_nb_pwd = current_app.config['NB_PWD']

            pwd_list = UserPassword.query.filter(UserPassword.user_id == p_id) \
                .order_by(UserPassword.id.desc()) \
                .limit(p_nb_pwd) \
                .all()
            if pwd_list is not None:
                for row in pwd_list:
                    if check_password_hash(row.password_hash, p_pwd):
                        return True
        return False


def verify_reset_password_token(token):
    dict_token = dict()
    try:
        dict_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithm=['HS256'])
    except Exception as e:
        pass
    finally:
        p_id = dict_token['reset_pwd']
        p_pwd_hash = dict_token['pwd_hash']
        user = User.query.get(p_id)
        if user.password_hash == p_pwd_hash:
            return user
        else:
            print('Token deactivate')


if __name__ == "__main__":
    a1 = Admin(username="admin1", email="admin1@gestibank.fr")
    a2 = Admin(username="admin2", email="admin2@gestibank.fr")
    store_data(a1)
    store_data(a2)

    m1 = Manager(username="manager1", email="manager1@gestibank.fr")
    m2 = Manager(username="manager2", email="manager2@gestibank.fr")
    store_data([m1, m2])

    u1 = User(username="user1", email="user1@yahoo.fr")
    u2 = User(username="user2", email="user2@gmail.com")
    c1 = Client(username="client1", email="client1@yahoo.fr", manager_id=m1.id)
    c2 = Client(username="client2", email="client2@orange.fr", manager_id=m1.id)
    c3 = Client(username="client3", email="client3@hotmail.com", manager_id=m2.id)

    store_data([u1, u2])
    store_data([c1, c2, c3])
