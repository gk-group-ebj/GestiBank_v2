from flask import Flask

from webapp.bdd.models.model_users import User, Admin, Manager, Client
from webapp.extensions import db, migrate, babel
from webapp.conf.config import Config


from webapp.auth import bp as auth_bp
from webapp.main import bp as main_bp


def create_app(p_config=Config):
    app_return = Flask(__name__)

    with app_return.app_context():
        app_return.debug = True
        app_return.config.from_object(p_config)

        db.init_app(app_return)
        migrate.init_app(app_return, db)

        babel.init_app(app_return)

        app_return.register_blueprint(main_bp)
        app_return.register_blueprint(auth_bp)


        @app_return.shell_context_processor
        def inject_conf_var():
            return {'db': db, 'User': User, "Admin": Admin, "Manager": Manager, "Client": Client }

    return app_return
