# FastAPI - The Complete Course (717 - 12hrs)

## VSCode
1. `pip install ruff`
2. Install the following extensions:
   1. Code formatting, linting, import sorting: `charliermarsh.ruff`
   2. Pylance IntelliSense, linting, Python Debugger: `ms-python.python`
   3. Python Indent: `KevinRose.vsc-python-indent`
   4. Type Hints: `njqdev.vscode-python-typehint`
   5. Dependency info: `ninoseki.vscode-pylens`
3. Add the following to your `settings.json`:
```
  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.codeActionsOnSave": {
      "source.fixAll": "always",
      "source.organizeImports": "always"
    }
  },
```
4. Run `pip freeze > requirements.txt` to create a list of installed packages
5. Run `pip install -r requirements.txt` to install all the dependencies listed in the `requirements.txt`

## Setup (14)

1. `pip3 list`
   1. List python packages installed in the current environment
2. `python3 -m venv DIRECTORYenv`
   1. Run the python module venv to create a virtual environment in the current directory with the next argument as the name
   2. Can run pip3 list again and see that the venv is not yet activated
3. `source DIRECTORYenv/bin/activate`
   1. Run the activate binary thats in the new virtual environment directory to activate the virtual environment
   2. Can run pip3 list to see that there is now an active virtual environment with only the pip and the setuptools package installed
4. `deactivate`
   1. Deactivates the venv (can run pip3 list to verify)
5. `pip install fastapi`
6. `pip install "uvicorn[standard]"`
   1. Uvicorn: an ASGI (Asynchronous Server Gateway Interface) web server, known for its high performance.
   2. Uvicorn[standard]: not only installing uvicorn but also the additional packages that are part of the "standard" supporting dependencies including:
      1. click: A package for creating command-line interfaces.
      2. h11: An HTTP/1.1 parser.
      3. websockets: A library for building WebSocket servers and clients.
      4. httptools: A framework for building HTTP servers.
      5. uvloop: An alternative event loop for asyncio. It's designed to be a drop-in replacement for the standard asyncio loop.

## Project 1 - Request Method Logic (79)

### Create FastAPI App and Endpoint

1. `touch books.py`

   ```
   from fastapi import FastAPI

   app = FastAPI()

   @app.get("/books")
   async def get_books():
       return [
           {"name": "Harry Potter", "author": "J. K. Rowling"},
           {"name": "Lord of the Rings", "author": "J. R. R. Tolkien"},
       ]
   ```

   1. from fastapi import FastAPI: Imports the FastAPI class from the fastapi module.
   2. app = FastAPI(): Creates an instance of FastAPI. This instance (app) will be used to create routes/endpoints.
   3. @app.get("/books"): A decorator that tells FastAPI to execute the following function when an HTTP GET request is made to the URL path /books. This sets up a route.
   4. async def get_books(): Defines an asynchronous function get_books. The async keyword enables the function to perform asynchronous operations if needed.
   5. return [{}, {}]: The function returns a list of dictionaries

2. `uvicorn books:app --reload`
   1. uvicorn: This is the CLI for Uvicorn
   2. books: books refers to the Python file name. This file should contain your FastAPI application instance.
   3. app: is the variable name of the FastAPI instance in the books.py file. This is the application that Uvicorn will run. This app handles HTTP requests, routes them to the appropriate handler functions, and returns HTTP responses.
   4. --reload: This flag enables auto-reloading of the server when there are code changes in the file
3. Go to `http://127.0.0.1:8000/books`
4. Go to `http://127.0.0.1:8000/docs` to see swagger UI
   1. Click 'Try it Out' > 'Execute'
   2. Observe Request URL, Response Body

### Path Parameters

1. Ensure shorter and static path parameters are listed before longer and dynamic parameters because FastAPI look at functions in order from top to bottom

   ```
   @app.get("/book/{dynamic}")
   ...

   @app.get("/book/mybook")
   ...
   # the function for /mybook will never run because mybook would be caught first by /{dynamic}
   ```

2. `http://127.0.0.1:8000/books/The%Alchemist`
   1. harry%20potter: results in 'the alchemist`
