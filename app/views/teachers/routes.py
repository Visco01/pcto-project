import json
from flask import Blueprint, request, jsonify, abort
from app.lib.models import Building
from app.lib.models_schema import ClassroomSchema
from .forms import NewCourse_Form, NewLesson_Form
from app.lib.db_actions import *
from flask_login import current_user, login_required
from flask import render_template, url_for, redirect, flash
from .utils import teacher_required
import simplejson as json
teachers = Blueprint('teachers', __name__)

@teachers.route('/dashboard')
@login_required
@teacher_required
def dashboard():
    """Reinderizza alla schermata dashboard del professore"""
    
    return render_template('teachers/dashboard.html', courses=get_all_courses_from_teacher(current_user.id_user))


@teachers.route('/profile')
@login_required
@teacher_required
def profile():
    """Reinderizza alla schermata del profilo privato del professore"""
    
    return render_template('teachers/profile.html')


@teachers.route('/new_course', methods=['GET', 'POST'])
@login_required
@teacher_required
def newCourse():
    """Reinderizza al form di creazione di un nuovo corso"""
    
    form = NewCourse_Form()
    form.category.choices = [(category.id_category, category.c_name) for category in get_all_categories()]

    #Validazione del form e inserimento del corso nel database
    if form.validate_on_submit():
        insert_course(form)
        return redirect(url_for('teachers.profile'))
    return render_template('teachers/create_course.html', form=form)


@teachers.route('/edit_course/<int:id_course>', methods=['GET', 'POST'])
@login_required
@teacher_required
def edit_course(id_course):
    """Reinderizza alla schermata di modifica del corso selezionato"""
    
    data_string = request.form.get('a')
    data = {}

    if data_string:
        data = json.loads(data_string)
        update_course(id_course, data)

    categories_left = get_all_categories()
    category = get_course_category(id_course)
    categories_left.remove(category)

    return render_template('teachers/course_description.html', course=get_course_by_id(id_course), categories=categories_left, this_category=category)


@teachers.route('<int:id_course>/new_lesson', methods=['GET', 'POST'])
@login_required
@teacher_required
def newLesson(id_course):
    """Reinderizza alla schermata di creazione di una nuova lezione"""
    
    if current_user.id_user:
        abort(404)
    # Contiene: edificio, aula, modalità, descrizione, tasto invia
    new_lesson = NewLesson_Form()

    new_lesson.building.choices = [(building.id_building, building.b_name) for building in Building.query.all()]


    #Validazione del form e controllo di una eventuale sovrapposizione con altre lezioni
    if new_lesson.validate_on_submit():
        if not check_lesson_availability(new_lesson):
            flash('L\' aula inserita è già prenotata', 'danger')
            return render_template('teachers/new_lesson.html', id_course=id_course, form=new_lesson)

        insert_lesson(new_lesson, id_course)
        # Lezione inserita
        return redirect(url_for('teachers.lessons', id_course=id_course))

    return render_template('teachers/new_lesson.html', id_course=id_course, form=new_lesson)


@teachers.route('/<int:id_course>/lessons', methods = ['GET','POST'])
@login_required
@teacher_required
def lessons(id_course):
    """Reinderizza alla schermata di visualizzazione delle lezioni del corso selezionato"""
    
    lessons = get_course_lessons(id_course)

    return render_template('teachers/lesson_list.html', course = get_course_by_id(id_course), lessons = lessons)



# UTILITY per Ajax

@teachers.route('/getClassrooms/<string:id_building>', methods=['GET', 'POST'])
@login_required
@teacher_required
def getClassrooms(id_building):
    """Seleziona tutte le aule di una sede (utilizzata nella richiesta AJAX)"""
    
    class_schema = ClassroomSchema(many=True)
    classrooms = get_classrooms_from_building(id_building)
    return jsonify(class_schema.dump(classrooms))
