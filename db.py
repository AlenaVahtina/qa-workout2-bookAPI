import sqlite3
from sqlite3 import Error


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(':memory:')
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_db(conn):
    cur = conn.cursor()
    cur.execute("CREATE TABLE author(id int, FirstName varchar(32), LastName varchar(32), PRIMARY KEY (Id))")
    cur.execute("CREATE TABLE book(id int, name varchar(100), year date, description text, PRIMARY KEY (Id))")
    cur.execute("CREATE TABLE page(id int, book_id int, content text, is_torn boolean, PRIMARY KEY (Id))")
    cur.execute("CREATE TABLE book_author(book_id int, author_id int)")

