from aiohttp import web
import aiohttp_cors
import logging
import json
import datetime
from db import DB

logging.basicConfig(level="DEBUG")


def validBooks(books):
    for book in books:
        if not book.get("name", None):
            resp = "{'Error':'Book can't be without a name'}"
            return resp


async def getBook(request):
    book_id = str(request.match_info['book_id'])
    if int(book_id) < 0:
        resp = "{'Error': 'book can't have id<0'}"
        return web.json_response(resp, status=422)
    else:
        resp = x.select_one_book(book_id)
        return web.json_response(resp, status=200)


async def getAllBooks(request):
    resp = x.select_all_book()
    return web.json_response(resp, status=200)


async def getBookAllPages(request):
    book_id = str(request.match_info['book_id'])
    resp = x.select_pages(book_id)
    return web.json_response(resp, status=200)


async def getBookSinglePage(request):
    book_id = str(request.match_info['book_id'])
    page_id = str(request.match_info['page_id'])
    resp = x.select_page(book_id, page_id)
    return web.json_response(resp, status=200)


async def getBookAuthors(request):
    book_id = str(request.match_info['book_id'])
    resp = x.select_authors_by_book(book_id)
    return web.json_response(resp, status=200)


async def getAuthors(request):
    resp = x.select_authors()
    return web.json_response(resp, status=200)


async def addBook(request):
    books = await request.json()
    resp = validBooks(books)
    if resp:
        return web.json_response(resp, status=422)
    resp = x.insert_books(books)
    return web.json_response(resp, status=200)


app = web.Application()
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})

# All GET
app.add_routes([web.get("/library/books/", getAllBooks)])
app.add_routes([web.get("/library/books/{book_id}", getBook)])
app.add_routes([web.get("/library/books/{book_id}/pages/", getBookAllPages)])
app.add_routes([web.get("/library/books/{book_id}/pages/{page_id}", getBookSinglePage)])
app.add_routes([web.get("/library/books/{book_id}/authors/", getBookAuthors)])
app.add_routes([web.get("/library/authors/", getAuthors)])

# All POST
app.add_routes([web.post("/library/books/", addBook)])
#
# # All PUT
# app.add_routes([web.put("/library/books/{book_id}", updateBook)])
#
# # All PATCH
# app.add_routes([web.patch("/library/books/{book_id}/pages/{page_id}", updateBookSinglePage)])
#
# # All DELETE
# app.add_routes([web.delete("/library/books/{book_id}", deleteBook)])
#
# # All HEAD
# app.add_routes([web.get("/library/books/{book_id}", downloadBook)])


if __name__ == '__main__':
    x = DB()
    x.create_connection()
    x.create_db()
    x.create_value()
    x.select_all_book()
    web.run_app(app)
