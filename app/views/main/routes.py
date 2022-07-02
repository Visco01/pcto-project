from flask import Blueprint, session
from .forms import LoginForm, RegistrationFrom
from app.lib.db_actions import *
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, flash, redirect, request

from app import mail
from flask_mail import Message

import secrets

import folium

from app.lib.models import *

main = Blueprint('main', __name__)

@main.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users = users)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("Accesso già effettuato", 'danger')
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():

        user = get_user_by_email(form.email.data)

        if(not user):
            flash("Account non registrato", 'danger')
            return redirect(url_for('main.login'))

        if(not user.is_active):
            flash("Account non attivo: verifica l'account tramite l'email inviata a " + user.email, 'danger')
            return redirect(url_for('main.login'))

        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.rememberMe.data)

            if get_student_by_id(user.id_user):
                session['role'] = 'student'
            else:
                session['role'] = 'teacher'
                flash("Accesso come professore", 'success')
                return redirect(url_for('teachers.profile'))


            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('students.dashboard')) # ternary operator
        else:
            flash('Accesso negato', 'danger')

    return render_template('login.html', form = form)


def send_verification_email(token, email):
    msg = Message("Attivazione account PCTO Unive",
                  sender="noreply.pcto@gmail.com",
                  recipients=[email])

    msg.body = "Conferma il tuo account cliccando sul seguente link: http://localhost:5000/verify_account/" + token

    mail.send(msg)


@main.route('/verify_account/<string:token>')
def verify_account(token):
    if(set_user_active(token)):
        flash('Account attivato!', 'success')
    else:
        flash('Account non attivato', 'danger')

    return redirect(url_for('main.login'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("Accesso già effettuato", 'danger')
        return redirect(url_for('main.index'))
    form = RegistrationFrom()
    if form.validate_on_submit():

        token = secrets.token_urlsafe(16)
        insert_token(token, form.email.data)
        insert_user(form)

        send_verification_email(token, form.email.data)

        flash('Email di verifica inviata a ' + form.email.data, 'success')

    return render_template('register.html', form = form)


@main.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('main.index'))


@main.route('/course_page/<int:id>')
@login_required
def course_page(id):
    # Crea mappa nelle coordinate indicate
    # location=[latitude, longitude]
    # zoom_start imposta lo zoom di partenza della mappa

    # seleziona l'edificio in cui si terrà la prossima lezione del corso
    building = get_building_from_lesson(id)
    #seleziona i partecipanti al corso
    partecipants = get_subscribed_students_data(id)

    if building:
        map = folium.Map(location=[building.latitude, building.longitude], zoom_start=18)
        lessons = get_course_lessons(id)

        # Crea un marker nelle coordinate indicate e aggiungilo alla mappa
        folium.Marker([building.latitude, building.longitude]).add_to(map)
        # _repr_html_() renderizza la mappa e la visualizza
        return render_template('course_page.html', map=map._repr_html_(), course=get_course_by_id(id), lessons=lessons, partecipants=partecipants)
    # _repr_html_() renderizza la mappa e la visualizza
    return render_template('course_page.html', course=get_course_by_id(id), partecipants=partecipants)

@main.route('/load_data')
def load_data():
    import urllib.request, json
    # Sedi

    with urllib.request.urlopen("http://apps.unive.it/sitows/didattica/sedi") as url:
        data = json.loads(url.read().decode())
        for datas in data:

            if isinstance(datas['COORDINATE'], str):
                coordinates_list = datas['COORDINATE'].split(",")
                coordinate_x = coordinates_list[0]
                coordinate_y = coordinates_list[1]
                #print(coordinate_x + "  " + coordinate_y)

            newBuilding = Building(id_building=datas['SEDE_ID'], b_name=datas['NOME'], longitude=coordinate_x, latitude=coordinate_y)

            db.session.add(newBuilding)
            db.session.commit()
            db.session.flush()

    # Aule
    with urllib.request.urlopen("https://apps.unive.it/sitows/didattica/aule") as url:
        data = json.loads(url.read().decode())
        for datas in data:

            if get_building_from_classroom(datas['SEDE_ID']):
                newClassroom = Classroom(id_classroom=datas['AULA_ID'], c_name=datas['NOME'], capacity=datas    ['POSTI'], id_building=datas['SEDE_ID'])
                db.session.add(newClassroom)
                db.session.flush()


    db.session.commit()
    return 'done'

@main.route('/<path>/<id_course>/lessons', methods = ['GET','POST'])
def lessons(id_course,path):
    isTeacher = False
    if path == 'teacher':
        isTeacher = True
    if not current_user.is_authenticated:
        return redirect(url_for('main.index'))

    lessons = get_course_lessons(id_course)

    hasLessons = True
    if len(lessons) == 0:
        hasLessons = False
    return render_template('lesson_list.html', teacher = isTeacher, course = get_course_by_id(id_course), lessons = lessons, no_lessons = not hasLessons)
