"""
Utility functions for handling SQL operations in the Flight Reservation Flask Application.
"""

from sqlalchemy.sql import text

def execute_sql_script(session, file_path):
    """
    Execute an SQL script from a file.

    Args:
        session: The SQLAlchemy session to use.
        file_path: The path to the SQL script file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        sql_script = file.read()
        statements = sql_script.split(";")
        for statement in statements:
            statement = statement.strip()
            if statement:  # Skip empty statements
                session.execute(text(statement))
