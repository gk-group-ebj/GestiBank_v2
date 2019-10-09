from os import path, environ

from sqlalchemy.pool import SingletonThreadPool


class Config(object):
    BASEDIR = path.abspath(path.dirname(__file__))
    SECRET_KEY = environ.get('SECRET_KEY') or 'you-will-never-guess'

    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_PORT = '3306'
    MYSQL_DB = 'gestibank'

    MyDB = environ.get("DB") or "Sqlite"

    if MyDB == "MYSQL":
        SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL") or \
                                  "mysql+mysqlconnector://" + MYSQL_USER + ":" + MYSQL_PASSWORD + "@" + \
                                  MYSQL_HOST + ":" + MYSQL_PORT + "/" + MYSQL_DB


        SQLALCHEMY_ENGINE_OPTIONS = {
            "poolclass": SingletonThreadPool
        }
    else:
        SQLALCHEMY_DATABASE_FILE = path.realpath(path.join(BASEDIR, "..", "bdd", "gestibank.db"))
        SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_ URL') or \
                                  'sqlite:///' + SQLALCHEMY_DATABASE_FILE

        SQLALCHEMY_ENGINE_OPTIONS = {
            "poolclass": SingletonThreadPool,
            "connect_args": {
                'check_same_thread': False
            }
        }

    SQLALCHEMY_TRACK_MODIFICATIONS = False
