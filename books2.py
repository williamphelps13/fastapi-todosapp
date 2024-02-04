from typing import Optional

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(ge=1, le=5)
    published_date: int = Field(ge=1900, le=2022)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Test Step",
                "author": "Test",
                "description": "Test",
                "rating": 1,
                "published_date": 1900,
            }
        }


BOOKS = [
    Book(
        1,
        "The Great Gatsby",
        "F. Scott Fitzgerald",
        "The story of the fabulously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan.",
        4,
        1925,
    ),
    Book(
        2,
        "To Kill a Mockingbird",
        "Harper Lee",
        "The story of a young lawyer in Alabama",
        5,
        1960,
    ),
    Book(
        3, "1984", "George Orwell", "A dystopian social science fiction novel", 4, 1949
    ),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    new_book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    BOOKS.append(new_book)
    return new_book


@app.get("/books/{id}", status_code=status.HTTP_200_OK)
async def read_book(id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(ge=1, le=5)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    if books_to_return:
        return books_to_return
    raise HTTPException(status_code=404, detail="Book not found")


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    for i, existing_book in enumerate(BOOKS):
        if existing_book.id == book.id:
            BOOKS[i] = book
            return
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: int = Path(gt=0)):
    for i, existing_book in enumerate(BOOKS):
        if existing_book.id == book_id:
            return BOOKS.pop(i)
    raise HTTPException(status_code=404, detail="Book not found")
