from database import SessionLocal
from sqlalchemy.sql import text  # Import text for executing raw SQL

def seed_data():
    with SessionLocal().bind.connect() as connection:
        transaction = connection.begin()  # Start a transaction
        try:
            with open("sql-scripts/2-data.sql", "r") as file:
                sql_script = file.read()
                # Split the script into individual statements
                statements = sql_script.split(";")
                for statement in statements:
                    statement = statement.strip()
                    if statement:  # Skip empty statements
                        connection.execute(text(statement))  # Execute each statement
            transaction.commit()  # Explicitly commit the transaction
            print("SQL script executed successfully!")
        except Exception as e:
            transaction.rollback()  # Rollback the transaction in case of an error
            print(f"Error executing SQL script: {e}")

if __name__ == "__main__":
    seed_data()
