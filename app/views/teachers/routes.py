from flask import Blueprint, request
from .forms import NewCourseForm
from app.lib.db_actions import *
from flask_login import current_user, login_required
from flask import render_template, url_for, redirect
from .utils import teacher_required

teachers = Blueprint('teachers', __name__)

@teachers.route('/dashboard')
@login_required
@teacher_required
def dashboard():
    return render_template('teachers/dashboard.html', courses=get_all_courses_from_teacher(current_user.id_user))

@teachers.route('/profile')
@login_required
@teacher_required
def profile():
    return render_template('teachers/profile.html')


@teachers.route('/new', methods=['GET', 'POST'])
@login_required
@teacher_required
def newCourse():
    form = NewCourseForm()
    form.category.choices = [(category.id_category, category.c_name) for category in get_all_categories()]

    if form.validate_on_submit():
        insert_course(form)
        return redirect(url_for('teachers.profile'))
    return render_template('teachers/create_course.html', form=form)

@teachers.route('description/<id_course>',methods =['GET','POST'])
@login_required
@teacher_required
def courseDescription(id_course):
    data = request.form.get('info')
    print(data)
    if data is not None:
        update_course_description(id_course,data)
    print("here")
    return render_template('teachers/course_description.html',course = get_course_by_id(id_course))
