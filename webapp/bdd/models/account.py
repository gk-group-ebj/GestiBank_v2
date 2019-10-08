# coding: utf-8

from datetime import datetime
from enum import Enum
from sqlalchemy.ext.hybrid import hybrid_property

from webapp.bdd.models import ACCOUNT_THRESHOLD, BANK_THRESHOLD, PAID_RATE, AGIOS_RATE
from webapp.extensions import db


# Compte courant sans autorisation de découvert
class typeAccount(Enum):
    CURRENT_ACCOUNT = "Compte Courant"
    DEBIT_ACCOUNT = "Comte Autorisation de découvert"
    PAID_ACCOUNT = "Compte Rémunéré"


class Account(db.Model):
    __tablename__: "account"

    id = db.Column(db.Integer, primary_key=True)  # Integer
    account_number = db.Column(db.Integer, nullable=False, index=True, unique=True)  # Varchar(40)
    type = db.Column(db.Enum(typeAccount), nullable=False,
                     server_default=typeAccount.CURRENT_ACCOUNT.name)  # Enum typeAccount
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)  # Varchar(20)
    iban = db.Column(db.String(20), unique=True)  # Varchar(20)
    _balance = db.Column("balance", db.Float(12, 2), default=0)  # Varchar(20)

    account_threshold = ACCOUNT_THRESHOLD

    __mapper_args__ = {
        'polymorphic_identity': 'account',
        'polymorphic_on': type
    }

    def __init__(self, **kwargs):
        super(Account, self).__init__(**kwargs)
        self.balance = 0.0
        self.creation_date = datetime.utcnow
        self.type = typeAccount.CURRENT_ACCOUNT

    @hybrid_property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, p_balance):
        try:
            if float(p_balance) >= self.account_threshold:
                self._balance = float(p_balance)
            else:
                raise NegativeBalanceException(
                    "FAILED : entrez un montant positif".format(self.account_number)
                )
        except Exception as e:
            raise e

    # Methods
    def credit(self, p_count):
        self.balance = self.balance + float(p_count)

    def debit(self, p_count):
        try:
            new_balance = self.balance - float(p_count)
            if new_balance >= 0.0:
                self.balance = new_balance
            else:
                raise NegativeBalanceException(
                    "FAILED : le solde du compte {} est négatif.".format(self.account_number)
                    )
        except Exception as e:
            raise e

    def __add__(self, p_count):
        return self.credit(p_count)

    def __sub__(self, p_count):
        return self.debit(p_count)

    def __eq__(self, other):
        return (self.account_number == other.account_number) and \
               (self.type == other.type)

    def __str__(self):
        if self.balance >= self.account_threshold:
            return "<Account[{}:{}:{:+.2f}]>".format(self.account_number,
                                                     self.type.value,
                                                     self.balance)
        else:
            return "<Account[{}:{}:{:-.2f}]>".format(self.account_number,
                                                     self.type.value,
                                                     self.balance)

    def __repr__(self):
        return self.__str__()


class PaidAccount(Account):
    __tablename__ = None

    __mapper_args__ = {
        'polymorphic_identity': 'paid_account'
    }

    __paid_rate = PAID_RATE
    __bank_threshold = BANK_THRESHOLD

    benefit = db.Column(db.Float(12, 2), default=0)  # Varchar(20)

    def __init__(self, **kwargs):
        super(PaidAccount, self).__init__()
        self.type = typeAccount.PAID_ACCOUNT
        self.benefit = 0.0


class DebitAccount(Account):
    __tablename__ = None

    __mapper_args__ = {
        'polymorphic_identity': 'debit_account'
    }

    __agios_rate = AGIOS_RATE

    cashier_facility = db.Column(db.Boolean, default=False)  # BoleanÒ

    def __init__(self):
        super(DebitAccount, self).__init__()
        self.type = typeAccount.DEBIT_ACCOUNT
        self.cashier_facility = False
        self.agios = dict()

    def debit(self, p_count):
        try:
            new_balance = (self.balance + self.cashier_facility) - float(p_count)
            if new_balance >= 0.0:
                self.balance = new_balance - self.cashier_facility
            else:
                raise NegativeBalanceException(
                    "FAILED : le decouvert autorisé pour le compte {} est atteint.".format(self.account_number)
                    )
        except Exception as e:
            raise e


class NegativeBalanceException(Exception):
    def __init__(self, p_message):
        self.__message = p_message
