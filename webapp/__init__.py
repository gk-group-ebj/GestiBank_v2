from flask import Flask

from webapp.extensions import db, migrate
from webapp.conf.config import Config

from webapp.main import bp as main_bp


def create_app(p_config=Config):
    app_return = Flask(__name__)

    with app_return.app_context():
        app_return.debug = True
        app_return.config.from_object(p_config)

        db.init_app(app_return)
        migrate.init_app(app_return, db)

        app_return.register_blueprint(main_bp)

    return app_return
