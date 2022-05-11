from flask import Blueprint
from .forms import NewCourseForm
from app.lib.db_actions import *
from flask_login import current_user, login_required
from flask import render_template, url_for, redirect

teachers = Blueprint('teachers', __name__)

@teachers.route('/dashboard')
@login_required
def dashboard():
    checkUser()
    return render_template('teachers/dashboard.html', courses=get_all_courses_from_teacher(current_user.id_user))

@teachers.route('/profile')
@login_required
def profile():
    checkUser()
    return render_template('teachers/profile.html')


@teachers.route('/new', methods=['GET', 'POST'])
@login_required
def newCourse():
    checkUser()
    form = NewCourseForm()
    form.category.choices = [(category.id_category, category.c_name) for category in get_all_categories()]

    if form.validate_on_submit():
        insert_course(form)
        return redirect(url_for('teachers.profile'))
    return render_template('teachers/create_course.html', form=form)

# Reinderizza tutti gli studenti al loro profilo
def checkUser():
    if get_student_by_id(current_user.id_user):
        return redirect(url_for('main.index'))
