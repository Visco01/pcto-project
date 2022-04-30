from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .conn import ConnectionData
import os

app = Flask('app')

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = ConnectionData.get_url()

db = SQLAlchemy(app)
db_model = db.Model
