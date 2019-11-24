import os

from flask import Flask, session, render_template, request, flash, redirect, abort
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import requests

import json

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
    if session.get('logged_in'):
        message=(f"Welcome, { session['name'] }!")
    else:
        message=(f"Please Log in to search the database.")
    return render_template("index.html", message=message, is_auth=session.get('logged_in'))

@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html", message="Come back soon", is_auth=session.get('logged_in'))

@app.route('/login')
def login():
    if not session.get('logged_in'):
        return render_template("login.html")
    else:
        return redirect('/')

@app.route('/login_check', methods=['POST'])
def login_check():
    username = request.form['username']
    password = request.form['password']
    query = db.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}';").fetchone()
    if query:
        session['name'] = query[3]
        session['id'] = query[0]
        session['logged_in'] = True
        message=f"Welcome, { session['name'] }!"
        return redirect('/')
    else:
        message='Wrong password!'
        return render_template("/login.html", message=message)

@app.route('/register')
def register():
    if not session.get('logged_in'):
        return render_template("/register.html")
    else:
        return redirect('/register_check')

@app.route('/register_check', methods=['POST'])
def register_check():
    username = request.form['username']
    password = request.form['password']
    display_name = request.form['display']
    query = db.execute(f"SELECT display_name FROM users WHERE username='{username}';").fetchone()
    if query:
        message='Username already taken!'
        return render_template("/register.html", message='Username already exists! Please choose different one')
    else:
        query = db.execute(f"INSERT INTO users (username, password, display_name) VALUES ('{username}', '{password}', '{display_name}')")
        db.commit()
        message='Thanks for registering! Please Log in'
        return render_template("/index.html", message='Thanks for registering! Please Log in', is_auth=False)

@app.route('/search', methods=['POST'])
def search():
    criteria = request.form['criteria']
    txt = request.form['txt']
    if criteria == "Search by":
        return render_template("/index.html", is_auth=session.get('logged_in'), message=(f"Wrong input!."))
    else:
        query = db.execute(f"SELECT * FROM books WHERE {criteria} LIKE '%{txt}%' ORDER BY title;").fetchall()
        if len(query) == 0:
            message = "No results found. Please try again."
            return render_template("/index.html", is_auth=session.get('logged_in'), message=message)
        else:
            return render_template("/index.html", is_auth=session.get('logged_in'), results=query)

@app.route("/book/<isbn>")
def book(isbn):
    # Make sure book exists.
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return render_template("/index.html", is_auth=session.get('logged_in'), message="No such book. Please try again using search box.")
    # Setting session variable
    session['isbn'] = isbn
    # Get all reviews.
    reviews = db.execute("SELECT reviews.rating, reviews.review, users.display_name FROM reviews JOIN users ON reviews.id_user=users.id WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
    session['nr'] = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "C2cWspF6M9QNh6rK7I0Dw", "isbns": isbn}).json()["books"][0]["work_ratings_count"]
    session['ar'] = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "C2cWspF6M9QNh6rK7I0Dw", "isbns": isbn}).json()["books"][0]["average_rating"]
    return render_template("/book.html", is_auth=session.get('logged_in'), results=book, reviews=reviews, nr=session['nr'], ar=session['ar'])

@app.route('/rate')
def rate():
    user = str(session.get('id'))
    isbn = str(session.get('isbn'))
    query = db.execute("SELECT * FROM reviews WHERE isbn = :isbn AND id_user = :user", {"isbn": isbn, "user": user}).fetchall()
    if query:
        message = "You already rated this book"
        url = f"/book/{isbn}"
        reviews = db.execute("SELECT reviews.rating, reviews.review, users.display_name FROM reviews JOIN users ON reviews.id_user=users.id WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
        book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
        return render_template("book.html", is_auth=session.get('logged_in'), message=message, results=book, reviews=reviews, nr=session['nr'], ar=session['ar'])
    else:
        return render_template("/rate.html")


@app.route('/rate_submit', methods=['POST'])
def rate_submit():
    review = request.form['review']
    isbn = str(session.get('isbn'))
    id_user = str(session.get('id'))
    rating = request.form['rating']
    print(review,isbn,id_user,rating)
    query = db.execute(f"INSERT INTO reviews (review, isbn, id_user, rating) VALUES ('{review}', '{isbn}', '{id_user}', '{rating}' )")
    db.commit()
    url = f"/book/{isbn}"
    return redirect(url)

@app.route("/api/<isbn>")
def api(isbn):
    # Make sure book exists.
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        abort(404, description="Book not found")
    else:
        response = {}
        response["title"] = book.title
        response["author"] = book.author
        response["year"] = book.year
        response["isbn"] = book.isbn
        reviews = db.execute("SELECT COUNT(*), AVG(rating) FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
        print(reviews)
        response["review_count"] = reviews[0]
        response["average_score"] = float(str(round(reviews[1], 1)))
        print(response)
        return json.dumps(response)
