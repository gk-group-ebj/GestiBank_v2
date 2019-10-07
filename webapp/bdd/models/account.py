from datetime import datetime
from enum import Enum

from webapp.extensions import db


# Compte courant sans autorisation de découvert
class typeAccount(Enum):
    CURRENT_ACCOUNT = "Compte Courant"
    DEBIT_ACCOUNT = "Comte Autorisation de découvert"
    PAID_ACCOUNT = "Compte Rémunéré"


class Account(db.Model):
    __tablename__: "account"

    id = db.Column(db.Integer, primary_key=True)  # Integer
    account_number = db.Column(db.Integer, index=True, unique=True)  # Varchar(40)
    type = db.Column(db.String(20))  # Varchar(20)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)  # Varchar(20)
    iban = db.Column(db.String(20), unique=True)  # Varchar(20)
    balance = (db.Float(12, 2))  # Varchar(20)

    __mapper_args__ = {
        'polymorphic_identity': 'account',
        'polymorphic_on': type
    }

    def __init__(self):
        self.type = typeAccount.CURRENT_ACCOUNT

    def set_balance(self, p_balance):
        try:
            if float(p_balance) >= 0.0:
                self.balance = float(p_balance)
                # print(f"SUCCESS : Mise à jour du solde du compte {self.__account_number}")
                return self.__balance
            else:
                raise NegativeBalanceException(
                    "FAILED : entrez un montant positif".format(self.get_account_number()))
        except ValueError as e:
            print(e)

    # TODO
    def __str__(self):
        pass

    # TODO
    def __repr__(self):
        pass


class PaidAccount(Account):
    __tablename__ = None

    benefit = (db.Float(12, 2))  # Varchar(20)

    __mapper_args__ = {
        'polymorphic_identity': 'paidaccount'
    }

    def __init__(self):
        self.type = typeAccount.PAID_ACCOUNT


class DebitAccount(Account):
    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': 'debitaccount'
    }

    def __init__(self):
        self.type = typeAccount.DEBIT_ACCOUNT


class NegativeBalanceException(Exception):
    def __init__(self, p_message):
        self.__message = p_message
