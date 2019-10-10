# coding: utf-8

from datetime import datetime, timedelta

from webapp.bdd.models import AGIOS_RATE
from webapp.bdd.models.utils import PaginatedAPIMixin
from webapp.extensions import db


class DebitAccountAgiosHistory(db.Model, PaginatedAPIMixin):
    __tablename__: "debit_account_agios_history"

    __agios_rate = AGIOS_RATE

    id = db.Column(db.Integer, primary_key=True)  # Integer
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), index=True)
    agios_check_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)  # Varchar(20)
    cashier_facility_attime = db.Column("cashier_facility", db.Float(12, 2), default=0)
    balance_daily = db.Column(db.Float(12, 2), default=0)
    daily_agios = db.Column(db.Float(12, 2), default=0)

    # Dictionnaire pour le calcul trimestriel des agios à date fixe
    DICT_DATES = {0: '01-01',
                  1: '01-04',
                  2: '01-07',
                  3: '01-10'}

    def __init__(self, **kwargs):
        super(DebitAccountAgiosHistory, self).__init__(**kwargs)
        self.agios_check_date = datetime.utcnow()
        self.balance_daily = 0.0
        self.cashier_facility_attime = 0.0
        self.daily_agios = 0.0

    @property
    def __str__(self):
        return "<{}[{} : {} : {} : {} : {} : {}]>" \
            .format(self.__class__.name,
                    self.id,
                    self.account_id,
                    self.agios_check_date.strftime("%d-%m-%Y"),
                    self.cashier_facility_attime,
                    self.balance_daily,
                    self.daily_agios)

    def __repr__(self):
        return self.__str__

    def calculate_daily_agios(self):
        pass

    @staticmethod
    def calculate_trimester_agios(self):
        date_jour = datetime.utcnow()
        date_jour_mois = date_jour.strftime('%d-%m')
        if date_jour_mois in DebitAccountAgiosHistory.DICT_DATES.values:
            # Calculer le jour / mois
            key_debut = DebitAccountAgiosHistory.DICT_DATES.index(date_jour_mois) - 1
            end_interval = date_jour + timedelta(jours=-1)
            str_end_interval = end_interval.strftime('%d-%m-%Y')
            if key_debut >= 0:
                y = date_jour.year
                start = DebitAccountAgiosHistory.DICT_DATES[key_debut]
            else:
                y = date_jour.year - 1
                start = DebitAccountAgiosHistory.DICT_DATES[len(DebitAccountAgiosHistory.DICT_DATES) - 1]

            str_start_interval = start + "-" + str(y)


if __name__ == "__main__":
    pass
