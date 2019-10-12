# coding: utf-8
from datetime import datetime
from flask import url_for

from webapp.bdd.models.utils import PaginatedAPIMixin
from webapp.extensions import db


class OpenAccountRequest(db.Model, PaginatedAPIMixin):
    __tablename__ = 'open_account_request'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    lastname = db.Column(db.String(64), nullable=False)
    firstname = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False)
    id_card = db.Column(db.LargeBinary(length=(2**32)-1), nullable=False)
    proof_of_address = db.Column(db.LargeBinary(length=(2**32)-1), nullable=False)
    salary = db.Column(db.LargeBinary(length=(2**32)-1), nullable=False)
    request_date = db.Column(db.DateTime, default=datetime.utcnow())
    manager_id = db.Column(db.Integer, default=0)

    def __init__(self, **kwargs):
        super(OpenAccountRequest, self).__init__(**kwargs)
        if self.request_date is None:
            self.request_date = datetime.utcnow()

    def to_dict(self, endpoint):
        data = {
            'id': self.id,
            'request': self.type,
            '_links': {
                'self': url_for(endpoint, id=self.id)
            }
        }
        return data

    def __str__(self):
        return "<{}[{}:{}:{:+.2f}]>".format(self.__class__.__name__,
                                            self.id,
                                            self.request_date.strftime("%d-%m-%Y"),
                                            self.balance)

    def __repr__(self):
        return self.__str__()

    def to_dict(self, endpoint):
        data = {
            'id': self.id,
            'reqquest': self.account_number,
            '_links': {
                'self': url_for(endpoint, id=self.id)
            }
        }
        return data

    @staticmethod
    def from_dict(cls, data, p_object=None):
        if data.json:
            data = data.json
        elif data.args:
            data = data.args
        else:
            return None

        if p_object is not None:
            my_object = p_object
        else:
            my_object = OpenAccountRequest()

        my_attr_dict = dict(OpenAccountRequest)

        for field in my_attr_dict:
            if field in data:
                setattr(my_object, field, data[field])
