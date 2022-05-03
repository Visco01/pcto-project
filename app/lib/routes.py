from flask import render_template, url_for, flash, redirect, request
from app import app, bcrypt
from app.lib.models import User, Student
from app.lib.forms import RegistrationFrom, LoginForm
from app.lib.db_actions import *
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users = users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():

        user = get_user_by_email(form)

        #DA SISTEMARE
        if(not user):
            flash("Account non registrato", 'danger')
            return redirect(url_for('login'))

        student = get_student(user)
        
        if bcrypt.check_password_hash(student.password, form.password.data):
            if(not login_user(user, remember=form.rememberMe.data)):
                print("Utente inattivo")

            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('private')) # ternary operator
        else:
            flash('Accesso negato', 'danger')

    return render_template('login.html', form = form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationFrom()
    if form.validate_on_submit():

        insert_user(form)

        flash(f'Account creato, {form.firstName.data}', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/private')
@login_required
def private():
    return render_template('private.html')
