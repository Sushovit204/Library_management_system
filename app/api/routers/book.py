from schemas.book import Books
from psycopg2 import DatabaseError, OperationalError, ProgrammingError
from fastapi import HTTPException, status, APIRouter
from db.database import create_connection, create_cursor


# Create a connection
mydb = create_connection()

# Create a cursor
mycursor = create_cursor(mydb)

router = APIRouter(
    prefix="/book",
    tags=["Book"]
)

# creating a new book entry
@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_book(book:Books):
    try:
        query = "INSERT INTO BOOKS(title, isbn, published_date, genre) VALUES (%s,%s,%s,%s)"
        val = (book.title, book.isbn, book.published_date, book.genre)
        mycursor.execute(query, val)
        mydb.commit()
        return{"data":"Book Created Successfully"}
    
    except (ProgrammingError, OperationalError, DatabaseError) as e:
        print(f"Database Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e
    
    finally:
        mycursor.close()
        mydb.close()
        