from flask import Blueprint, jsonify
from flask import render_template, url_for, redirect, flash, request
from app.lib.db_actions import *
from flask_login import current_user, login_required
from flask import render_template, url_for, redirect
from .utils import student_required
from app.lib.models_schema import UserSchema, CourseSchema

students = Blueprint('students', __name__)

#Reinderizza alla schermata dashboard dello studente
@students.route('/dashboard')
@login_required
@student_required
def dashboard():
    return render_template('students/dashboard.html', courses=get_all_courses())


#Reinderizza alla schermata del profilo privato dello studente
@students.route('/profile')
@login_required
@student_required
def profile():
    return render_template('students/profile.html')


#Reinderizza alla schermata di visualizzazione dei corsi ai quali lo studente è iscritto
@students.route('/my_courses')
@login_required
@student_required
def user_courses():
    return render_template('students/user_courses.html', courses=get_courses_by_student(current_user.id_user))


#UTILITY per Ajax

#Procedura di iscrizione ad un corso
@students.route('/subscription/<int:id_course>', methods=['GET', 'POST'])
@login_required
@student_required
def subscription_to_course(id_course):

    course = get_course_by_id(id_course)

    #Controlla che lo studente non sia già iscritto al corso selezionato
    if(is_student_already_subscribed(id_student=current_user.id_user, id_course=id_course)):
        response = {'mess': 'Errore: sei già iscritto a <strong>' + course.c_name + '</strong>!', 'type': 'danger'}
    else:
        insert_course_subscription(id_student=current_user.id_user, id_course=id_course)
        response = {'mess': 'Iscritto correttamente a <strong>'+ course.c_name +'</strong>!', 'type': 'success'}
    return jsonify(response)


#Procedura di disiscrizione ad un corso
@students.route('/delete_subscription/<int:id_course>', methods=['GET', 'POST'])
@login_required
@student_required
def delete_subscription_to_course(id_course):

    delete_course_subscription(id_student=current_user.id_user, id_course=id_course)
    response = {'mess': 'Iscrizione cancellata correttamente!', 'type': 'success', 'n_corsi': len(get_courses_by_student(current_user.id_user))}

    return jsonify(response)


#Controlla se lo studente è già iscritto ad un corso
@students.route('/is_subscribed/<int:id_course>', methods=['GET', 'POST'])
@login_required
@student_required
def is_subscribed(id_course):
    response = db.session.query(StudentsCourses).filter(StudentsCourses.id_course == id_course, StudentsCourses.id_student == current_user.id_user).first()
    if(response):
        return 'ok'
    else:
        return ''


#Seleziona i dettagli di un determinato corso
@students.route('/description/<int:id_course>', methods=['GET', 'POST'])
@login_required
@student_required
def description(id_course):

    user_schema = UserSchema()
    course_schema = CourseSchema()

    prof = get_course_professor(id_course)
    courses = get_all_courses()
    course = get_course_by_id(id_course)

    response = {'subscription_number': len(get_subscribed_students(id_course)),
                'prof': user_schema.dump(prof),
                'courses': course_schema.dump(courses),
                'course': course_schema.dump(course),
                'is_already_subscribed': is_student_already_subscribed(current_user.id_user, id_course)}

    return jsonify(response)
