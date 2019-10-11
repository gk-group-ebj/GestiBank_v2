from flask_login import login_required
from werkzeug.utils import redirect

from webapp.main import bp
from flask import render_template, request, session


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


@bp.route('/language/', methods=['GET', 'POST'])
@bp.endpoint('set_language')
def set_language():
    session['language'] = request.form['lang']
    return redirect(request.referrer)
