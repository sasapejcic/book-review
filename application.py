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
    print(session.get('logged_in'))
    return render_template("index.html", is_auth=session.get('logged_in'), message=(f"Welcome, { session['name'] }!"))

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
        return render_template("index.html", is_auth=session.get('logged_in'), message=(f"Welcome, { session['name'] }!"))
    else:
        return render_template("index.html", message='Wrong password!')

@app.route('/register.html')
def register_r():
    if not session.get('logged_in'):
        return render_template("register.html")
    else:
        return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    display_name = request.form['display']
    query = db.execute(f"SELECT display_name FROM users WHERE username='{username}';").fetchone()
    if query:
        return render_template("index.html", message='Username already taken!')
    else:
        query = db.execute(f"INSERT INTO users (username, password, display_name) VALUES ('{username}', '{password}', '{display_name}')")
        db.commit()
        return render_template("index.html", message='Thanks for registering! Please Log in')
