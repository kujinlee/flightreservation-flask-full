"""
Configuration for pytest and test fixtures for the Flight Reservation Flask Application.
"""

import os
import sys
import pytest
from database import init_db, SessionLocal

# Add the project root directory to the Python module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app as flask_app  # Import after modifying sys.path

@pytest.fixture(scope="module")
def app():
    """
    Provide a Flask app instance for testing.
    """
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Use in-memory SQLite for testing
    with flask_app.app_context():
        init_db()  # Initialize the database schema
    yield flask_app

@pytest.fixture(scope="module")
def client(app):
    """
    Provide a test client for the Flask app.
    """
    return app.test_client()

@pytest.fixture(scope="function")
def db_session():
    """
    Provide a database session for testing.
    """
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()
