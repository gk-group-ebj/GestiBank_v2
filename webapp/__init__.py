from flask import Flask

from webapp.bdd.models.accounts import Account, PaidAccount, DebitAccount
from webapp.bdd.models.users import User, Admin, Manager, Client
from webapp.extensions import db, migrate, babel
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

        app_return.register_blueprint(auth_bp)
        app_return.register_blueprint(main_bp)
        app_return.register_blueprint(api_bp)

        @app_return.shell_context_processor
        def inject_conf_var():
            return {'db': db,
                    'User': User, "Admin": Admin, "Manager": Manager, "Client": Client,
                    "Account": Account, "PaidAccount": PaidAccount, "DebitAccount": DebitAccount
                    }

    return app_return
