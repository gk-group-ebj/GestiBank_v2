from os import path, environ

from sqlalchemy.pool import SingletonThreadPool


class Config(object):
    BASEDIR = path.abspath(path.dirname(__file__))

    SQLALCHEMY_DATABASE_FILE = path.realpath(path.join(BASEDIR, "..", "bdd", "gestibank.db"))

    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL") or \
        "sqlite:///" + SQLALCHEMY_DATABASE_FILE

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "poolclass": SingletonThreadPool,
        "connect_args": {
            "check_same_thread": False
        }
    }
