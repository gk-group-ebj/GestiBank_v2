# coding: utf-8

from datetime import datetime, timedelta
from sqlalchemy import func

from flask import url_for

from webapp.bdd.models.accounts import Account, DebitAccount, UnexpectedAccountTypeException, NoAccountIdException
from webapp.bdd.models import AGIOS_RATE
from webapp.bdd.models.utils import PaginatedAPIMixin, store_data
from webapp.bdd.models.transactions_history import typeTransaction, TransactionHistory

from webapp.extensions import db


class DebitAccountAgiosHistory(db.Model, PaginatedAPIMixin):
    __tablename__: "debit_account_agios_history"
    __table_args__ = {
        'extend_existing': True
    }

    __agios_rate = AGIOS_RATE

    id = db.Column(db.Integer, primary_key=True)  # Integer
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), index=True)
    agios_check_date = db.Column(db.DateTime, default=datetime.utcnow(), index=True)  # Varchar(20)
    cashier_facility_attime = db.Column(db.Float(12, 2), default=0)
    balance_attime = db.Column(db.Float(12, 2), default=0)
    daily_agios = db.Column(db.Float(12, 2), default=0)

    # Dictionnaire pour le calcul trimestriel des agios à date fixe
    DICT_DATES = {0: '01-01',
                  1: '04-01',
                  2: '07-01',
                  3: '10-01'}

    def __init__(self, **kwargs):
        super(DebitAccountAgiosHistory, self).__init__(**kwargs)
        if self.agios_check_date is None:
            self.agios_check_date = datetime.utcnow()

        if self.daily_agios is None:
            self.daily_agios = 0.0

        if self.account_id is not None:
            account = Account.query.get(self.account_id)
            if account:
                if isinstance(account, DebitAccount):
                    if self.balance_attime is None:
                        self.balance_attime = account.balance

                    if self.cashier_facility_attime is None:
                        self.cashier_facility_attime = account.cashier_facility
                else:
                    raise UnexpectedAccountTypeException(
                        "FAILED: le compte {} est de type {}. Il n'est pas soumis au calcul d'Agios".format(
                            account.account_number, account.type)
                    )
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
            'account_id': self.account_id,
            '_links': {
                'self': url_for(endpoint, id=self.id)
            }
        }
        return data

    def __str__(self):
        return "<{}[{} : {} : {} : {} : {} : {}]>" \
            .format(self.__class__.__name__,
                    self.id,
                    self.account_id,
                    self.agios_check_date.strftime("%d-%m-%Y"),
                    self.cashier_facility_attime,
                    self.balance_attime,
                    self.daily_agios)

    def __repr__(self):
        return self.__str__()

    def calculate_daily_agios(self):
        if self.balance_attime < 0:
            absolute_balance = abs(self.balance_attime)
            if absolute_balance > self.cashier_facility_attime:
                self.daily_agios = absolute_balance - self.cashier_facility_attime
                # Ajouter une ligne dans la table des historiques agios si daily_agios est valorisé
                store_data(self)

    @staticmethod
    def calculate_trimester_agios(self, p_amount):
        return (float(p_amount) * AGIOS_RATE) / (100.0 * 365.0)

    @staticmethod
    def update_trimester_agios(date_jour=datetime.utcnow()):
        date_mois_jour = date_jour.strftime('%m-%d')
        if date_mois_jour in DebitAccountAgiosHistory.DICT_DATES.values():
            # Calculer le mois / jour
            key_debut = list(DebitAccountAgiosHistory.DICT_DATES.values()).index(date_mois_jour) - 1
            end_interval = date_jour - timedelta(days=1)
            str_end_interval = end_interval.strftime('%Y-%m-%d')
            if key_debut >= 0:
                y = date_jour.year
                start = DebitAccountAgiosHistory.DICT_DATES[key_debut]
            else:
                y = date_jour.year - 1
                start = DebitAccountAgiosHistory.DICT_DATES[len(DebitAccountAgiosHistory.DICT_DATES) - 1]

            str_start_interval = str(y) + "-" + start

            list_amounts = DebitAccountAgiosHistory.query.with_entities(DebitAccountAgiosHistory.account_id, func.sum(
                DebitAccountAgiosHistory.daily_agios)). \
                filter(DebitAccountAgiosHistory.agios_check_date.between(str_start_interval, str_end_interval)). \
                group_by(DebitAccountAgiosHistory.account_id).all()

            for i in list_amounts:
                debit_account_id = i[0]
                trimester_agios = DebitAccountAgiosHistory.calculate_trimester_agios(i[1])
                t = TransactionHistory(
                    operation_date=date_jour,
                    account_id=debit_account_id,
                    operation_amount=trimester_agios,
                    type=typeTransaction.DEBIT_AGIOS
                )

                d = Account.query.get(t.account_id)
                t.balance_attime = d.debit(t.operation_amount)
                store_data(d, t)


if __name__ == "__main__":
    # from webapp.bdd.models.utils import store_data
    # from datetime import datetime, timedelta
    # from webapp.bdd.models.transactions_history import typeTransaction

    o1 = DebitAccountAgiosHistory(account_id=1,
                                  agios_check_date=datetime.strptime("11-10-2018", "%d-%m-%Y"),
                                  balance_attime=-300.0,
                                  cashier_facility_attime=200.0)

    o2 = DebitAccountAgiosHistory(account_id=1,
                                  agios_check_date=datetime.strptime("01-04-2019", "%d-%m-%Y"),
                                  balance_attime=-300.0,
                                  cashier_facility_attime=200.0)

    o3 = DebitAccountAgiosHistory(account_id=1,
                                  agios_check_date=datetime.strptime("01-05-2019", "%d-%m-%Y"),
                                  balance_attime=-400.0,
                                  cashier_facility_attime=200.0)

    o4 = DebitAccountAgiosHistory(account_id=1,
                                  agios_check_date=datetime.strptime("01-06-2019", "%d-%m-%Y"),
                                  balance_attime=-400.0,
                                  cashier_facility_attime=400.0)

    o5 = DebitAccountAgiosHistory(account_id=1,
                                  agios_check_date=datetime.strptime("01-07-2019", "%d-%m-%Y"),
                                  balance_attime=-300.0,
                                  cashier_facility_attime=200.0)

    o2 = DebitAccountAgiosHistory(account_id=3,
                                  agios_check_date=datetime.strptime("01-03-2019", "%d-%m-%Y"),
                                  balance_attime=-300.0,
                                  cashier_facility_attime=200.0)

    o3 = DebitAccountAgiosHistory(account_id=5,
                                  agios_check_date=datetime.strptime("01-03-2019", "%d-%m-%Y"),
                                  balance_attime=-300.0,
                                  cashier_facility_attime=200.0)