3. URL: http://127.0.0.1:8000/books/the%20alchemist
   ```
   @app.get("/books/{book_title}")
   async def read_book(book_title: str): #int, float, dict, bool
       for book in BOOKS:
           if book['title'].casefold() == book_title.casefold():
               return book
       return {"message": "Book not found!"}
   ```
   Response: {"title": "The Alchemist"...}; See this in Swagger UI

### Query Parameters

1. Query paramters are:

   1. Request paramters after "?"
   2. Have name=value pairs
   3. 127.0.0.1:8000/books/?category=fantasy
   4. FastAPI has this syntax @app.get("/books/") to know that if the argument of the function matches a name in the query parameter

   ```
   @app.get("/books/")
   async def read_books_by_query(title: str, author: str, category: str):
      filtered_books = [
        book for book in BOOKS
        if book.get('title', '').casefold() == title.casefold()
        and book.get('author', '').casefold() == author.casefold()
        and book.get('category', '').casefold() == category.casefold()
      ]

      return filtered_books if filtered_books else {'message': "No books found for this query"}
   ```

## Project 2 - Move Fast (93)

```
from fastapi import FastAPI, Path, Query, HTTPException
from typing import Optional
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book: #class to have instances of Book as data instead of simply dictionaries
  id: int
  title: str
  author: str
  description: str
  rating: int
  published_date: int

  def __init__(self, id, title, author, description, rating, published_date): #constructor
    self.id = id
    self.title = title
    self.author = author
    self.description = description
    self.rating = rating
    self.published_date = published_date

class BookRequest(BaseModel): #class that uses pydantic to validate POST and PUT requests
  id: Optional[int] = None #since there is logic that will generate an incremented id this is optional
  title: str = Field(min_length=1, max_length=100) #pydantic will return error message if not between 1-100
  author: str = Field(min_length=1, max_length=100)
  description: str = Field(min_length=1, max_length=100)
  rating: int = Field(ge=1, le=5)
  published_date: int = Field(ge=1900, le=2022)

  class Config: #pydantic integrates with swagger to provide an example POST/PUT object
    json_schema_extra = {
      "example": {
        "title": "Test",
        "author": "Test",
        "description": "Test",
        "rating": 1,
        "published_date": 1900
      }
    }

BOOKS = [ #Local data; will be in a database in next project
  Book(1, "The Great Gatsby", "F. Scott Fitzgerald", "The story of the fabulously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan.", 4, 1925),
  Book(2, "To Kill a Mockingbird", "Harper Lee", "The story of a young lawyer in Alabama", 5, 1960),
  Book(3, "1984", "George Orwell", "A dystopian social science fiction novel", 4, 1949)
]

@app.get("/books")
async def read_all_books():
  return BOOKS

@app.post("/create-book", status_code=status.HTTP_201_CREATED) #If successfully creates and returns a new instance of a Book then will also return a 201
async def create_book(book_request: BookRequest): #the request will become an instance of the BookRequest class that extends pydantic BaseModel and therefore integrates validation
  new_book = Book(**book_request.model_dump()) #dumps the properties into the arguments of the Book class to create a new instance of Book
  new_book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1 #logic that increments id
  BOOKS.append(new_book)
  return new_book #POST returns what was posted and a 201 status code

@app.get("/books/{id}", status_code=status.HTTP_200_OK)
async def read_book(id: int = Path(gt=0)): #FastAPI Path first validates the path parameter
  for book in BOOKS:
    if book.id == id:
      return book
  raise HTTPException(status_code=404, detail="Book not found") #returns 404 if no match to id is found

@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(ge=1, le=5)): #FastAPI Query first validates the query parameter
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
            return #PUT does not return what was updated but returns a 204 status code
    raise HTTPException(status_code=404, detail='Book not found')

@app.delete("/books/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: int = Path(gt=0)):
    for i, existing_book in enumerate(BOOKS):
        if existing_book.id == book_id:
            return BOOKS.pop(i) #DELETE does could return what was deleted and if it does also maybe returns a 200 status code
    raise HTTPException(status_code=404, detail='Book not found')
```

