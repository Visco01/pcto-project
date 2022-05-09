from flask import Blueprint
from flask import render_template, url_for, redirect
from app.lib.db_actions import *
from app.lib.forms import newCourseForm
from flask_login import current_user, login_required

from .authentication import authentication_blueprint

teacher_blueprint = Blueprint('teacher', __name__)
teacher_blueprint.register_blueprint(authentication_blueprint)

@teacher_blueprint.route('/teacher/dashboard', methods=['GET', 'POST'])
@login_required
def teacher_dashboard():
    if get_student_by_id(current_user.id_user):
        return redirect(url_for('authentication.login'))

    form = newCourseForm()
    form.category.choices = [(category.id_category, category.c_name) for category in get_all_categories()]

    if form.validate_on_submit():
        insert_course(form)
        return redirect(url_for('teacher'))

    return render_template('teacher.html', courses=get_all_courses_from_teacher(current_user.id_user), form=form)


@teacher_blueprint.route('/teacher/profile')
@login_required
def teacher_profile():
    return render_template('profile.html', user_type='teacher', template='profile')
