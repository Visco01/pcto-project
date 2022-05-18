import json
from flask import Blueprint, request, jsonify

from app.lib.models import Classroom
from .forms import NewCourseForm, NewLessonForm
from app.lib.db_actions import *
from flask_login import current_user, login_required
from flask import render_template, url_for, redirect
from .utils import teacher_required
import simplejson as json
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

@teachers.route('/description/<id_course>',methods =['GET','POST'])
@login_required
@teacher_required
def courseDescription(id_course):
    data_string = request.form.get('a')
    data = {}

    if data_string:
        data = json.loads(data_string)
        update_course(id_course,data)
    
    categories_left = get_all_categories()
    category = get_course_category(id_course)
    categories_left.remove(category)

    return render_template('teachers/course_description.html',course = get_course_by_id(id_course),categories = categories_left,this_category = category)


@teachers.route('<id_course>/new_lesson', methods = ['GET','POST'])
@login_required
@teacher_required
def newLesson(id_course):

    form = NewLessonForm()
    form.classroom.choices = [(classroom.id_classroom, classroom.c_name) for classroom in get_classrooms_by_capacity(len(get_subscribed_students(id_course)))]

    if form.validate_on_submit():
        insert_lesson(form, id_course)
        return redirect(url_for('main.lessons', id_course = id_course, path = 'teacher'))

    return render_template('teachers/new_lesson.html', form = form)