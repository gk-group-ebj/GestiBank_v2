# coding: utf-8

from datetime import datetime, timedelta

from flask import url_for

from webapp.bdd.models import PAID_RATE, PAID_THRESHOLD
from webapp.bdd.models.accounts import Account, PaidAccount, UnexpectedAccountTypeException, NoAccountIdException
from webapp.bdd.models.utils import PaginatedAPIMixin

from webapp.extensions import db


class PaidAccountBenefitHistory(db.Model, PaginatedAPIMixin):
    __tablename__: "paid_account_benefit_history"
    __table_args__ = {
        'extend_existing': True
    }

    __paid_rate = PAID_RATE
    __paid_THRESHOLD = PAID_THRESHOLD

    id = db.Column(db.Integer, primary_key=True)  # Integer
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), index=True)
    paid_check_date = db.Column(db.DateTime, default=datetime.utcnow(), index=True)  # Varchar(20)
    paid_threshold_attime = db.Column("cashier_facility", db.Float(12, 2), default=0)
    balance_attime = db.Column(db.Float(12, 2), default=0)
    daily_paid = db.Column(db.Float(12, 2), default=0)

    def __init__(self, **kwargs):
        super(PaidAccountBenefitHistory, self).__init__(**kwargs)
        if self.paid_check_date is None:
            self.paid_check_date = datetime.utcnow()

        if self.daily_paid is None:
            self.daily_paid = 0.0

        if self.account_id is not None:
            account = Account.query.get(self.account_id)
            if account:
                if isinstance(account, PaidAccount):
                    if self.balance_attime is None:
                        self.balance_attime = account.balance

                    if self.paid_threshold_attime is None:
                        self.paid_threshold_attime = account.paid_threshold
                else:
                    raise UnexpectedAccountTypeException(
                        "FAILED: le compte {} est de type {}. Il n'est pas soumis à une rémunération".format(
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
        return "<{}}[{} : {} : {} : {} : {} : {}]>" \
            .format(self.__class__.__name__,
                    self.id,
                    self.account_id,
                    self.paid_check_date.strftime("%d-%m-%Y"),
                    self.paid_threshold_attime,
                    self.balance_daily,
                    self.daily_paid)

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    # from webapp.bdd.models.utils import store_data
    pass
