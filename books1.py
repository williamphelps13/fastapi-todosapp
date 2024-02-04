from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {"title": "The Alchemist", "author": "Paulo Coelho", "category": "Adventure"},
    {"title": "The Prophet", "author": "Kahlil Gibran", "category": "Philosophy"},
    {
        "title": "The Little Prince",
        "author": "Antoine de Saint-Exupery",
        "category": "Philosophy",
    },
    {
        "title": "The Book Thief",
        "author": "Markus Zusak",
        "category": "Historical Fiction",
    },
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "category": "Fantasy"},
    {
        "title": "The Lord of the Rings",
        "author": "J.R.R. Tolkien",
        "category": "Fantasy",
    },
    {
        "title": "Harry Potter and the Philosopher's Stone",
        "author": "J.K. Rowling",
        "category": "Fantasy",
    },
]


@app.get("/")
async def bookstore():
    return {"message": "Welcome to the Bookstore!"}


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/my-book")
async def get_my_book():
    return {"message": "My favorite book is Wallflower"}


@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book["title"].casefold() == book_title.casefold():
            return book
    return {"message": "Book not found for this title"}


@app.get("/{dynamic_param}")
async def read_dynamic_param(dynamic_param: str):
    return {"dynamic_param": dynamic_param}


@app.get("/books/{book_author}/")
async def read_category_by_query(book_author: str, category: str):
    filtered_books = []
    for book in BOOKS:
        if (
            book["author"].casefold() == book_author.casefold()
            and book["category"].casefold() == category.casefold()
        ):
            filtered_books.append(book)

    if filtered_books:
        return filtered_books
    return {"message": "No books found for this title and query"}


@app.get("/books/")
async def read_books_by_query(title: str, author: str, category: str):
    filtered_books = [
        book
        for book in BOOKS
        if book.get("title", "").casefold() == title.casefold()
        and book.get("author", "").casefold() == author.casefold()
        and book.get("category", "").casefold() == category.casefold()
    ]

    return (
        filtered_books
        if filtered_books
        else {"message": "No books found for this query"}
    )
