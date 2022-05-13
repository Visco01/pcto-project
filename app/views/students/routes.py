from flask import Blueprint
from flask import render_template, url_for, redirect, flash
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
