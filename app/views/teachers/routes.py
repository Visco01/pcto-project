from flask import Blueprint
from .forms import NewCourseForm
from app.lib.db_actions import *
from flask_login import current_user, login_required
from flask import render_template, url_for, redirect

teachers = Blueprint('teachers', __name__)

@teachers.route('/teacher', methods=['GET', 'POST'])
@login_required
def teacher():
    # Controlla che gli studenti non possano accedere come professori cambiando URL
    if get_student_by_id(current_user.id_user):
        return redirect(url_for('students.student'))

    form = NewCourseForm()
    # Ottieni categorie da inserire nel menù a tendina
    form.category.choices = [(category.id_category, category.c_name) for category in get_all_categories()]

    if form.validate_on_submit():
        insert_course(form)
        # Pulisci form
        return redirect(url_for('teachers.teacher'))

    # Genera template
    return render_template('teacher.html', courses=get_all_courses_from_teacher(current_user.id_user), form=form)
