from datetime import datetime

from flask_login import login_required, current_user
from werkzeug.utils import redirect

from webapp import DebitAccountAgiosHistory, Account
from webapp.bdd.models.accounts import typeAccount
from webapp.main import bp
from flask import render_template, request, session, url_for
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
    list_manager = db.session.query(Manager.id, Manager.username).all()
    return render_template("admin/requests.html",
                           title_content='List of requests',
                           requests=requests,
                           list_manager=list_manager)


@bp.route('/manager/<id>/requests')
@login_required
def requests_by_manager(id):
    manager = db.session.query(User).get(int(id))
    print(manager)
    list_req = db.session.query(OpenAccountRequest).filter(OpenAccountRequest.manager_id == id).all()
    return render_template("admin/requests.html",
                           title_content='List of requests',
                           requests=list_req,
                           list_manager=[manager])


@bp.route('/request/<id>/set_manager', methods=['GET', 'POST'])
@bp.endpoint('set_manager')
def set_manager(id):
    req = OpenAccountRequest.query.get(id)
    req.manager_id = int(request.form['manager_id'])
    db.session.commit()
    return redirect(request.referrer)


@bp.route('/clients', methods=['GET', 'POST'])
@login_required
def create_client():
    print(request.form)
    # username = request.form
    # store_data(
    #     User(username=r.username, lastname=r.lastname, firstname=r.firstname, email=r.email, phone=r.phone,
    #          manager_id=r.manager_id)
    # )


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
    print(session['language'])
    return redirect(request.referrer)


@bp.route('/agios/trim', methods=['GET', 'POST'])
@bp.route('/agios/trim/<agios_date>', methods=['GET', 'POST'])
@login_required
def trim_agios(agios_date='2020-01-01'):
    if agios_date is None:
        DebitAccountAgiosHistory.update_trimester_agios()
    else:
        DebitAccountAgiosHistory.update_trimester_agios(datetime.strptime(agios_date, "%Y-%m-%d"))

    return redirect(url_for('main.index_admin'))


@bp.route('/agios/jour', methods=['GET', 'POST'])
@bp.route('/agios/jour/<agios_date>', methods=['GET', 'POST'])
@login_required
def jour_agios(agios_date=datetime.utcnow().strftime("%Y-%m-%d")):
    list_debit_account = db.session.query(Account).filter(Account.type == typeAccount.DEBIT_ACCOUNT.name).all()

    for item in list_debit_account:
        debit_history = DebitAccountAgiosHistory(account_id=item.id, agios_check_date=datetime.strptime(agios_date, "%Y-%m-%d"))
        debit_history.calculate_daily_underthreshold()

    return redirect(url_for('main.index_admin'))
