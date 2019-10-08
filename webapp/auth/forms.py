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


""" formulaire de demande de connexion"""


class RegistrationForm(FlaskForm):
    lastname = StringField(_l('Lastname'), validators=[DataRequired()])
    firstname = StringField(_l('Firstname'), validators=[DataRequired()])
    phone = StringField(_l('Phone'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    nb_street = StringField(_l('Street Number'), validators=[DataRequired()])
    street = StringField(_l('Street Name'), validators=[DataRequired()])
    zip = StringField(_l('Zip code'), validators=[DataRequired()])
    city = StringField(_l('City'), validators=[DataRequired()])
    nb_child = StringField(_l('Nombre of child'), validators=[DataRequired()])
    marital_statue = RadioField(_l('Marital Status'), choices=[('Single',_l('Single')),('Maried', _l('Maried')),('Widowed', _l('Widowed')),('Divorced',_l('Divorced'))],
                               validators=[DataRequired()])


    submit = SubmitField(_l('Register'))