from flask import render_template, request, flash, redirect, url_for, current_app
from werkzeug.exceptions import abort
from werkzeug.urls import url_parse

from webapp.api.mail.email import send_password_reset_email
from webapp.auth import bp
from webapp.auth.forms import RegistrationForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm, \
    ClientRegistrationForm
from flask_babel import _
from flask_login import current_user, login_user, logout_user, login_required
from webapp.bdd.models.users import User, verify_reset_password_token, UserNotFoundException
from webapp.bdd.models.requests import OpenAccountRequest
from webapp.bdd.models.utils import store_data


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(get_index_url(request.path)))

    form = LoginForm()

    if form.validate_on_submit():
        my_username = form.username.data

        my_user = User.query.filter_by(username=my_username).first_or_404(
            _('ERROR : user with username %(username)s is unknown.', username=my_username.upper())
        )

        if my_user is not None:
            if not my_user.checkpass(form.password_hash.data):
                flash(_(
                    "ERROR : password for user %(username)s is invalid.",
                    username=my_username.upper()))

                abort(message=UserNotFoundException(_(
                    "ERROR : password for user %(username)s is invalid.", username=my_username.upper())),
                    next='auth.login')

                return redirect(url_for('auth.login'))
            else:
                login_user(my_user, remember=form.remember_me.data)

                next_page = request.args.get("next")

                if (not next_page) or (url_parse(next_page).netloc != ''):
                    if my_user.type == "client":
                        next_page = url_for("main.index_client")
                    elif my_user.type == "admin":
                        next_page = url_for("main.index_admin")
                    elif my_user.type == "manager":
                        next_page = url_for("main.index_manager")

                return redirect(next_page)
        else:
            abort(message=_('ERROR : user with username %(username)s is unknown.', username=my_username.upper()),
                  next='auth.login')
    return render_template("auth/login.html", title_content=_('Login'), form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register_client():
    form = ClientRegistrationForm()
    if form.validate_on_submit():
        id_card = form.id_card.data.read()
        proof_of_address = form.proof_of_address.data.read()
        salary = form.salary.data.read()
        open_account_request = OpenAccountRequest(
            lastname=form.lastname.data,
            firstname=form.firstname.data,
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            id_card=id_card,
            proof_of_address=proof_of_address,
            salary=salary
        )
        store_data(open_account_request)
        flash('Félicitation vous avez fait une demande de création de compte.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', title_content=_('Register'), form=form)


@bp.route('/register/manager', methods=['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm()
    return render_template('auth/register_admin.html', title_content=_('Register Manager'), form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for(get_index_url(request.path)))

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        my_email = form.email.data

        my_user = User.query.filter_by(email=my_email).first_or_404(
            _('ERROR : user with email %(email)s is unknown.', email=my_email.upper()))

        if my_user is not None:
            send_password_reset_email(my_user)
            flash(_(
                "%(email)s ==> Un email vous a été envoyez pour réinitialiser votre mot de passe.",
                email=my_email.upper()))
            return redirect(url_for('auth.login'))
        else:
            abort(message=_('ERROR : user with email %(email)s is unknown.', email=my_email.upper()),
                  next='auth.reset_password_request')
    return render_template('auth/reset_password_request.html', title_content=_("Reset your password"), form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for(get_index_url(request.path)))

    my_user_by_token = verify_reset_password_token(token)
    if not my_user_by_token:
        return redirect(url_for(get_index_url(request.path)))

    my_form = ResetPasswordForm()

    if my_form.validate_on_submit():
        my_user_by_token.password_hash = my_form.password_hash.data
        if my_user_by_token.change_pwd:
            flash(
                _("%(username)s, votre mot de passe a été réinitialisé.", username=my_user_by_token.username.upper()))
            return redirect(url_for('auth.login'))
        else:
            flash(_(
                "%(username)s, vous avez saisi le même mot de passe que les %(nb_pwd)s précédent(s). "
                "Veuillez modifier votre mot de passe.",
                username=my_user_by_token.username.upper(),
                nb_pwd=current_app.config['NB_PWD']))

            abort(message=_(
                "%(username)s, vous avez saisi le même mot de passe que les %(nb_pwd)s précédent(s). "
                "Veuillez modifier votre mot de passe.", username=my_user_by_token.username.upper(),
                nb_pwd=current_app.config['NB_PWD']),
                next='auth.reset_password')
    return render_template('auth/reset_password.html', title_content=_("Reset Password"), form=my_form)


@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for(get_index_url(request.path)))


def get_index_url(request_path):
    if 'admin' in request_path:
        return 'main.index_admin'
    elif 'manager' in request_path:
        return 'main.index_manager'
    elif 'client' in request_path:
        return 'main.index_client'
    else:
        return 'main.index'
