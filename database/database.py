"""
Database configuration and initialization for the Flight Reservation Flask Application.
"""

import os
import logging
import time  # Add this import
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.sql_utils import execute_sql_script  # Import the utility function

# Load environment variables
load_dotenv()

# Get the database URL from the environment
DATABASE_URL = os.getenv("DATABASE_URL")
logging.info("MYLOG: DATABASE_URL: %s", DATABASE_URL)  # Use lazy % formatting

# Ensure DATABASE_URL is not None
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

# Initialize the database engine
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initialize the database by executing the schema SQL script.
    """
    retries = 5  # Number of retries
    while retries > 0:
        try:
            with engine.connect() as connection:
                execute_sql_script(connection, "sql-scripts/1-schema.sql")  # Use utility function
                break  # Exit the loop if successful
        except Exception as e:
            logging.error("Database connection failed: %s. Retrying in 5 seconds...", e)
            retries -= 1
            time.sleep(5)  # Wait before retrying
    if retries == 0:
        raise Exception("Failed to connect to the database after multiple retries.")

def get_db():
    """
    Dependency to get the database session.
    """
    db = SessionLocal()  # Create a new database session
    try:
        yield db  # Provide the session to the caller
    finally:
        db.close()  # Ensure the session is closed after use
