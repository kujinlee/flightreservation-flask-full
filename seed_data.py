"""
Script to seed the database with initial data for the Flight Reservation Flask Application.
"""

from sqlalchemy.exc import SQLAlchemyError  # Import specific SQLAlchemy exceptions
from database import SessionLocal
from utils.sql_utils import execute_sql_script  # Import the utility function

def seed_data():
    """
    Seed the database with initial data.
    """
    with SessionLocal() as session:
        try:
            execute_sql_script(session, "sql-scripts/2-seed.sql")  # Use utility function
            session.commit()
        except SQLAlchemyError as exc:  # Catch specific SQLAlchemy exceptions
            session.rollback()
            print(f"Error seeding data: {exc}")

if __name__ == "__main__":
    seed_data()
