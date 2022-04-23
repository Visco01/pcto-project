from flask import Flask, render_template
from lib.conn import get_engine
app = Flask(__name__)


@app.route('/')
def index():
    engine = get_engine()
    return engine.url.database

test = 'Hello world'

@app.route('/login')
def login():
    return render_template('login.html', title=test)


@app.route('/register')
def register():
    return render_template('register.html', title=test)


if __name__ == '__main__':
    app.run(debug=True)
