from flask import Blueprint, session, abort
from .forms import Login_Form, Registration_Form
from app.lib.db_actions import *
from flask_login import login_user, current_user, logout_user, login_required
from app.views.teachers.utils import teacher_required
from flask import render_template, url_for, flash, redirect, request
from app import mail
from flask_mail import Message
import secrets
import folium
from app.lib.models import *

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """Reinderizza alla root del sito"""

    users = User.query.all()
    return render_template('index.html', users=users)


@main.route('/login', methods=['GET', 'POST'])
def login():
    """Reinderizza alla schermata di login"""

    # Controlla se l'utente ha già fatto l'accesso
    if current_user.is_authenticated:
        flash("Accesso già effettuato", 'danger')
        return redirect(url_for('main.index'))

    form = Login_Form()

    # Controlla che il form sia valido
    if form.validate_on_submit():

        user = get_user_by_email(form.email.data)

        if(not user):
            flash("Account non registrato", 'danger')
            return redirect(url_for('main.login'))

        if(not user.is_active):
            flash("Account non attivo: verifica l'account tramite l'email inviata a " +
                  user.email, 'danger')
            return redirect(url_for('main.login'))

        # Crittografia della password
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)

            # Assegnazione del ruolo nella sessione (Studente o Professore)
            if get_student_by_id(user.id_user):
                session['role'] = 'student'
            else:
                session['role'] = 'teacher'
                flash("Accesso come professore", 'success')
                return redirect(url_for('teachers.profile'))

            # Reinderizza alla pagina precedentemente richiesta prima di effettuare il login
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('students.dashboard'))
        else:
            flash('Accesso negato', 'danger')

    return render_template('login.html', form=form)


def send_verification_email(token, email):
    """Invia una email di verifica per attivare l'account in seguito alla registrazione"""

    msg = Message("Attivazione account PCTO Unive",
                  sender="noreply.pcto@gmail.com",
                  recipients=[email])

    msg.body = "Conferma il tuo account cliccando sul seguente link: http://localhost:5000/verify_account/" + token

    mail.send(msg)


@main.route('/verify_account/<string:token>')
def verify_account(token):
    """Controlla che il token di verifica corrisponda a quello associato all'utente nel database"""

    if(set_user_active(token)):
        flash('Account attivato!', 'success')
    else:
        flash('Account non attivato', 'danger')

    return redirect(url_for('main.login'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    """Reinderizza alla schermata di registrazione"""

    # Controlla se l'utente ha già effettuato l'accesso
    if current_user.is_authenticated:
        flash("Accesso già effettuato", 'danger')
        return redirect(url_for('main.index'))

    form = Registration_Form()

    if form.validate_on_submit():

        # Generazione del toke univoco per l'attivazione dell'account
        token = secrets.token_urlsafe(16)
        insert_token(token, form.email.data)
        insert_user(form)

        send_verification_email(token, form.email.data)

        flash('Email di verifica inviata a ' + form.email.data, 'success')

    return render_template('register.html', form=form)


@main.route('/logout')
def logout():
    """Effettua il logout dalla web application"""

    logout_user()
    session.clear()
    return redirect(url_for('main.index'))


@main.route('/course_page/<int:id>')
@login_required
def course_page(id):
    """Reinderizza alla schermata di presentazione del corso selezionato"""

    # Controlla che l'utente sia effettivamente iscritto al corso
    if current_user.id_user not in get_users_from_course(id):
        abort(404)

    # Crea mappa nelle coordinate indicate
    # location=[latitude, longitude]
    # zoom_start imposta lo zoom di partenza della mappa

    # seleziona l'edificio in cui si terrà la prossima lezione del corso
    building = get_building_from_lesson(id)
    # seleziona i partecipanti al corso
    partecipants = get_subscribed_students_data(id)

    if building:
        map = folium.Map(
            location=[building.latitude, building.longitude], zoom_start=18)
        lessons = get_course_lessons(id)

        # Crea un marker nelle coordinate indicate e aggiungilo alla mappa
        folium.Marker(
            location = [building.latitude, building.longitude],
            popup = building.b_name
            ).add_to(map)
        
        # _repr_html_() renderizza la mappa e la visualizza
        return render_template('course_page.html', map=map._repr_html_(), course=get_course_by_id(id), lessons=lessons, partecipants=partecipants)

    return render_template('course_page.html', course=get_course_by_id(id), partecipants=partecipants)


@login_required
@teacher_required
@main.route('/load_data')
def load_data():
    """Scarica i dati delle sedi e delle aule nel database"""

    import urllib.request
    import json

    # Importazione delle sedi
    with urllib.request.urlopen("http://apps.unive.it/sitows/didattica/sedi") as url:
        data = json.loads(url.read().decode())
        for datas in data:

            if isinstance(datas['COORDINATE'], str):
                coordinates_list = datas['COORDINATE'].split(",")
                coordinate_x = coordinates_list[0]
                coordinate_y = coordinates_list[1]

            newBuilding = Building(
                id_building=datas['SEDE_ID'], b_name=datas['NOME'], longitude=coordinate_x, latitude=coordinate_y)

            db.session.add(newBuilding)
            db.session.commit()
            db.session.flush()

    # Importazione delle aule
    with urllib.request.urlopen("https://apps.unive.it/sitows/didattica/aule") as url:
        data = json.loads(url.read().decode())
        for datas in data:

            if get_building_from_classroom(datas['SEDE_ID']):
                newClassroom = Classroom(
                    id_classroom=datas['AULA_ID'], c_name=datas['NOME'], capacity=datas['POSTI'], id_building=datas['SEDE_ID'])
                db.session.add(newClassroom)
                db.session.flush()

    db.session.commit()
    return 'done'
