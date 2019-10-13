from flask_login import login_required
from werkzeug.utils import redirect

from webapp.main import bp
from flask import render_template, request, session
from webapp.bdd.models.users import Manager
from webapp.bdd.models.requests import OpenAccountRequest

from webapp.extensions import db


@bp.route('/')
@bp.route('/home')
@bp.route('/index')
def index():
    return render_template('main/index.html')


@bp.route('/manager')
@bp.route('/manager/home')
@bp.route('/manager/index')
@login_required
def index_manager():
    return render_template('manager/index.html')


@bp.route('/admin')
@bp.route('/admin/home')
@bp.route('/admin/index')
@login_required
def index_admin():
    return render_template('admin/index.html')


@bp.route('/admin/requests')
@login_required
def requests():
    requests = OpenAccountRequest.query.filter(OpenAccountRequest.manager_id == '0').all()
    list_manager =  db.session.query(Manager.id, Manager.firstname).all()
    return render_template("admin/requests.html",
                           title='List of requests',
                           requests=requests,
                           list_manager=list_manager)

@bp.route('/admin/set_manager', methods=['GET', 'POST'])
@bp.endpoint('set_manager')
def set_manager():
    o = request.form
    print(o)
    return redirect(request.referrer)

@bp.route('/client')
@bp.route('/client/home')
@bp.route('/client/index')
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
