import os

from flask import Flask, session, render_template, request, flash, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    #session['logged_in'] = True
    if session.get('logged_in'):
        query = db.execute("SELECT display_name FROM users WHERE username='sasa' AND password='sasa';").fetchone()
        session['name'] = query[0]

    #session.clear()
    #print(app.config)

    return render_template("index.html", is_auth=session.get('logged_in'), name=session.get('name'))

@app.route("/logout.html")
def logout():
    session['logged_in'] = False
    session['name'] = None
    return redirect('/')

@app.route('/login.html')
def login_r():
    if not session.get('logged_in'):
        return render_template("login.html")
    else:
        return index()

@app.route('/login', methods=['POST'])
def login():
    if request.form['password'] == 'sasa' and request.form['username'] == 'sasa':
        session['logged_in'] = True
        session['name'] = "Bruce Wayne"
        return redirect('/')
    else:
        flash('wrong password!')
        return login_r()
