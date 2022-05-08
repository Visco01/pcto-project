from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from app.lib.db_actions import *
from app.lib.forms import LoginForm
from flask_login import login_user, current_user, logout_user

authentication_blueprint = Blueprint('authentication', __name__)

@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('private'))

    form = LoginForm()

    if form.validate_on_submit():

        user = get_user_by_email(form.email.data)

        if(not user):
            flash("Account non registrato", 'danger')
            return redirect(url_for('authentication.login'))

        #! HARDCODED LOGIN (creare utente)
        #? Email:    stefano.calzavara@unive.it
        #? Password: password
        if(user.email == 'visconti373@gmail.com'): # email arbitraria
            login_user(user, remember=form.rememberMe.data)
            flash("Accesso come professore", 'success')
            return redirect(url_for('private'))

        student = get_student_by_id(user.id_user)

        if bcrypt.check_password_hash(student.password, form.password.data):
            login_user(user, remember=form.rememberMe.data)

            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('private'))
        else:
            flash('Accesso negato', 'danger')

    return render_template('login.html', form = form)


@authentication_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
