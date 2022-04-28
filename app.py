from flask import Flask, make_response, redirect, render_template, request, url_for, flash
# import di flask login
from flask_login import *
# import from lib/conn -> connessione al database
from lib.conn import get_engine

# importa form
from lib.forms import RegistrationFrom, LoginForm

import os

import sqlalchemy
import lib.orm_classes

app = Flask(__name__)

# inizializza flask_login
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    # costruttore di classe
    def __init__(self, id, email, pwd):
        self.id = id
        self.email = email
        self.pwd = pwd


def get_user_by_email(email):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM users WHERE email = ?', email)
    user = rs.fetchone()
    conn.close()
    return User(user.id, user.email, user.pwd)


@login_manager.user_loader
def load_user(user_id):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM users WHERE id_user = ?', user_id)
    user = rs.fetchone()
    conn.close()
    return User(user.id, user.mail, user.pwd)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('private'))
        
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM users')
    users = rs.fetchall()
    conn.close()
    return render_template('index.html', user=users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form = form)
    """ 
    if request.method == 'POST':
        conn = engine.connect()
        rs = conn.execute('SELECT pwd FROM students WHERE email = ?', [
                          request.form['user']])
        real_pwd = rs.fetchone()
        conn.close()

        if (real_pwd is not None):
            # resto della logica di autenticazione
            pass
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

    if request.form['pass'] == real_pwd['pwd']:
        user = get_user_by_email(request.form['user'])
        login_user(user)
        return redirect(url_for('private'))
    else:
        return redirect(url_for('index')) """

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationFrom()
    if form.validate_on_submit():
        flash(f'Account creato, {form.firstName.data}', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/private')
@login_required
def private():
    conn = engine.connect()
    users = conn.execute('SELECT * FROM users')
    resp = make_response(render_template('private.html', user=users))
    conn.close()
    return resp


if __name__ == '__main__':
    # inizializza engine db
    engine = get_engine()
    # fai partire l'applicazione Flask
    app.run(host='0.0.0.0', debug=True)
