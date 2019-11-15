import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from connection import connection

DB_URL = connection()[4]
#DB_URL = os.getenv("DATABASE_URL")

engine = create_engine(DB_URL)
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("../books.csv")
    reader = csv.reader(f)

    # Skipping the header
    next(reader, None)

    for isbn, title, author, year in reader:

        db.execute("INSERT INTO books (isbn, author, title, year) VALUES (:isbn, :author, :title, :year)",
                    {"isbn": isbn, "author": author, "title": title, "year": year})
        print(f"Added book with isbn number {isbn}.")
    db.commit()

if __name__ == "__main__":
    main()
