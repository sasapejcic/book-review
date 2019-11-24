# Project 1

Web Programming with Python and JavaScript

application.py is the main file of this project. All routes inside of it are
made according to instructions. There are routes for home page, login, register,
logout, search, book display, review submit and api. There are  two routes for
handling errors at the bottom of the file.

.gitignore is used to ignore cache folders, stanalone sass compiler, and some
files used in a process of development.

books.csv is a file with 5000 books that has been used to populate the database.
Database itself is hosted at Heroku.

requirements.txt stores libraries required to proper functioning of the website.
request library has been added to this file.

flask-run.bat is file used to initially set environment variables at the first
run. It should not be deployed to production server but it was helpful during
development.

templates folder is used to store html files that are rendered by application.py.

header.html is used to display logo, site name and login and join buttons and
it is included in layout.html
layout.html is template file used to render all html files that are described
below.
index.html is most complex of all html files. It has couple of blocks that are
used to render different forms, buttons messages and search boxes based on
various conditions.
login.html register.html and rate.html are pretty much self explanatory.
book.html displays info about specific book.
error.html is rendered when 404 or 405 error occurs.

static folder has two subfolders css and images.
images folder has only logo.png inside of it.
css folder has three files: styles.scss and corresponding map and css files.

db_scripts folder has three files.
connection.py is used to store parameters required to connect to Heroku database.
create_db.py drops all tables from existing database and creates new one from
scratch.
import.py is file required for this project. Its purpose is to import data from
books.csv into database.
