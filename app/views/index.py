from flask import render_template, url_for, redirect
from app import app
from app.lib.models import User
from app.lib.db_actions import *
from flask_login import current_user,login_required

#BLUEPRINTS
from .register import register_blueprint
from .authentication import authentication_blueprint
from .student import student_blueprint
from .teacher import teacher_blueprint

app.register_blueprint(register_blueprint)
app.register_blueprint(authentication_blueprint)
app.register_blueprint(student_blueprint)
app.register_blueprint(teacher_blueprint)

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users = users)


@app.route('/private')
@login_required
def private():
    if get_student_by_id(current_user.id_user):
        return redirect(url_for('student.student'))
    else:
        return redirect(url_for('teacher.teacher'))
