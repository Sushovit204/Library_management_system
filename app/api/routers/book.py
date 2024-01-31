from schemas.book import Books
from psycopg2 import DatabaseError, OperationalError, ProgrammingError
from fastapi import HTTPException, status, APIRouter
from db.database import create_connection, create_cursor
from typing import List


router = APIRouter(
    prefix="/book",
    tags=["Book"]
)

# creating a new book entry
@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_book(book:Books):
    try:
        # Create a connection
        mydb = create_connection()

        # Create a cursor
        mycursor = create_cursor(mydb)

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

# endpoint to list all books
@router.get("/list", response_model=List[Books])
def list_all_books():
    try:
        # Create a connection
        mydb = create_connection()

        # Create a cursor
        mycursor = create_cursor(mydb)

        query = "SELECT * FROM BOOKS"
        mycursor.execute(query)
        books = mycursor.fetchall()

        # Check if the result set is empty
        if not books:
            return []

        # Convert tuples to dictionaries
        book_dicts = [{"title": book[1], "isbn": book[2], "published_date": book[3], "genre": book[4]} for book in books]
        return book_dicts
    except (ProgrammingError, OperationalError, DatabaseError) as e:
        print(f"Database Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e
    finally:
        mycursor.close()
        mydb.close()

# endpoint to get user by id
@router.get("/{book_id}", response_model=Books)
def get_user_by_id(book_id: int):
    try:
        # Create a connection
        mydb = create_connection()

        # Create a cursor
        mycursor = create_cursor(mydb)

        query = "SELECT * FROM BOOKS WHERE book_id = %s"
        val = (book_id,)
        mycursor.execute(query, val)
        book = mycursor.fetchone()
        
        if book:
            # Convert tuples to dictionaries
            user_dict = {"title": book[1], "isbn": book[2], "published_date": book[3], "genre": book[4]}
            return user_dict
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {book_id} not found",
            )
    except (ProgrammingError, OperationalError, DatabaseError) as e:
        print(f"Database Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e
    finally:
        mycursor.close()
        mydb.close()
        