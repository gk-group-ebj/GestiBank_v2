from flask_login import login_required

from webapp.main import bp
from flask import render_template
#from flask_login import current_user


@bp.route('/')
@bp.route('/home')
@bp.route('/index')
def index():
    return render_template('main/index.html')


@bp.route('/manager')
@bp.route('/home/manager')
@bp.route('/index/manager')
@login_required
def index_manager():
    return render_template('manager/index.html')


@bp.route('/admin')
@bp.route('/home/admin')
@bp.route('/index/admin')
@login_required
def index_admin():
    return render_template('admin/index.html')


@bp.route('/client')
@bp.route('/home/client')
@bp.route('/index/client')
@login_required
def index_client():
    return render_template('client/index.html')


@bp.route('/event')
@bp.route('/event/admin', methods=['GET', 'POST'], endpoint='event_admin')
@bp.route('/event/manager', methods=['GET', 'POST'], endpoint='event_manager')
@bp.route('/event/client',  methods=['GET', 'POST'], endpoint='event_client')
def event():
    return render_template('main/event.html')
