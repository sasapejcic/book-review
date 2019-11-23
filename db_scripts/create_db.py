import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from connection import connection

# Database URL using connection.py
DB_URL = connection()[4]

# Database URL using environment
#DB_URL = os.getenv("DATABASE_URL")

# Creating session
engine = create_engine(DB_URL)
db = scoped_session(sessionmaker(bind=engine))

# Main function used to recreate the whole database
def main():
    db.execute("DROP TABLE IF EXISTS reviews, users, books;")
    db.execute("CREATE TABLE IF NOT EXISTS books (isbn char(10) PRIMARY KEY, title varchar(100) NOT NULL, author varchar(40) NOT NULL, year smallint NOT NULL);")
    db.execute("CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY, username varchar(20) NOT NULL UNIQUE, password varchar(20) NOT NULL, display_name varchar(20));")
    db.execute("CREATE TABLE IF NOT EXISTS reviews (id serial PRIMARY KEY, review text NOT NULL, isbn char(10) NOT NULL REFERENCES books(isbn), id_user integer NOT NULL REFERENCES users(id)), rating smallint NOT NULL;")
    db.commit()

if __name__ == "__main__":
    main()
