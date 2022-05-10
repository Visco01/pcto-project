from flask import Blueprint
from flask import render_template, url_for, redirect, flash
from app.lib.db_actions import *
from flask_login import current_user, login_required
from flask import render_template, url_for, redirect

students = Blueprint('students', __name__)

@students.route('/student/dashboard')
@login_required
def student_dashboard():
    if get_student_by_id(current_user.id_user) is None:
        return redirect(url_for('main.login'))

    return render_template('students/student.html', courses=get_all_courses(), template='dashboard')


@students.route('/student/profile')
@login_required
def student_profile():
    if get_student_by_id(current_user.id_user) is None:
        return redirect(url_for('main.login'))

    return render_template('profile.html', user_type='student', template='profile')



@students.route('/student')
@login_required
def student():
    if get_student_by_id(current_user.id_user) is None:
        return redirect(url_for('teachers.teacher_dashboard'))

    return redirect(url_for('students.student_dashboard'))
