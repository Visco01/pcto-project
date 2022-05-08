from flask import Blueprint
from flask import render_template, url_for, flash, redirect
from app.lib.db_actions import *
from app.lib.forms import RegistrationFrom

register_blueprint = Blueprint('register', __name__)

@register_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('private'))
    form = RegistrationFrom()
    if form.validate_on_submit():

        insert_user(form)

        flash(f'Account creato, {form.firstName.data}', 'success')
        return redirect(url_for('authentication.login'))
    return render_template('register.html', form = form)
