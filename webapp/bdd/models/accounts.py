# coding: utf-8

from datetime import datetime
from enum import Enum

from flask import url_for
from sqlalchemy.ext.hybrid import hybrid_property

from webapp.bdd.models.utils import PaginatedAPIMixin
from webapp.extensions import db


# Compte courant sans autorisation de découvert
class typeAccount(Enum):
    CURRENT_ACCOUNT = "Compte Courant"
    DEBIT_ACCOUNT = "Compte Autorisation de découvert"
    PAID_ACCOUNT = "Compte Rémunéré"


class Account(db.Model, PaginatedAPIMixin):
    __tablename__: "account"
    __table_args__= {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)  # Integer
    account_number = db.Column(db.Integer, nullable=False, index=True, unique=True)  # Varchar(40)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), index=True)
    type = db.Column(db.Enum(typeAccount), nullable=False,
                     server_default=typeAccount.CURRENT_ACCOUNT.name)  # Enum typeAccount
    creation_date = db.Column(db.DateTime, default=datetime.utcnow())  # Datetime(20)
    iban = db.Column(db.String(20), unique=True)  # Varchar(20)
    balance = db.Column(db.Float(12, 2), default=0)
    _cashier_facility = db.Column("cashier_facility", db.Float(12, 2), default=0)
    _paid_threshold = db.Column("paid_threshold", db.Float(12, 2), default=0)

    __mapper_args__ = {
        'polymorphic_identity': 'account',
        'polymorphic_on': type
    }

    def __init__(self, **kwargs):
        super(Account, self).__init__(**kwargs)
        self.type = typeAccount.CURRENT_ACCOUNT

        if self.creation_date is None:
            self.creation_date = datetime.utcnow()

        if self.balance is None:
            self.balance = 0.0

        if self._cashier_facility is None:
            self._cashier_facility = 0.0

        if self._paid_threshold is None:
            self._paid_threshold = 0.0

    @hybrid_property
    def cashier_facility(self):
        return self._cashier_facility

    @cashier_facility.setter
    def cashier_facility(self, p_cashier):
        if p_cashier >= 0.0:
            self._cashier_facility = float(p_cashier)
        else:
            raise NegativeCashierFacilityException(
                "FAILED: le montant de découvert autorisé pour le compte {} est négatif. "
                "Entrez un montant positif".format(self.account_number)
            )

    @hybrid_property
    def paid_threshold(self):
        return self._paid_threshold

    @paid_threshold.setter
    def paid_threshold(self, p_paid):
        if p_paid >= 0.0:
            self._paid_threshold = float(p_paid)
        else:
            raise NegativePaidThresholdException(
                "FAILED: le seuil de rémunération pour le compte {} est négatif. Entrez un montant positif".format(
                    self.account_number)
            )

    # Methods
    def credit(self, p_amount):
        if p_amount >= 0.0:
            self.balance = self.balance + float(p_amount)
        else:
            raise NegativeOperationException(
                "FAILED: le montant impliqué dans l'opération sur le compte {} est négatif".format(self.account_number)
            )

    def debit(self, p_amount):
        if p_amount >= 0.0:
            try:
                new_balance = (self.balance + self.cashier_facility) - float(p_amount)
                if new_balance >= 0.0:
                    self.balance = new_balance - self.cashier_facility
                else:
                    raise NegativeBalanceException(
                        "FAILED : le seuil de découvert du compte {} est dépassé. Opération refusée.".format(
                            self.account_number)
                    )
            except Exception as e:
                raise e
        else:
            raise NegativeOperationException(
                "FAILED: le montant impliqué dans l'opération sur le compte {} est négatif".format(self.account_number)
            )

    def __add__(self, p_count):
        return self.credit(p_count)

    def __sub__(self, p_count):
        return self.debit(p_count)

    def __eq__(self, other):
        return (self.account_number == other.account_number) and \
               (self.type == other.type)

    def __str__(self):
        if self.balance >= 0.0:
            return "<{}[{}:{}:{:+.2f}:{}:{}]>".format(self.__class__.__name__,
                                                self.account_number,
                                                self.type.value,
                                                self.balance,
                                                self.cashier_facility,
                                                self.paid_threshold)
        else:
            return "<{}[{}:{}:{:-.2f}:{}:{}]>".format(self.__class__.__name__,
                                                self.account_number,
                                                self.type.value,
                                                self.balance,
                                                self.cashier_facility,
                                                self.paid_threshold)

    def __repr__(self):
        return self.__str__()

    def to_dict(self, endpoint):
        data = {
            'id': self.id,
            'account_number': self.account_number,
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
            my_object = Account()

        my_attr_dict = dict(Account)

        for field in my_attr_dict:
            if field in data:
                setattr(my_object, field, data[field])


class PaidAccount(Account):
    __tablename__ = None

    __mapper_args__ = {
        'polymorphic_identity': 'paid_account'
    }

    def __init__(self, **kwargs):
        super(PaidAccount, self).__init__(**kwargs)
        self.type = typeAccount.PAID_ACCOUNT
        # self.benefit = 0.0


class DebitAccount(Account):
    __tablename__ = None

    __mapper_args__ = {
        'polymorphic_identity': 'debit_account'
    }

    def __init__(self, **kwargs):
        super(DebitAccount, self).__init__(**kwargs)
        self.type = typeAccount.DEBIT_ACCOUNT


class NegativeBalanceException(Exception):
    def __init__(self, p_message):
        self.__message = p_message


class NegativeOperationException(Exception):
    def __init__(self, p_message):
        self.__message = p_message


class NegativeCashierFacilityException(Exception):
    def __init__(self, p_message):
        self.__message = p_message


class NegativePaidThresholdException(Exception):
    def __init__(self, p_message):
        self.__message = p_message


if __name__ == "__main__":
    db.metadata.clear()
