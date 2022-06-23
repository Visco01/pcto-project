import json
from flask import Blueprint, request, jsonify

from app.lib.models import Building, Classroom
from app.lib.models_schema import ClassroomSchema
from .forms import NewCourseForm, NewLessonBase, NewLessonSchedule, NewLessonSingle, NewLessonSingle
from app.lib.db_actions import *
from flask_login import current_user, login_required
from flask import render_template, url_for, redirect
from .utils import teacher_required
import simplejson as json
teachers = Blueprint('teachers', __name__)

# ROUTES


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


@teachers.route('/description/<id_course>', methods=['GET', 'POST'])
@login_required
@teacher_required
def courseDescription(id_course):
    data_string = request.form.get('a')
    data = {}

    if data_string:
        data = json.loads(data_string)
        update_course(id_course, data)

    categories_left = get_all_categories()
    category = get_course_category(id_course)
    categories_left.remove(category)

    return render_template('teachers/course_description.html', course=get_course_by_id(id_course), categories=categories_left, this_category=category)


@teachers.route('<id_course>/new_lesson', methods=['GET', 'POST'])
@login_required
@teacher_required
def newLesson(id_course):
    # Contiene: edificio, aula, modalità, descrizione, tasto invia
    lesson_base = NewLessonBase()
    # Contiene: data, ora
    single_lesson = NewLessonSingle()
    # Contiene: data, giorni, ore, numero lezioni
    schedule = NewLessonSchedule()

    lesson_base.building.choices = [(building.id_building, building.b_name) for building in Building.query.all()]

    # Non serve più
    # lesson_base.classroom.choices = [(classroom.id_classroom, classroom.c_name) for classroom in get_classrooms_by_capacity(get_course_by_id(id_course).max_partecipants)]

    for i in range(4):
        schedule.days.append_entry()

    for i in range(5):
        schedule.time_m.append_entry()

    schedule.validate()
    single_lesson.validate()
    print('single')
    print(single_lesson.errors)
    print('schedule')
    print(schedule.errors)
    # Gruppo di lezioni
    if schedule.validate_on_submit():
        create_course_schedule(lesson_base, schedule, id_course)
        # Gruppo di lezioni inserito
        return redirect(url_for('main.lessons', id_course=id_course, path='teacher'))

    # Lezione singola
    if single_lesson.validate_on_submit():
        insert_lesson(lesson_base, single_lesson, id_course)
        # Lezione inserita
        return redirect(url_for('main.lessons', id_course=id_course, path='teacher'))

    # Corso non inserito
    return render_template('teachers/new_lesson.html', id_course=id_course, form_base=lesson_base, form_single=single_lesson, form_schedule=schedule)


# UTILITY


@teachers.route('/getClassrooms/<string:id_building>', methods=['GET', 'POST'])
@login_required
@teacher_required
def getClassrooms(id_building):
    class_schema = ClassroomSchema(many=True)
    classrooms = get_Classrooms_From_Building(id_building)
    return jsonify(class_schema.dump(classrooms))


'''
@teachers.route('<id_course>/new_schedule', methods = ['GET','POST'])
@login_required
@teacher_required
def newSchedule(id_course):
    # Contiene: edificio, aula, modalità, descrizione, tasto invia
    lesson_base = NewLessonBase()
    # Contiene: data, ora
    single_lesson = NewLessonSingle()
    # Contiene: data, giorni, ore, numero lezioni
    schedule = NewLessonSchedule()
    
    
    
    lesson_base.building.choices = [(building.id_building, building.b_name) for building in Building.query.all()]
    lesson_base.classroom.choices = [(classroom.id_classroom, classroom.c_name) for classroom in get_classrooms_by_capacity(get_course_by_id(id_course).max_partecipants)]
'''