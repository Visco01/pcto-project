from flask import redirect, render_template, url_for, flash
from lib.app_def import app
from lib.orm_classes import User
from lib.forms import RegistrationFrom, LoginForm
from lib.db_actions import *


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users = users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
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


if __name__ == '__main__':
    #run flask app
    app.run(host='0.0.0.0', debug=True)
