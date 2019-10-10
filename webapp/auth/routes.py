from flask import render_template, request, flash, redirect, url_for
from werkzeug.urls import url_parse

from webapp import Admin
from webapp.auth import bp
from webapp.auth.forms import RegistrationForm, LoginForm
from flask_babel import _
from flask_login import current_user, login_user, logout_user, login_required
from webapp.bdd.models.users import User, Client, Admin, Manager


@bp.route('/login/admin', methods=['GET', 'POST'])
@bp.route('/login/manager', methods=['GET', 'POST'])
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():
        if request.path == '/login/admin':
            return render_template('admin/index.html')
        elif request.path == '/login/manager':
            return render_template('manager/index.html')
        else:
            client = Client.query.filter_by(username = form.username.data).first()

            if client is None or not client.checkpass(form.password_hash.data):
                flash('Login ou mot de passe invalide')
                return redirect(url_for('auth.login'))
            login_user(client, remember = form.remember_me.data)
            return redirect(url_for('main.index_client'))
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).nextloc != '':
                next_page = url_for('main.index')
            return redirect(next_page)

    return render_template("auth/login.html", title=_('Login'), form=form)


@bp.route('/register/manager', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('auth/register.html', form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    return None


@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('main.index'))
