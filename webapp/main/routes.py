from webapp.main import bp
from flask import render_template
from flask_login import current_user


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('main/index.html')

@bp.route('/event')
def event():
    return render_template('main/event.html')
