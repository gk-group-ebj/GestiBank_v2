from flask import current_app
from datetime import datetime
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from time import time

from webapp.extensions import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(64), index=True)
    firstname = db.Column(db.String(64), index=True)
    email = db.Column(db.String(128), unique=True)
    phone = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    # Colonne type qui permettra de faire le lien entre les différentes tables
    type = db.Column(db.String(50))

    # Argument permettant de paramétrer les tables polymorphiques
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'user'
    }

    def __repr__(self):
        return "<Utilisateur {}>".format(self.lastname)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def checkpass(self, password):
        return check_password_hash(self.password, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_mdp': self.id, 'esp': time() + expires_in}, current_app.config['SECRET_KEY'],
                          algorithm='HS256').decode('utf-8')


class Admin(User):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)

    # Argument permettant de paramétrer les tables polymorphiques
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }


class Manager(User):
    __tablename__ = 'manager'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    mle = db.Column(db.Integer)
    registation = db.Column(db.String)
    entry_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Argument permettant de paramétrer les tables polymorphiques
    __mapper_args__ = {
        'polymorphic_identity': 'manager'
    }


class Client(User):
    __tablename__ = 'client'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    nb_street = db.Column(db.String)
    street = db.Column(db.String)
    city = db.Column(db.String)
    zip = db.Column(db.Integer)
    nb_child = db.Column(db.Integer)
    marital_status = db.Column(db.String)

    # Argument permettant de paramétrer les tables polymorphiques
    __mapper_args__ = {
        'polymorphic_identity': 'client'
    }
