from flask import Flask

from webapp.bdd.models.model_users import User
from webapp.extensions import db, migrate, babel
from webapp.conf.config import Config
from webapp.auth import bp as auth_bp



def create_app(p_config=Config):
    app_return = Flask(__name__)

    with app_return.app_context():
        app_return.debug = True
        app_return.config.from_object(p_config)

        db.init_app(app_return)
        migrate.init_app(app_return, db)
        app_return.register_blueprint(auth_bp)
        babel.init_app(app_return)

        @app_return.shell_context_processor
        def inject_conf_var():
            return {'db': db, 'User': User}

    return app_return
