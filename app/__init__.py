from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_gravatar import Gravatar
from flask_mail import Mail
import babel
from flask_navigation import Navigation
from app.lib.conn import ConnectionData

#Inizializzazione app
app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

#Connessione al Database
app.config['SECRET_KEY'] = 'e617cdbc1721d5469e8345acd2c7e5c3'
app.config['SQLALCHEMY_DATABASE_URI'] = ConnectionData.get_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Inizializzazione librerie
nav = Navigation(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)

#Inizializzazione LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'

#Configurazione Gravatar per la foto profilo
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='mp',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

#Configurazione email automatica per l'attivazione dell'account
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'noreply.pcto@gmail.com',
    MAIL_PASSWORD = 'vzrtaevyzfmssvyx'
)
mail = Mail(app)

#Importazione blueprints
from app.views.main.routes import main
from app.views.students.routes import students
from app.views.teachers.routes import teachers

app.register_blueprint(main)
app.register_blueprint(students, url_prefix='/student')
app.register_blueprint(teachers, url_prefix='/teacher')

#Definizione route pagina di errore 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

app.register_error_handler(404, page_not_found)

#Creazione Navbar
nav.Bar('not_logged', [
    nav.Item('Accedi', 'main.login'),
    nav.Item('Registrati', 'main.register'),
])

nav.Bar('students', [
    nav.Item('Corsi', 'students.dashboard'),
    nav.Item('I miei corsi', 'students.user_courses')
])

nav.Bar('teachers', [
    nav.Item('Gestione corsi', 'teachers.dashboard')
])

# Filtro Jinja2 per formattare le date
# {{ "date" | format_datetime }}
@app.template_filter()
def format_datetime(value, format):
    if format == 'date':
        return babel.dates.format_date(value, format="short", locale='it')
    if format == 'time':
        return babel.dates.format_time(value, format="short", locale='it')
