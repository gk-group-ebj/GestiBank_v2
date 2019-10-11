from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel, lazy_gettext as _l
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()

babel = Babel()
bootstrap = Bootstrap()

login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')

mail = Mail()
