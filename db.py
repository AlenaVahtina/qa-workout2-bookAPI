import sqlite3
from sqlite3 import Error


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
            self.conn.row_factory = dict_factory
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
        cur = self.conn.cursor()
        books = cur.execute("SELECT id, name, year, description from book").fetchall()
        return books

    def select_one_book(self, book_id):
        cur = self.conn.cursor()
        book = cur.execute("SELECT id, name, year, description from book where id=?", book_id).fetchone()
        return book

    def select_pages(self, book_id):
        result = {"book": None,
                  "pages": []}
        self.conn.row_factory = dict_factory
        cur = self.conn.cursor()
        book_name = cur.execute("SELECT name FROM book where id=?", book_id).fetchone()
        result["book"] = book_name["name"]
        pages = cur.execute("SELECT id, content, is_destroyed FROM page WHERE book_id=?", book_id).fetchall()
        result["pages"] = pages
        return result

    def select_page(self, book_id, page_id):
        cur = self.conn.cursor()
        page = cur.execute("SELECT id, content, is_destroyed FROM page WHERE book_id=? AND id=?",
                           (book_id, page_id)).fetchone()
        return page

    def select_authors_by_book(self, book_id):
        cur = self.conn.cursor()
        authors = cur.execute("SELECT a.first_name, a.last_name FROM author as a "
                              "INNER JOIN book_author as ba "
                              "ON a.id=ba.author_id "
                              "WHERE ba.book_id=?", book_id).fetchall()
        return authors

    def select_authors(self):
        cur = self.conn.cursor()
        authors = cur.execute("SELECT first_name, last_name FROM author").fetchall()
        return authors

    def insert_books(self, books):
        result = {}
        cur = self.conn.cursor()
        for book in books:
            cur.execute("INSERT INTO book(name, year, description) VALUES(?,?,?)", (book["name"], book["year"],
                                                                                    book["description"]))
            book_id = cur.lastrowid
            for author in book['authors']:
                cur.execute("INSERT INTO author(first_name, last_name) VALUES(?,?)", (author["first_name"],
                                                                                      author["last_name"]))
                author_id = cur.lastrowid
                cur.execute("INSERT INTO  book_author(book_id, author_id) VALUES(?,?)", (book_id, author_id))
            for page in book["pages"]:
                cur.execute("INSERT INTO page(book_id, content, is_destroyed) VALUES(?,?,?)", (book_id, page["content"],
                                                                                               page["is_destroyed"]))
            self.conn.commit()
            result = "{'OK':'Insert success'}"
        return result

    def update_books(self, book, book_id):
        result = {}
        cur = self.conn.cursor()
        cur.execute("UPDATE book SET name=?, year=?, description=? WHERE id=?", (book["name"], book["year"],
                                                                                 book["description"], book_id))
        for page in book["pages"]:
            cur.execute("INSERT INTO page(book_id, content, is_destroyed) VALUES(?,?,?)", (book_id, page["content"],
                                                                                           page["is_destroyed"]))
        self.conn.commit()
        result = "{'OK':'Update success'}"
        return result

    def update_book_single_page(self, new_page, book_id, page_id):
        result = {}
        cur = self.conn.cursor()
        pages = cur.execute("SELECT id FROM page WHERE book_id=?", book_id).fetchall()
        if int(page_id) in [int(x['id']) for x in pages]:
            cur.execute("UPDATE page SET content=?, is_destroyed=0 WHERE id=?", (new_page["content"], page_id))
        else:
            cur.execute("INSERT INTO page(book_id, content, is_destroyed) VALUES(?,?,?)", (book_id, new_page["content"],
                                                                                           "true"))
        self.conn.commit()
        result = "{'OK':'Update success'}"
        return result

    def delete_book(self, book_id):
        result = {}
        cur = self.conn.cursor()
        cur.execute("DELETE FROM book WHERE id=?", book_id)
        cur.execute("DELETE FROM book_author WHERE book_id=?", book_id)
        cur.execute("DELETE FROM page WHERE book_id=?", book_id)
        self.conn.commit()
        result = "{'OK':'Delete success'}"
        return result

    def get_book_all_pages_info(self, book_id):
        cur = self.conn.cursor()
        return cur.execute("SELECT cast(count(*) as text) as \"Page-count\" FROM page WHERE book_id=?", book_id).fetchone()
