# coding: utf-8

from datetime import datetime
from webapp.extensions import db


class AccountAgiosHistory(db.Model):
    __tablename__: "account_agios_history"

    id = db.Column(db.Integer, primary_key=True)  # Integer
    account_check_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)  # Varchar(20)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), index=True)
    _cashier_facility_attime = db.Column("cashier_facility", db.Float(12, 2), default=0)
    _paid_threshold_attime = db.Column("paid_threshold", db.Float(12, 2), default=0)
    operation_amount = db.Column(db.Float(12, 2), default=0)
    balance_daily = db.Column(db.Float(12, 2), default=0)

    def __init__(self, **kwargs):
        super(AccountAgiosHistory, self).__init__(**kwargs)
        self.balance_daily = 0.0
        self.cashier_facility_attime = 0.0
        self.paid_threshold_attime = 0.0
        self.operation_date = datetime.utcnow()
        self.operation_amount = 0.0

    def __str__(self):
        return "<AccountHistory[{} : {} : {}]>".format(self.id,
                                           self.operation_date.strftime("%d-%m-%Y"),
                                           self.account_id)

    def __repr__(self):
        return self.__str__


if __name__ == "__main__":
    ha = AccountHistory(id=1,
                        account_id=1)

    print(ha)

