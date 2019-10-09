from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email
from flask_babel import lazy_gettext as _l


""" formulaire de connexion au compte de la banque"""

# a préciser quelles sont les information demandé pour la connexion
class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


""" formulaire de creation d'un manager par l'admin """

class RegistrationForm(FlaskForm):
    mle = StringField(_l('Matricule'), validators=[DataRequired()])
    lastname = StringField(_l('Lastname'), validators=[DataRequired()])
    firstname = StringField(_l('Firstname'), validators=[DataRequired()])
    username = StringField(_l('Username'), validators=[DataRequired()])
    phone = StringField(_l('Phone'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])


    submit = SubmitField(_l('Register'))
