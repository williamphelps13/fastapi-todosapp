from fastapi import FastAPI  # Import the FastAPI class to create your web app.
import models  # Import your SQLAlchemy models that define your database schema.
from database import engine  # Import the SQLAlchemy engine for database connection.

app = FastAPI()  # Create an instance of the FastAPI class. This object provides all the web app functionalities.

models.Base.metadata.create_all(bind=engine)  # Create the database tables based on your models if they don't already exist