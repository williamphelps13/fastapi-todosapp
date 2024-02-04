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
