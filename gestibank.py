from webapp import create_app
from webapp.extensions import db

if __name__ == '__main__':
    db.create_all(app=create_app())
