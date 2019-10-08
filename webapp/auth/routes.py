from flask import render_template
from webapp.auth import bp
from webapp.auth.forms import RegistrationForm



@bp.route('/')
@bp.route('/index', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('auth/register.html', form=form)
