from flask import render_template, request, flash, redirect, url_for
from werkzeug.urls import url_parse

from webapp import Admin
from webapp.auth import bp
from webapp.auth.forms import RegistrationForm, LoginForm
from flask_babel import _
from flask_login import login_user


@bp.route('/login/admin', methods=['GET', 'POST'])
@bp.route('/login/manager', methods=['GET', 'POST'])
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if request.path == '/login/admin':
            return render_template('admin/index.html')
    render_template("auth/login.html", title=_('Login'), form=form)


@bp.route('/register/manager', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('auth/register.html', form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    return None


@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    return None
