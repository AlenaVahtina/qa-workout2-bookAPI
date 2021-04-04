from aiohttp import web
import aiohttp_cors
import logging
import json
import datetime
from db import DB

logging.basicConfig(level="DEBUG")


async def getAllBooks(request):
    db.select_all_book()



app = web.Application()
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})

# # All GET
app.add_routes([web.get("/library/books/", getAllBooks)])
# app.add_routes([web.get("/library/books/{book_id}", getBook)])
# app.add_routes([web.get("/library/books/{book_id}/pages/", getBookAllPages)])
# app.add_routes([web.get("/library/books/{book_id}/pages/{page_id}", getBookSinglePage)])
# app.add_routes([web.get("/library/books/{book_id}/authors/", getBookAuthors)])
# app.add_routes([web.get("/library/authors", getAuthors)])
# app.add_routes([web.get("/library/authors/{author_id}/books/", getAuthorBooks)])
#
# # All POST
# app.add_routes([web.post("/library/books/", addBook)])
# app.add_routes([web.post("/library/authors/{author_id}", addAuthorBooks)])
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
# app.add_routes([web.get("/library/books/{book_id}", getBookHEAD)])


# for route in list(app.router.routes()):
#     cors.add(route)

if __name__ == '__main__':
    x = DB()
    x.create_connection()
    x.create_db()
    x.create_value()
    x.select_all_book()
    web.run_app(app)
