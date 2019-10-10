# coding: utf-8

from datetime import datetime, timedelta
from webapp.bdd.models import PAID_RATE, PAID_THRESHOLD
from webapp.extensions import db


class PaidAccountBenefitHistory(db.Model):
    __tablename__: "paid_account_benefit_history"
    __table_args__= {'extend_existing': True}

    __paid_rate = PAID_RATE
    __paid_THRESHOLD = PAID_THRESHOLD

    id = db.Column(db.Integer, primary_key=True)  # Integer
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), index=True)
    paid_check_date = db.Column(db.DateTime, default=datetime.utcnow(), index=True)  # Varchar(20)
    paid_threshold_attime = db.Column("cashier_facility", db.Float(12, 2), default=0)
    balance_daily = db.Column(db.Float(12, 2), default=0)
    daily_paid = db.Column(db.Float(12, 2), default=0)

    def __init__(self, **kwargs):
        super(PaidAccountBenefitHistory, self).__init__(**kwargs)
        if self.paid_check_date is None:
            self.paid_check_date = datetime.utcnow()
        if self.balance_daily is None:
            self.balance_daily = 0.0
        if self.paid_threshold_attime:
            self.paid_threshold_attime = 0.0
        if self.daily_paid is None:
            self.daily_paid = 0.0

    def __str__(self):
        return "<{}}[{} : {} : {} : {} : {} : {}]>" \
            .format(self.__class__.__name__,
                    self.id,
                    self.account_id,
                    self.paid_check_date.strftime("%d-%m-%Y"),
                    self.paid_threshold_attime,
                    self.balance_daily,
                    self.daily_paid)

    def __repr__(self):
        return self.__str__


if __name__ == "__main__":
    pass
