from urllib import response
from flask import Blueprint, jsonify
from flask import render_template, url_for, redirect, flash, request
from app.lib.db_actions import *
from flask_login import current_user, login_required
from flask import render_template, url_for, redirect
from .utils import student_required

students = Blueprint('students', __name__)

@students.route('/dashboard')
@login_required
@student_required
def dashboard():
    return render_template('students/dashboard.html', courses=get_all_courses())


@students.route('/profile')
@login_required
@student_required
def profile():
    return render_template('students/profile.html')


@students.route('/subscription/<id_course>', methods=['GET', 'POST'])
@login_required
@student_required
def subscription_to_course(id_course):
    if(is_student_already_subscribed(id_student=current_user.id_user, id_course=id_course)):
        response = {'mess': 'Errore: sei già iscritto a questo corso!', 'type': 'danger'}
    else:
        insert_course_subscription(id_student=current_user.id_user, id_course=id_course)
        response = {'mess': 'Iscritto correttamente!', 'type': 'success'}
    return jsonify(response)


@students.route('/description/<id_course>', methods=['GET', 'POST'])
@login_required
@student_required
def description(id_course):
    
    response = {'subscription_number': len(get_subscribed_students(id_course)), 'prof': get_course_professor(id_course), 'courses': get_all_courses(), 'course': get_course_by_id(id_course)}
    return jsonify(response)
