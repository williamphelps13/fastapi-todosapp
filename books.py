from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {'title': "The Alchemist", 'author': "Paulo Coelho", 'category': "Adventure"},
    {'title': "The Prophet", 'author': "Kahlil Gibran", 'category': "Philosophy"},
    {'title': "The Little Prince", 'author': "Antoine de Saint-Exupery", 'category': "Philosophy"},
    {'title': "The Book Thief", 'author': "Markus Zusak", 'category': "Historical Fiction"},
    {'title': "The Hobbit", 'author': "J.R.R. Tolkien", 'category': "Fantasy"},
    {'title': "The Lord of the Rings", 'author': "J.R.R. Tolkien", 'category': "Fantasy"},
    {'title': "Harry Potter and the Philosopher's Stone", 'author': "J.K. Rowling", 'category': "Fantasy"},
]

@app.get("/")
async def bookstore():
    return {"message": "Welcome to the Bookstore!"}

@app.get("/books")
async def read_all_books():
    return BOOKS