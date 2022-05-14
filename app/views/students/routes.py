from flask import Blueprint
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


@students.route('/subscription/<id_course>')
@login_required
@student_required
def subscription_to_course(id_course):
    #print(id_course)

    if(is_student_subscripted(id_student=current_user.id_user, id_course=id_course)):
        flash('Errore: sei già iscritto a questo corso!', 'danger')
    else:
        insert_course_subscription(id_student=current_user.id_user, id_course=id_course)
        flash('Iscrizione eseguita con successo', 'success')

    return redirect(url_for('students.profile'))
