from fastapi import FastAPI, HTTPException, status
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os

# Loading environment varibales
load_dotenv()

app = FastAPI()

# Connect to PostgreSQL database
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
)

# Execute SQL commands
def execute_sql_command(command: str):
    try:
        with conn.cursor() as cursor:
            cursor.execute(command)
        conn.commit()
        print("Database successfully created")
    except Error as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e

@app.on_event("startup")
async def startup_event():
    print(os.getcwd())

    # Initialize tables and data on startup
    execute_sql_command(open("db/create_tables.sql").read())

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}
