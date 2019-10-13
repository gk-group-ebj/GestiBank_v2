# coding: utf-8

from os import path, environ

from sqlalchemy.pool import SingletonThreadPool


class Config(object):
    BASEDIR = path.abspath(path.dirname(__file__))
    SECRET_KEY = environ.get('SECRET_KEY') or 'you-will-never-guess'

    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_PORT = '8889'
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

    # PASSWORD MANAGEMENT
    NB_PWD = 2
    EXPIRES_IN = 600

    # MAIL
    MAIL_SERVER = environ.get('MAIL_SERVER') or "localhost"
    MAIL_PORT = environ.get('MAIL_PORT') or "8025"
    #SMTP SERVER
    # python -m smtpd --debug -n -c DebuggingServer localhost:8025 > webapp/logs/mail.log

    # ADMINS' EMAILS
    ADMINS_EMAIL = "admin@gestibank.com"

    # BABEL PARAM
    BABEL_TRANSLATION_DIRECTORIES = path.realpath(path.join(BASEDIR, "..", "conf", "translations"))
    BABEL_DEFAULT_LOCALE = 'fr'
    LANGUAGES = dict(de="German", en="English", es="Spanish", fr="French")
