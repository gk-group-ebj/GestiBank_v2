# coding: utf-8

from datetime import datetime
from enum import Enum
from sqlalchemy.ext.hybrid import hybrid_property

from webapp.bdd.models import BANK_THRESHOLD, PAID_RATE, AGIOS_RATE
from webapp.extensions import db


# Compte courant sans autorisation de découvert
class typeAccount(Enum):
    CURRENT_ACCOUNT = "Compte Courant"
    DEBIT_ACCOUNT = "Compte Autorisation de découvert"
    PAID_ACCOUNT = "Compte Rémunéré"


class Account(db.Model):
    __tablename__: "account"

    id = db.Column(db.Integer, primary_key=True)  # Integer
    account_number = db.Column(db.Integer, nullable=False, index=True, unique=True)  # Varchar(40)
    type = db.Column(db.Enum(typeAccount), nullable=False,
                     server_default=typeAccount.CURRENT_ACCOUNT.name)  # Enum typeAccount
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)  # Varchar(20)
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
        self.balance = 0.0
        self.cashier_facility = 0.0
        self.paid_threshold = 0.0
        self.creation_date = datetime.utcnow()
        self.type = typeAccount.CURRENT_ACCOUNT

    @hybrid_property
    def cashier_facility(self):
        return self._cashier_facility

    @cashier_facility.setter
    def cashier_facility(self, p_cashier):
        if p_cashier >= 0.0:
            self.cashier_facility = float(p_cashier)
        else:
            raise NegativeCashierFacilityException(
                "FAILED: le montant de découvert autorisé pour le compte {} est négatif ".format(self.account_number)
            )

    @hybrid_property
    def paid_threshold(self):
        return self._paid_threshold

    @paid_threshold.setter
    def paid_threshold(self, p_paid):
        if p_paid >= 0.0:
            self.paid_threshold = float(p_paid)
        else:
            raise NegativePaidThresholdException(
                "FAILED: le seuil de rémunération pour le compte {} est négatif ".format(self.account_number)
            )


    # Methods
    def credit(self, p_count):
        if p_count >= 0.0:
            self.balance = self.balance + float(p_count)
        else:
            raise NegativeOperationException(
                "FAILED: le montant de l'opération sur le compte {} est négatif".format(self.account_number)
            )

    def debit(self, p_count):
        if p_count >= 0.0:
            try:
                new_balance = (self.balance + self.cashier_facility) - float(p_count)
                if new_balance >= 0.0:
                    self.balance = new_balance - self.cashier_facility
                else:
                    raise NegativeBalanceException(
                        "FAILED : le seuil de découvert du compte {} est dépassé.".format(self.account_number)
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
        super(PaidAccount, self).__init__(**kwargs)
        self.type = typeAccount.PAID_ACCOUNT
        self.benefit = 0.0


class DebitAccount(Account):
    __tablename__ = None

    __mapper_args__ = {
        'polymorphic_identity': 'debit_account'
    }

    __agios_rate = AGIOS_RATE

    def __init__(self, **kwargs):
        super(DebitAccount, self).__init__(**kwargs)
        self.type = typeAccount.DEBIT_ACCOUNT
        ##self.agios = dict()
        self.agios = {
            datetime.utcnow().strftime("%d-%m-%Y"): 0.0
        }

    def agios(self, p_key_strdate, p_val_newbalance):
        if self.agios.get(p_key_strdate):
            self.agios.update(p_key_strdate, p_val_newbalance)
        else:
            self.agios[p_key_strdate] = p_val_newbalance

    # TODO How to debit agios on balance
    def debitagios(self, p_count):
        self.balance = self.balance - X

    # TODO a finir
    def credit(self, p_count):
        if p_count >= 0.0:
            new_balance = (self.balance + self.cashier_facility) + float(p_count)
            self.balance = new_balance - self.cashier_facility
            if new_balance >= 0.0:
                self.agios(p_key_strdate, 0.0)
            else:
                daily_agios = -1 * new_balance
                self.agios(p_key_strdate, daily_agios)

        else:
            raise NegativeOperationException(
                "FAILED: le montant impliqué dans l'opération sur le compte {} est négatif".format(self.account_number)
            )

    # TODO a finir
    def debit(self, p_count):
        if p_count >= 0.0:
            new_balance = (self.balance + self.cashier_facility) - float(p_count)
            self.balance = new_balance - self.cashier_facility
            if new_balance >= 0.0:
                self.agios(p_key_strdate, 0.0)
            else:
                daily_agios = -1 * new_balance
                self.agios(p_key_strdate, daily_agios)
        else:
            raise NegativeOperationException(
                "FAILED: le montant impliqué dans l'opération sur le compte {} est négatif".format(self.account_number)
            )

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
    # Context
    # DebitAccount avec cash_facility = 400
        # 01/01 solde = 0, aucune opération
        # 02/01 debit de 200 ==> solde = -200 et new_balance = 200
        # 03/01 debit de 300 ==> solde = -500 et new_balance = -100 ==> agios[03/01] = 100    (créer en débit)
        # 03/01 debit de 100 ==> solde = -600 et new_balance = -200 ==> agios[03/01] = 200    (écraser en débit)
        # 04/01 credit de 100 ==> solde = -500 et new_balance = -100 ==> agios[04/01] = 100    (créer en crédit)
        # 04/01 credit de 200 ==> solde = -300 et new_balance = +100 ==> agios[04/01] = 0      (écraser en credit à 0 car new_balance >= 0)

    pass
