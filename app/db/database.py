import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import Error

# Loading environment varibales
load_dotenv()

# Connect to PostgreSQL database
def create_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        print("Connected Successfuly to Database")
        return conn

    except Error as e:
        print(f"Error Connecting to database: {e}")
        raise

# creating a cursor object for later use 
def create_cursor(conn):
    return conn.cursor()