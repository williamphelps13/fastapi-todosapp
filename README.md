# FastAPI - The Complete Course (717 - 12hrs)

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
7. `touch books.py`

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

8. `uvicorn books:app --reload`
   1. uvicorn: This is the CLI for Uvicorn
   2. books: books refers to the Python file name. This file should contain your FastAPI application instance.
   3. app: is the variable name of the FastAPI instance in the books.py file. This is the application that Uvicorn will run. This app handles HTTP requests, routes them to the appropriate handler functions, and returns HTTP responses.
   4. --reload: This flag enables auto-reloading of the server when there are code changes in the file
9. Go to `http://127.0.0.1:8000/books`
10. Go to `http://127.0.0.1:8000/docs` to see swagger UI
    1.  Click 'Try it Out' > 'Execute'
    2.  Observe Request URL, Response Body

## Project 1 - Request Method Logic (79)

## Project 2 - Move Fast (93)

## Setup Database (51)

## API Request Methods (34)

---

## Authentication & Authorization (94)

## Authenticate Requests (44)

## Large Production Database Setup (58)

## Project 3.5 - Alembic Data Migration (37)

## Project 4 - Full Stack Application (196)

## Deploying (17)
