from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
migrate = Migrate()

babel = Babel()
bootstrap = Bootstrap()
