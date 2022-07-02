import json
from flask import Blueprint, request, jsonify
from app.lib.models import Building, Classroom
from app.lib.models_schema import ClassroomSchema
from .forms import NewCourseForm, NewLessonBase, NewLessonSingle
from app.lib.db_actions import *
from flask_login import current_user, login_required
from flask import render_template, url_for, redirect, flash
from .utils import teacher_required
import simplejson as json
teachers = Blueprint('teachers', __name__)

#Reinderizza alla schermata dashboard del professore
@teachers.route('/dashboard')
@login_required
@teacher_required
def dashboard():
    return render_template('teachers/dashboard.html', courses=get_all_courses_from_teacher(current_user.id_user))


#Reinderizza alla schermata del profilo privato del professore
@teachers.route('/profile')
@login_required
@teacher_required
def profile():
    return render_template('teachers/profile.html')


#Reinderizza al form di creazione di un nuovo corso
@teachers.route('/new', methods=['GET', 'POST'])
@login_required
@teacher_required
def newCourse():
    form = NewCourseForm()
    form.category.choices = [(category.id_category, category.c_name) for category in get_all_categories()]

    #Validazione del form e inserimento del corso nel database
    if form.validate_on_submit():
        insert_course(form)
        return redirect(url_for('teachers.profile'))
    return render_template('teachers/create_course.html', form=form)


#Reinderizza alla schermata di modifica del corso selezionato
@teachers.route('/edit_course/<id_course>', methods=['GET', 'POST'])
@login_required
@teacher_required
def edit_course(id_course):
    data_string = request.form.get('a')
    data = {}

    if data_string:
        data = json.loads(data_string)
        update_course(id_course, data)

    categories_left = get_all_categories()
    category = get_course_category(id_course)
    categories_left.remove(category)

    return render_template('teachers/course_description.html', course=get_course_by_id(id_course), categories=categories_left, this_category=category)


#Reinderizza alla schermata di creazione di una nuova lezione
@teachers.route('<id_course>/new_lesson', methods=['GET', 'POST'])
@login_required
@teacher_required
def newLesson(id_course):
    # Contiene: edificio, aula, modalità, descrizione, tasto invia
    lesson_base = NewLessonBase()
    # Contiene: data, ora
    single_lesson = NewLessonSingle()

    lesson_base.building.choices = [(building.id_building, building.b_name) for building in Building.query.all()]


    #Validazione del form e controllo di una eventuale sovrapposizione con altre lezioni
    if single_lesson.validate_on_submit():
        if not check_lesson_availability(lesson_base, single_lesson):
            flash('L\' aula inserita è già prenotata', 'danger')
            return render_template('teachers/new_lesson.html', id_course=id_course, form_base=lesson_base, form_single=single_lesson)

        insert_lesson(lesson_base, single_lesson, id_course)
        # Lezione inserita
        return redirect(url_for('main.lessons', id_course=id_course, path='teacher'))

    return render_template('teachers/new_lesson.html', id_course=id_course, form_base=lesson_base, form_single=single_lesson)


#Reinderizza alla schermata di visualizzazione delle lezioni del corso selezionato
@teachers.route('/<int:id_course>/lessons', methods = ['GET','POST'])
@login_required
@teacher_required
def lessons(id_course):
    lessons = get_course_lessons(id_course)

    return render_template('lesson_list.html', course = get_course_by_id(id_course), lessons = lessons)



# UTILITY per Ajax

#Seleziona tutte le aule di una sede (utilizzata nella richiesta AJAX)
@teachers.route('/getClassrooms/<string:id_building>', methods=['GET', 'POST'])
@login_required
@teacher_required
def getClassrooms(id_building):
    class_schema = ClassroomSchema(many=True)
    classrooms = get_classrooms_from_building(id_building)
    return jsonify(class_schema.dump(classrooms))
