from flask import Blueprint
from flask import render_template, url_for, redirect
from app.lib.db_actions import *
from flask_login import current_user, login_required

from .authentication import authentication_blueprint

student_blueprint = Blueprint('student', __name__)
student_blueprint.register_blueprint(authentication_blueprint)

@student_blueprint.route('/student')
@login_required
def student():
    if get_student_by_id(current_user.id_user) is None:
        return redirect(url_for('authentication.login'))

    return render_template('student.html', courses=get_all_course())
