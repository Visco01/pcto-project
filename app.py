from flask import Flask
from lib.conn import get_engine
app = Flask(__name__)



@app.route('/')
def index():
    engine = get_engine()
    return engine.url.database
