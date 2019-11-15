import os
import psycopg2
from connection import connection

#DATABASE_URL = os.environ['DATABASE_URL']

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = connection()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host=params[0],database=params[1], user=params[2], password=params[3])

        # create a cursor
        cur = conn.cursor()

        # Dropin tables
        print('Droping existing tables...')
        cur.execute('DROP TABLE IF EXISTS reviews, users, books;')

        # Creating tables
        print('Creating tables...')
        cur.execute("CREATE TABLE IF NOT EXISTS books (isbn char(10) NOT NULL PRIMARY KEY, title varchar(100) NOT NULL, author varchar(40) NOT NULL, year integer NOT NULL);")
        cur.execute("CREATE TABLE IF NOT EXISTS users (id serial NOT NULL UNIQUE PRIMARY KEY, username varchar(20) NOT NULL UNIQUE, password varchar(20) NOT NULL, display_name varchar(20));")
        cur.execute("CREATE TABLE IF NOT EXISTS reviews (id serial NOT NULL UNIQUE PRIMARY KEY, review text NOT NULL, isbn char(10) NOT NULL REFERENCES books(isbn), id_user integer NOT NULL REFERENCES users(id));")

       # close the communication with the PostgreSQL
        cur.close()
        print("Committing...")
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

connect()

"""
if __name__ == '__main__':
    connect()

try:
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("SELECT vendor_id, vendor_name FROM vendors ORDER BY vendor_name")
    print("The number of parts: ", cur.rowcount)
    row = cur.fetchone()

    while row is not None:
        print(row)
        row = cur.fetchone()
    cur.close()
except(Exception, psycopg2.DatabaseError) as error:
    print(error)
"""
