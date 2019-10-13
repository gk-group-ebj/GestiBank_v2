from flask import Flask, current_app, request, session, render_template, redirect

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

        app_return.register_blueprint(main_bp)
        app_return.register_blueprint(auth_bp)
        app_return.register_blueprint(api_bp)

        # Gestion dans toutes les pages de l'application
        @app_return.context_processor
        def inject_conf_var():
            return dict(
                DEFAULT_LANGUAGE=current_app.config['BABEL_DEFAULT_LOCALE'],
                AVAILABLE_LANGUAGES=current_app.config['LANGUAGES'],
                CURRENT_LANGUAGE=session.get('language',
                                             request.accept_languages.best_match(
                                                 current_app.config['LANGUAGES'].keys()))
            )

        # Redirection de toutes les erreurs vers erreur.html
        @app_return.errorhandler(Exception)
        def http_error_handler(e):
            if request.endpoint:
                return render_template('main/error.html', err=e, next=request.endpoint)
            else:
                return render_template('main/error.html', err=e)

        from werkzeug.exceptions import default_exceptions
        for ex in default_exceptions:
            app_return.register_error_handler(ex, http_error_handler)

        @app_return.shell_context_processor
        def inject_conf_var():
            return {'db': db,
                    'User': User, "Admin": Admin, "Manager": Manager, "Client": Client, "UserPassword": UserPassword,
                    "Account": Account, "PaidAccount": PaidAccount, "DebitAccount": DebitAccount,
                    "DebitAccountAgiosHistory": DebitAccountAgiosHistory,
                    "PaidAccountBenefitHistory": PaidAccountBenefitHistory,
                    "TransactionHistory": TransactionHistory,
                    "OpenAccountRequest": OpenAccountRequest
                    }

        # Gestion de log
        # handler = RotatingFileHandler('logfile.log', maxBytes=10000, backupCount=1)
        # handler.setLevel(logging.INFO)
        # app_return.logger.addHandler(handler)
    return app_return


@babel.localeselector
def get_locale():
    # if the user has set up the language manually it will be stored in the session,
    # so we use the locale from the user settings
    try:
        language = session['language']
    except KeyError:
        language = current_app.config['BABEL_DEFAULT_LOCALE']
    finally:
        return language
