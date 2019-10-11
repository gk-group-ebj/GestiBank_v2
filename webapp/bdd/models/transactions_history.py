# coding: utf-8

from datetime import datetime
from enum import Enum

from flask import url_for

from webapp.bdd.models.utils import PaginatedAPIMixin
from webapp.extensions import db


# Compte courant sans autorisation de découvert
class typeTransaction(Enum):
    CREDIT = "Credit"
    CREDIT_BENEFIT = "Benefit"
    DEBIT = "Debit"
    DEBIT_AGIOS = "Agios"


class TransactionHistory(db.Model, PaginatedAPIMixin):
    __tablename__: "transaction_history"
    __table_args__ = {
        'extend_existing': True
    }

    id = db.Column(db.Integer, primary_key=True)  # Integer
    operation_date = db.Column(db.DateTime, default=datetime.utcnow(), index=True)  # Varchar(20)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False, index=True)
    type = db.Column(db.Enum(typeTransaction), nullable=False)  # Enum typeAccount
    operation_amount = db.Column(db.Float(12, 2), default=0)
    balance_attime = db.Column(db.Float(12, 2), default=0)

    def __init__(self, **kwargs):
        super(TransactionHistory, self).__init__(**kwargs)
        if self.operation_date is None:
            self.operation_date = datetime.utcnow()

        if self.balance_attime is None:
            self.balance_attime = 0.0

        if self.operation_amount is None:
            self.operation_amount = 0.0

    def to_dict(self, endpoint):
        data = {
            'id': self.id,
            'transaction': self.type,
            'account_id': self.account_id,
            '_links': {
                'self': url_for(endpoint, id=self.id)
            }
        }
        return data

    def __str__(self):
        return "<{}}[{} : {} : {} : {} : {} : {}]>" \
            .format(self.__class__.__name__,
                    self.id,
                    self.account_id,
                    self.operation_date.strftime("%d-%m-%Y"),
                    self.type,
                    self.operation_amount,
                    self.balance_attime)

    def __repr__(self):
        return self.__str__


if __name__ == "__main__":
    pass
