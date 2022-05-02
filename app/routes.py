from flask import render_template, url_for, flash, redirect
from app import app
from app.lib.orm_classes import User
from app.lib.forms import RegistrationFrom, LoginForm
from app.lib.db_actions import insert_user


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users = users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'test@test.com' and form.password.data == 'password':
            flash('Accesso consentito!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Accesso negato', 'danger')
    return render_template('login.html', form = form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationFrom()
    if form.validate_on_submit():
        user = User(first_name=form.firstName.data, last_name=form.lastName.data, birth_date=form.dob.data, email=form.email.data)
        insert_user(user)

        flash(f'Account creato, {form.firstName.data}', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form = form)