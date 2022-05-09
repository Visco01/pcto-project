from flask import Blueprint
from flask import render_template, url_for, redirect, flash
from app.lib.db_actions import *
from flask_login import current_user, login_required
from flask import render_template, url_for, redirect

students = Blueprint('students', __name__)

student_blueprint = Blueprint('student', __name__)
student_blueprint.register_blueprint(authentication_blueprint)

@student_blueprint.route('/student/dashboard')
@login_required
def student_dashboard():
    if get_student_by_id(current_user.id_user) is None:
        return redirect(url_for('authentication.login'))

    return render_template('student.html', courses=get_all_course(), template='dashboard')


@student_blueprint.route('/student/profile')
@login_required
def student_profile():
    return render_template('profile.html', user_type='student', template='profile')

@students.route('/student')
@login_required
def student():
    # Controlla che i professori non possano accedere come studenti cambiando URL
    if get_student_by_id(current_user.id_user) is None:
        return redirect(url_for('teachers.teacher'))
    # Genera template
    return render_template('student.html', courses=get_all_course())
