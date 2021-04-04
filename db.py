import sqlite3
from sqlite3 import Error


class DB:
    def __init__(self):
        self.conn = None

    def create_connection(self):
        try:
            self.conn = sqlite3.connect(':memory:')
            print(sqlite3.version)
        except Error as e:
            print(e)

    def create_db(self):
        cur = self.conn.cursor()
        cur.execute("CREATE TABLE author(id INTEGER, first_name varchar(32), last_name varchar(32), "
                    "PRIMARY KEY (id))")
        cur.execute("CREATE TABLE book(id INTEGER, name varchar(100), year date, description text, "
                    "PRIMARY KEY (id))")
        cur.execute("CREATE TABLE page(id INTEGER, book_id int, content text, is_torn boolean, "
                    "PRIMARY KEY (id))")
        cur.execute("CREATE TABLE book_author(book_id INTEGER, author_id INTEGER)")
        self.conn.commit()

    def create_value(self):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO book(name, year, description) VALUES('Сказки', '1994', 'Сказки народов мира')")
        cur.execute("INSERT INTO book(name, year, description) VALUES('Два капитана', '1944',"
                    " 'Приключенческий роман писателя Вениамина Каверина, который был написан им в 1938—1944 годах')")
        cur.execute("INSERT INTO author(first_name, last_name) VALUES('','')")
        self.conn.commit()

    def select_all_book(self):
        cur = self.conn.cursor()
        book = cur.execute("SELECT * from book")
        print(book.fetchall())
