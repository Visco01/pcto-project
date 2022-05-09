from flask import Blueprint
from app.lib.db_actions import *
from flask_login import current_user, login_required
from flask import render_template, url_for, redirect

students = Blueprint('students', __name__)

@students.route('/student')
@login_required
def student():
    # Controlla che i professori non possano accedere come studenti cambiando URL
    if get_student_by_id(current_user.id_user) is None:
        return redirect(url_for('teachers.teacher'))
    # Genera template
    return render_template('student.html', courses=get_all_course())