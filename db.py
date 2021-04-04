import sqlite3
from sqlite3 import Error


class DB:
    def __init__(self):
        self.conn = None

    def create_connection(self):
        # conn = None
        try:
            self.conn = sqlite3.connect(':memory:')
            print(sqlite3.version)
        except Error as e:
            print(e)
        # finally:
        #     if self.conn:
        #         self.conn.close()

    def create_db(self):
        cur = self.conn.cursor()
        cur.execute("CREATE TABLE author(id int, first_name varchar(32), last_name varchar(32), PRIMARY KEY (id))")
        cur.execute("CREATE TABLE book(id int, name varchar(100), year date, description text, PRIMARY KEY (id))")
        cur.execute("CREATE TABLE page(id int, book_id int, content text, is_torn boolean, PRIMARY KEY (id))")
        cur.execute("CREATE TABLE book_author(book_id int, author_id int)")
        self.conn.commit()

    def create_value(self):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO book(id, name, year, description) VALUES(1, 'Tails', '1994', 'Сказки народов мира')")
        self.conn.commit()

    def select_all_book(self):
        cur = self.conn.cursor()
        book = cur.execute("SELECT * from book")
        print(book.fetchone())
