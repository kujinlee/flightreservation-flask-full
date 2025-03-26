import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text  # Import text for executing raw SQL
import logging

# Load environment variables
load_dotenv()

# Get the database URL from the environment
DATABASE_URL = os.getenv("DATABASE_URL")
logging.info(f"MYLOG: DATABASE_URL: {DATABASE_URL}")  # Debug print to verify the value

# Ensure DATABASE_URL is not None
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

# Initialize the database engine
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Import Flight from models.py
from models import Flight  # Correct table name is already applied in models.py

# Initialize the database
def init_db():
    with engine.connect() as connection:
        with open("sql-scripts/1-schema.sql", "r") as file:
            sql_script = file.read()
            # Split the script into individual statements
            statements = sql_script.split(";")
            for statement in statements:
                statement = statement.strip()
                if statement:  # Skip empty statements
                    connection.execute(text(statement))  # Execute each statement

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
