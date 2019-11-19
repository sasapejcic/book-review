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
        return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    query = db.execute(f"SELECT display_name FROM users WHERE username='{username}' AND password='{password}';").fetchone()
    if query:
        session['name'] = query[0]
        session['logged_in'] = True
        return redirect('/')
    else:
        flash('wrong password!')
        return login_r()
