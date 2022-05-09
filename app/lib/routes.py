from flask import render_template, url_for, flash, redirect, request
from app import app, bcrypt
from app.lib.models import User
from app.lib.forms import RegistrationFrom, LoginForm, NewCourseForm
from app.lib.db_actions import *
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users = users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('private'))

    form = LoginForm()

    if form.validate_on_submit():

        user = get_user_by_email(form.email.data)

        if(not user):
            flash("Account non registrato", 'danger')
            return redirect(url_for('login'))
        
        #! HARDCODED LOGIN (creare utente)
        #? Email:    stefano.calzavara@unive.it
        #? Password: password
        if(user.email == 'stefano.calzavara@unive.it'): # email arbitraria
            login_user(user, remember=form.rememberMe.data)
            flash("Accesso come professore", 'success')
            return redirect(url_for('teacher'))
        #! ---------------

        student = get_student_by_id(user.id_user)
        
        if bcrypt.check_password_hash(student.password, form.password.data):
            login_user(user, remember=form.rememberMe.data)

            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('student')) # ternary operator
        else:
            flash('Accesso negato', 'danger')

    return render_template('login.html', form = form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('private'))
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
    # Indirizza l'utente verso la sezione corretta
    # Se l'id dell'utente corrente è uno studente, reindirizza a /student, altrimenti a /teacher
    if get_student_by_id(current_user.id_user):
        return redirect(url_for('student'))
    else:
        return redirect(url_for('teacher'))


@app.route('/teacher', methods=['GET', 'POST'])
@login_required
def teacher():
    # Controlla che gli studenti non possano accedere come professori cambiando URL
    if get_student_by_id(current_user.id_user):
        return redirect(url_for('student'))

    form = NewCourseForm()
    # Ottieni categorie da inserire nel menù a tendina
    form.category.choices = [(category.id_category, category.c_name) for category in get_all_categories()]

    if form.validate_on_submit():
        insert_course(form)
        # Pulisci form
        return redirect(url_for('teacher'))

    # Genera template
    return render_template('teacher.html', courses=get_all_courses_from_teacher(current_user.id_user), form=form)

@app.route('/student')
@login_required
def student():
    # Controlla che i professori non possano accedere come studenti cambiando URL
    if get_student_by_id(current_user.id_user) is None:
        return redirect(url_for('teacher'))
    # Genera template
    return render_template('student.html', courses=get_all_course())
