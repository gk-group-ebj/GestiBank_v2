# coding: utf-8

from datetime import datetime, timedelta
from sqlalchemy import func
from flask import url_for

from webapp.bdd.models import BENEFITS_RATE, BENEFITS_THRESHOLD
from webapp.bdd.models.accounts import Account, PaidAccount, UnexpectedAccountTypeException, NoAccountIdException
from webapp.bdd.models.utils import PaginatedAPIMixin, store_data
from webapp.bdd.models.transactions_history import typeTransaction, TransactionHistory
from webapp.extensions import db


class PaidAccountBenefitHistory(db.Model, PaginatedAPIMixin):
    __tablename__: "paid_account_benefits_history"
    __table_args__ = {
        'extend_existing': True
    }

    __benefits_rate = BENEFITS_RATE
    __benefits_threshold = BENEFITS_THRESHOLD

    id = db.Column(db.Integer, primary_key=True)  # Integer
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), index=True)
    benefits_check_date = db.Column(db.DateTime, default=datetime.utcnow(), index=True)  # Varchar(20)
    benefits_threshold_attime = db.Column( db.Float(12, 2), default=0)
    balance_attime = db.Column(db.Float(12, 2), default=0)
    daily_overthreshold = db.Column("amount_over_threshold", db.Float(12, 2), default=0)

    # Date de calcul annuel des interets
    PAID_DATE = "12-31"

    def __init__(self, **kwargs):
        super(PaidAccountBenefitHistory, self).__init__(**kwargs)
        if self.benefits_check_date is None:
            self.benefits_check_date = datetime.utcnow()

        if self.daily_overthreshold is None:
            self.daily_overthreshold = 0.0

        if self.account_id is not None:
            account = Account.query.get(self.account_id)
            if account:
                if isinstance(account, PaidAccount):
                    if self.balance_attime is None:
                        self.balance_attime = account.balance

                    if self.benefits_threshold_attime is None:
                        self.benefits_threshold_attime = account.benefits_threshold
                else:
                    raise UnexpectedAccountTypeException(
                        "FAILED: le compte {} est de type {}. Il n'est pas soumis à un credit d'intérets".format(
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
                    self.benefits_check_date.strftime("%d-%m-%Y"),
                    self.benefits_threshold_attime,
                    self.balance_attime,
                    self.daily_overthreshold)

    def __repr__(self):
        return self.__str__()

    def calculate_daily_overthreshold(self):
        if self.balance_attime > 0:
            absolute_balance = abs(self.balance_attime)
            if self.balance_attime > self.benefits_threshold_attime:
                self.daily_overthreshold = absolute_balance - self.benefits_threshold_attime
                # Remplis le champ dans la table historique des interets si  valorisé
                store_data(self)
        else:
            self.daily_overthreshold = 0.0
            store_data(self)

    @staticmethod
    def calculate_year_benefits(self, p_amount):
        return (float(p_amount)*BENEFITS_RATE) / (100.0*365)

    @staticmethod
    def update_year_benefits(date_jour=datetime.utcnow()):
        date_mois_jour = date_jour.strftime('%m-%d')
        if date_mois_jour == PaidAccountBenefitHistory.PAID_DATE:
            y = date_jour.year
            start_interval = str(y) + "-" + "01-01"
            end_interval = str(y) + "-" + "12-31"

            list_amounts = PaidAccountBenefitHistory.query.with_entities(PaidAccountBenefitHistory.account_id, func.sum(
                PaidAccountBenefitHistory.daily_overthreshold)). \
                filter(PaidAccountBenefitHistory.benefits_check_date.between(start_interval, end_interval)). \
                group_by(PaidAccountBenefitHistory.account_id).all()

            for i in list_amounts:
                paid_account_id = i[0]
                year_benefits = PaidAccountBenefitHistory.calculate_year_benefits(i[1])
                t = TransactionHistory(
                    operation_date=date_jour,
                    account_id=paid_account_id,
                    operation_amount=year_benefits,
                    type=typeTransaction.CREDIT_BENEFIT
                )

                d = Account.query.get(t.account_id)
                t.balance_attime = d.credit(t.operation_amount)
                store_data(d, t)
        else:
            pass

if __name__ == "__main__":
    # from webapp.bdd.models.utils import store_data
    pass
