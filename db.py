import sqlite3
from sqlite3 import Error
import json


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


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
        cur.execute("CREATE TABLE author(id INTEGER, first_name varchar(32), last_name varchar(32),"
                    "PRIMARY KEY (id))")
        cur.execute("CREATE TABLE book(id INTEGER, name varchar(100), year date, description text, "
                    "PRIMARY KEY (id))")
        cur.execute("CREATE TABLE page(id INTEGER, book_id int, content text, is_destroyed boolean, "
                    "PRIMARY KEY (id))")
        cur.execute("CREATE TABLE book_author(book_id INTEGER, author_id INTEGER)")
        self.conn.commit()

    def create_value(self):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO book(name, year, description) VALUES('Сказки', '1994', 'Сказки народов мира')")
        cur.execute("INSERT INTO book(name, year, description) VALUES('Два капитана', '1944',"
                    " 'Приключенческий роман писателя Вениамина Каверина, который был написан им в 1938—1944 годах')")
        cur.execute("INSERT INTO page(book_id, content, is_destroyed) "
                    "VALUES(1,'Жили-были старик со старухой', 'false')")
        cur.execute("INSERT INTO page(book_id, content, is_destroyed) VALUES(1, 'У самого синего моря', 'false')")
        cur.execute("INSERT INTO author(first_name, last_name) VALUES('Александр', 'Пушкин')")
        cur.execute("INSERT INTO  book_author(book_id, author_id) VALUES(1,1)")
        self.conn.commit()

    def select_all_book(self):
        result = []
        self.conn.row_factory = dict_factory
        cur = self.conn.cursor()
        books = cur.execute("SELECT id, name, year, description from book")
        for row in books:
            result.append({"id": row["id"],
                           "name": row["name"],
                           "year": row["year"],
                           "description": row["description"]})
        return result

    def select_one_book(self, book_id):
        self.conn.row_factory = dict_factory
        cur = self.conn.cursor()
        book = cur.execute("SELECT id, name, year, description from book where id=?", book_id).fetchone()
        result = {"id": book["id"],
                  "name": book["name"],
                  "year": book["year"],
                  "description": book["description"]}
        return result

    def select_pages(self, book_id):
        result = {"book": None,
                  "pages": []}
        self.conn.row_factory = dict_factory
        cur = self.conn.cursor()
        book_name = cur.execute("SELECT name FROM book where id=?", book_id).fetchone()
        result["book"] = book_name["name"]
        pages = cur.execute("SELECT id, content, is_destroyed FROM page WHERE book_id=?", book_id)
        for row in pages:
            result["pages"].append({"id": row["id"],
                                    "content": row["content"],
                                    "is_destroyed": row["is_destroyed"]})
        return result

    def select_page(self, book_id, page_id):
        self.conn.row_factory = dict_factory
        cur = self.conn.cursor()
        page = cur.execute("SELECT id, content, is_destroyed FROM page WHERE book_id=? AND id=?", (book_id, page_id)).fetchone()
        result = {
            "id": page["id"],
            "content": page["content"],
            "destroyed": page["is_destroyed"]
        }
        return result

    def select_authors_by_book(self, book_id):
        result = []
        self.conn.row_factory = dict_factory
        cur = self.conn.cursor()
        authors = cur.execute("SELECT a.first_name, a.last_name FROM author as a "
                              "INNER JOIN book_author as ba "
                              "ON a.id=ba.author_id "
                              "WHERE ba.book_id=?", book_id)
        for row in authors:
            result.append({"first_name": row["first_name"],
                          "last_name": row["last_name"]})
        return result

    def select_authors(self):
        result = []
        self.conn.row_factory = dict_factory
        cur = self.conn.cursor()
        authors = cur.execute("SELECT first_name, last_name FROM author")
        for row in authors:
            result.append({"first_name": row["first_name"],
                          "last_name": row["last_name"]})
        return result

    def insert_books(self, books):
        result = {}
        self.conn.row_factory = dict_factory
        cur = self.conn.cursor()
        for book in books:
            cur.execute("INSERT INTO book(name, year, description) VALUES(?,?,?)", (book["name"], book["year"],
                                                                                    book["description"]))
            self.conn.commit()
        return result