## Setup Database (51)
1. Create database.py - Database Configuration and Session Creation File
   1. Purpose: Establishes the connection to the database using SQLAlchemy. This includes setting up the database engine and session factory, which are crucial for interacting with the database in an object-oriented manner.
   2. Key Components:
      1. Database Engine: Responsible for connecting to the database. It's configured to connect to a SQLite database for this example.
      2. Session Factory (SessionLocal): A configured sessionmaker that creates sessions for database operations, allowing for transactions and queries to be executed.
      3. Declarative Base (Base): A base class for all model classes to inherit from. It ties the models to the engine and helps SQLAlchemy recognize them as part of the ORM.
```
# This code sets up the database for a FastAPI app, using SQLAlchemy, a tool that lets us work with databases in a more Pythonic way.
# Instead of writing SQL queries, we can use Python code to interact with our database, making it easier to create, read, update, and delete data.

from sqlalchemy import (
    create_engine,
)  # This line imports a function to create a connection to our database.
from sqlalchemy.orm import (
    sessionmaker,
)  # This imports a function to make sessions, which are used to manage our database operations safely.
from sqlalchemy.ext.declarative import (
    declarative_base,
)  # This imports a function to create a base class for our database models.

# This is the path to our database file. We're using SQLite here, which is a simple file-based database.
SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"

# Here we're setting up the connection to our database using the URL we defined. The 'check_same_thread: False' part is specific to SQLite and makes it work with FastAPI's async features.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# This line sets up a "factory" for our sessions. Each session is a temporary connection to the database, letting us make changes or get data.
# We're turning off some automatic features (autocommit and autoflush) to have more control over when data is actually saved or updated.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This line creates a base class for our models. In SQLAlchemy, models are Python classes that represent tables in our database.
# By inheriting from this base class, we can define the structure of our database in a clean, organized way.
Base = declarative_base()
```
2. Create models.py
   1. Purpose: Defines the structure of the database tables in terms of Python classes. Each class corresponds to a database table, and instances of these classes represent rows in their respective tables.
   2. Key Components:
      1. User Model: Represents users in the application, including fields like id, email, username, etc. It uses SQLAlchemy column types to define the data type and constraints for each column.
      2. Todo Model: Represents todo items associated with users. It includes fields for managing todo items, such as title, description, priority, and a foreign key to associate todos with users.
```
# First, we import 'Base' from our database setup to use as a foundation for our models.
# We also import various column types to define the data each column will hold.
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from database import Base


# Defining a Users table to store user information.
class Users(Base):
    __tablename__ = "users"  # The name of the table in the database.

    # Here we define the columns in the table and their data types:
    id = Column(
        Integer, primary_key=True, index=True
    )  # A unique ID for each user, used as the primary key, indexed for faster query performance
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)


# Defining a Todos table for storing todo items related to users.
class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(
        Boolean, default=False
    )  # If not complete value is provided this will default to False (0)
    owner_id = Column(
        Integer, ForeignKey("users.id")
    )  # Links each todo to a user in the Users table.
```
3. Create main.py - FastAPI Application Initialization File
   1. Purpose: Initializes the FastAPI application, imports the models, and creates the database tables if they don't exist yet. This file is the entry point for the web application, defining the FastAPI app instance and setting up the database.
   2. Key Components:
      1. FastAPI App Instance: The main object that FastAPI uses to create your web application. It handles incoming requests and routes them to the appropriate function.
      2. Database Table Creation: Uses the SQLAlchemy models to create database tables according to the defined schemas if they are not already present in the database.
4. uvicorn main:app --reload
   1. Starts up FastAPI app in development server which also creates todosapp.db
5. sqlite3 todosapp.db
6. Improve developer experience:
   1. .mode box
   2. .tables
   3. .schema todos
7. POST, GET, PUT, DELETE using SQL:
   1. INSERT INTO todos(title, description, priority, complete, owner_id) VALUES ('Learn FastAPI', 'Working on db', 5, False, 1);
   2. SELECT * FROM todos;
   3. UPDATE todos SET complete = 1 WHERE id = 1;
   4. DELETE FROM todos WHERE id = 1;

## API Request Methods (34)

## Authentication & Authorization (94)

## Authenticate Requests (44)

## Large Production Database Setup (58)

## Project 3.5 - Alembic Data Migration (37)

## Project 4 - Full Stack Application (196)

## Deploying (17)
