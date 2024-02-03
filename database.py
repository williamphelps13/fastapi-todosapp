# This code sets up the database for a FastAPI app, using SQLAlchemy, a tool that lets us work with databases in a more Pythonic way.
# Instead of writing SQL queries, we can use Python code to interact with our database, making it easier to create, read, update, and delete data.

from sqlalchemy import create_engine  # This line imports a function to create a connection to our database.
from sqlalchemy.orm import sessionmaker  # This imports a function to make sessions, which are used to manage our database operations safely.
from sqlalchemy.ext.declarative import declarative_base  # This imports a function to create a base class for our database models.

# This is the path to our database file. We're using SQLite here, which is a simple file-based database.
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'

# Here we're setting up the connection to our database using the URL we defined. The 'check_same_thread: False' part is specific to SQLite and makes it work with FastAPI's async features.
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

# This line sets up a "factory" for our sessions. Each session is a temporary connection to the database, letting us make changes or get data.
# We're turning off some automatic features (autocommit and autoflush) to have more control over when data is actually saved or updated.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This line creates a base class for our models. In SQLAlchemy, models are Python classes that represent tables in our database.
# By inheriting from this base class, we can define the structure of our database in a clean, organized way.
Base = declarative_base()
