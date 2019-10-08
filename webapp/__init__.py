from flask import Flask

from webapp.bdd.models.model_users import User, Admin, Manager, Client
from webapp.extensions import db, migrate
from webapp.conf.config import Config


def create_app(p_config=Config):
    app_return = Flask(__name__)

    with app_return.app_context():
        app_return.debug = True
        app_return.config.from_object(p_config)

        db.init_app(app_return)
        migrate.init_app(app_return, db)

        @app_return.shell_context_processor
        def inject_conf_var():
            return {'db': db, 'User': User, "Admin": Admin, "Manager": Manager, "Client": Client }

    return app_return
