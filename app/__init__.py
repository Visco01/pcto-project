from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.lib.conn import ConnectionData

import os
SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = ConnectionData.get_url()
db = SQLAlchemy(app)

from app.lib import routes