from webapp.main import bp
from flask import render_template
#from flask_login import current_user


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('main/index.html')

@bp.route('/manager/')
def index_manager():
    return render_template('manager/index.html')

#@bp.route('/')
@bp.route('/admin/index')
def index_admin():
    return render_template('admin/index.html')

@bp.route('/client/')
@bp.route('/client/index')
def index_client():
    return render_template('client/index.html')

@bp.route('/event')
def event():
    return render_template('main/event.html')
