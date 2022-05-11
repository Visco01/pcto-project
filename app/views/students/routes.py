from flask import Blueprint
from flask import render_template, url_for, redirect, flash
from app.lib.db_actions import *
from flask_login import current_user, login_required
from flask import render_template, url_for, redirect

students = Blueprint('students', __name__)

@students.route('/student/dashboard')
@login_required
def dashboard():
    checkUser()

    return render_template('students/dashboard.html', courses=get_all_courses())


@students.route('/student/profile')
@login_required
def profile():
    checkUser()

    return render_template('students/profile.html')

# Reinderizza tutti i professori al loro profilo
def checkUser():
    if get_student_by_id(current_user.id_user) is None:
        return redirect(url_for('main.index'))
