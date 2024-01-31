from fastapi import FastAPI, HTTPException, status
from psycopg2 import DatabaseError, OperationalError, ProgrammingError
from db.database import create_connection, create_cursor
import os
from api.routers import user, book, borrowed_book


app = FastAPI()

# Create a connection
mydb = create_connection()

# Create a cursor
mycursor = create_cursor(mydb)

# Execute SQL commands
def execute_sql_command(command: str):
    try:
        mycursor.execute(command)
        mydb.commit()
        print("Database successfully created")
    except (ProgrammingError, OperationalError, DatabaseError) as e:
        print(f"Database Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e

# Running this on startup to create database model if it does not exists
@app.on_event("startup")
async def startup_event():

    # for debugging case
    print(os.getcwd())

    try:
        # Initialize tables and data on startup
        execute_sql_command(open("db/create_tables.sql").read())
    except Exception as e:
        # logging the error for debugging
        print(f"Error during startup: {e}")
    finally:
        # Closing the database connection to avoid resource leak
        mycursor.close()
        mydb.close()

@app.get("/")
async def read_root():
    """Test route for seeing working of the API"""
    return {"message": "Hello, FastAPI!"}


# routers for the different API
app.include_router(user.router)
app.include_router(book.router)
app.include_router(borrowed_book.router)
