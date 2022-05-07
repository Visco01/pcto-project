from flask import render_template, url_for, flash, redirect, request
from app import app, bcrypt
from app.lib.models import User, Student, Course
from app.lib.forms import RegistrationFrom, LoginForm, newCourseForm
from app.lib.db_actions import *
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users = users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('student'))

    form = LoginForm()

    if form.validate_on_submit():

        user = get_user_by_email(form.email.data)

        if(not user):
            flash("Account non registrato", 'danger')
            return redirect(url_for('login'))
        
        #! HARDCODED LOGIN
        if(user.email == 'stefano.calzavara@unive.it'):
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

@app.route('/private/<string:type>')
@login_required
def private(type):
    if(type == 'student'):
        return redirect(url_for('student'))
    if(type == 'teacher'):
        return redirect(url_for('teacher'))


@app.route('/teacher')
@login_required
def teacher():
    form = newCourseForm()
    form.category.choices = [(category.id_category, category.c_name) for category in get_all_categories()]
    return render_template('teacher.html', courses=get_all_courses_from_teacher(current_user.id_user), form=form)

@app.route('/student')
@login_required
def student():
    return render_template('student.html', courses=get_all_course())
