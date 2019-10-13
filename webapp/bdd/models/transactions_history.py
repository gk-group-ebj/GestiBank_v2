# coding: utf-8

from datetime import datetime
from enum import Enum

from flask import url_for

from webapp.bdd.models.accounts import Account, NoAccountIdException, NegativeOperationException
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
    operation_date = db.Column(db.DateTime, default=datetime.utcnow(), index=True)  # Datetime
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False, index=True)
    type = db.Column(db.Enum(typeTransaction), nullable=False,
                     server_default=typeTransaction.CREDIT.name)  # Enum typeTransaction
    operation_amount = db.Column(db.Float(12, 2), default=0)
    balance_before_transaction = db.Column(db.Float(12, 2), default=0)
    balance_attime = db.Column(db.Float(12, 2), default=0)

    def __init__(self, **kwargs):
        super(TransactionHistory, self).__init__(**kwargs)
        if self.operation_date is None:
            self.operation_date = datetime.utcnow()

        if self.operation_amount is None:
            self.operation_amount = 0.0
        elif self.operation_amount < 0.0:
            raise NegativeOperationException(
                "FAILED: le montant impliqué dans l'opération sur le compte {} est négatif".format(self.account_number)
            )

        if self.account_id is not None:
            self.account = Account.query.get(self.account_id)
            if self.account:
                if self.balance_before_transaction is None:
                    self.balance_before_transaction = self.account.balance

                if self.balance_attime is None:
                    if self.type == typeTransaction.CREDIT or self.type == typeTransaction.CREDIT_BENEFIT:
                        self.balance_attime = self.account.credit(self.operation_amount)
                    elif self.type == typeTransaction.DEBIT or self.type == typeTransaction.DEBIT_AGIOS:
                        self.balance_attime = self.account.debit(self.operation_amount)
            else:
                raise NoAccountIdException(
                    "FAILED: No account_id"
                )
        else:
            raise NoAccountIdException(
                "FAILED: No account_id"
            )

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
        return "<{}[{} : {} : {} : {} : {} : {} : {}]>".format(self.__class__.__name__,
                                                               self.id,
                                                               self.account_id,
                                                               self.operation_date.strftime("%d-%m-%Y"),
                                                               self.type.name,
                                                               self.balance_before_transaction,
                                                               self.operation_amount,
                                                               self.balance_attime
                                                               )

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    from webapp.bdd.models.utils import store_data
    from datetime import datetime, timedelta
    from webapp.bdd.models.transactions_history import typeTransaction

    date_jour = datetime.utcnow()
    trimester_agios = 100
    t = TransactionHistory(operation_date=date_jour,
                           account_id=201,
                           operation_amount=trimester_agios,
                           type=typeTransaction.DEBIT_AGIOS
                           )
    store_data(t)
