from flask import Flask, current_app, request, session

from webapp.bdd.models.account_agios_history import DebitAccountAgiosHistory
from webapp.bdd.models.account_paid_history import PaidAccountBenefitHistory
from webapp.bdd.models.accounts import Account, PaidAccount, DebitAccount
from webapp.bdd.models.requests import OpenAccountRequest
from webapp.bdd.models.transactions_history import TransactionHistory
from webapp.bdd.models.users import User, Admin, Manager, Client, UserPassword
from webapp.extensions import db, migrate, babel, bootstrap, login, _l, mail
from webapp.conf.config import Config

from webapp.auth import bp as auth_bp
from webapp.main import bp as main_bp
from webapp.api import bp as api_bp


def create_app(p_config=Config):
    app_return = Flask(__name__)

    with app_return.app_context():
        app_return.debug = True
        app_return.config.from_object(p_config)

        db.init_app(app_return)
        migrate.init_app(app_return, db)

        babel.init_app(app_return)
        bootstrap.init_app(app_return)

        login.init_app(app_return)

        mail.init_app(app_return)

        app_return.register_blueprint(auth_bp)
        app_return.register_blueprint(main_bp)
        app_return.register_blueprint(api_bp)

        @app_return.context_processor
        def inject_conf_var():
            return dict(
                DEFAULT_LANGUAGE=current_app.config['BABEL_DEFAULT_LOCALE'],
                AVAILABLE_LANGUAGES=current_app.config['LANGUAGES'],
                CURRENT_LANGUAGE=session.get('language',
                                             request.accept_languages.best_match(
                                            current_app.config['LANGUAGES'].keys()))
            )

        @app_return.shell_context_processor
        def inject_conf_var():
            return {'db': db,
                    'User': User, "Admin": Admin, "Manager": Manager, "Client": Client, "UserPassword": UserPassword,
                    "Account": Account, "PaidAccount": PaidAccount, "DebitAccount": DebitAccount,
                    "DebitAccountAgiosHistory": DebitAccountAgiosHistory,
                    "PaidAccountBenefitHistory": PaidAccountBenefitHistory, "TransactionHistory": TransactionHistory,
                    "OpenAccountRequest": OpenAccountRequest
                    }

    return app_return
