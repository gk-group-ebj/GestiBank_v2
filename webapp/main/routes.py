from flask_login import login_required, current_user
from werkzeug.utils import redirect

from webapp.main import bp
from flask import render_template, request, session
from webapp.bdd.models.users import Manager, User
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

    list_manager = db.session.query(Manager.id, Manager.firstname).all()
    return render_template("admin/requests.html",
                           title_content='List of requests',
                           requests=requests,
                           list_manager=list_manager)


"""
@bp.route('/manager/<int:id>/requests')
@login_required
def requests_by_manager(id):
    OpenAccountRequest.query.get(OpenAccountRequest.manager_id == '0').all()

    list_manager = db.session.query(Manager.id, Manager.firstname).all()
    return render_template("admin/requests.html",
                           title_content='List of requests',
                           requests=requests,
                           list_manager=list_manager)
"""


@bp.route('/request/<id>/set_manager', methods=['GET', 'POST'])
@bp.endpoint('set_manager')
def set_manager(id):
    req = OpenAccountRequest.query.get(id)
    req.manager_id = request.form['manager_id']
    db.session.commit()
    return redirect(request.referrer, id=id)


@bp.route('/client')
@bp.route('/client/home')
@bp.route('/client/index')
@login_required
def index_client():
    return render_template('client/index.html')


@bp.route('/event')
def event():
    return render_template('main/event.html')


@bp.route('/language/', methods=['GET', 'POST'])
@bp.endpoint('set_language')
def set_language():
    session['language'] = request.form['lang']
    return redirect(request.referrer)
