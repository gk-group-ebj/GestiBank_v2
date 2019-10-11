from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_babel import gettext as _, lazy_gettext as _l

""" formulaire de connexion au compte de la banque"""


class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password_hash = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


""" formulaire saisie email suite mot de passe oublié"""


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Send email'))


""" formulaire mise à jour du mot de passe"""


class ResetPasswordForm(FlaskForm):
    password_hash = PasswordField(_l('Password'), validators=[DataRequired()])
    confirm_password = PasswordField(_l('Confirm your password'),
                                     validators=[DataRequired(), EqualTo('password_hash', message='Passwords must match')])
    submit = SubmitField(_('Reinit your password'))


""" formulaire de creation d'un manager par l'admin """


class RegistrationForm(FlaskForm):
    mle = StringField(_l('Matricule'), validators=[DataRequired()])
    lastname = StringField(_l('Lastname'), validators=[DataRequired()])
    firstname = StringField(_l('Firstname'), validators=[DataRequired()])
    username = StringField(_l('Username'), validators=[DataRequired()])
    phone = StringField(_l('Phone'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])

    submit = SubmitField(_l('Register'))


class ClientRegistrationForm(FlaskForm):
    firstname = StringField(_l('Firstname'), validators=[DataRequired()])
    lastname = StringField(_l('Lastname'), validators=[DataRequired()])
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    phone = StringField(_l('Phone'), validators=[DataRequired()])
    id_card = FileField(_l('ID card'), validators=[DataRequired()])
    proof_of_address = FileField(_l('Proof of address'), validators=[DataRequired()])
    salary = FileField(_l('Salary'), validators=[DataRequired()])


    submit = SubmitField(_l('Register'))
