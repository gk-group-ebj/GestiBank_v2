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
            user = Admin.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash(_('Invalid username or password'))
                return redirect(url_for('auth.login'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.index')
            return redirect(next_page)
    return render_template('auth/login.html', title=_('Sign In'), form=form)
    render_template("auth/login.html", title=_('Login'), form=form)


@bp.route('/register_Manager', methods=['GET', 'POST'])
@bp.route('/register_Clients', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('auth/register.html', form=form)
