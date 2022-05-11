from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from app.lib.conn import ConnectionData

import os
SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = ConnectionData.get_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'

# from app.views import index

from app.views.main.routes import main
from app.views.students.routes import students
from app.views.teachers.routes import teachers

app.register_blueprint(main)
app.register_blueprint(students, url_prefix='/student')
app.register_blueprint(teachers, url_prefix='/teacher')
