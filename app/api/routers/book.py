from schemas.book import Books
from schemas.book_detail import BookDetails
from psycopg2 import DatabaseError, OperationalError, ProgrammingError
from fastapi import HTTPException, status, APIRouter
from db.database import create_connection, create_cursor
from typing import List

# Router for book api where prefix is url and tags is used for grouping in API documentation
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
    
    # catching and loging the errors
    except (ProgrammingError, OperationalError, DatabaseError) as e:
        print(f"Database Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e
    
    finally:
        # closing cursor object and database
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

# Assign/Update Book Details: Endpoint to assign details to a book or update existing book details
@router.put("/update/{book_id}", status_code=status.HTTP_200_OK)
def assign_update_book_details(book_id: int, book_details: BookDetails):
    try:
        # Create a connection
        mydb = create_connection()

        # Create a cursor
        mycursor = create_cursor(mydb)

        # Check if a row with the specified book_id exists in book_details
        query_check = "SELECT details_id FROM BOOK_DETAILS WHERE book_id=%s"
        val_check = (book_id,)
        mycursor.execute(query_check, val_check)
        existing_details_id = mycursor.fetchone()

        if existing_details_id:
            # If a row exists, update it
            query_update = "UPDATE BOOK_DETAILS SET number_of_pages=%s, publisher=%s, language=%s WHERE book_id=%s"
            val_update = (book_details.number_of_pages, book_details.publisher, book_details.language, book_id)
            mycursor.execute(query_update, val_update)
        else:
            # If no row exists, insert a new row
            query_insert = "INSERT INTO BOOK_DETAILS(book_id, number_of_pages, publisher, language) VALUES (%s, %s, %s, %s)"
            val_insert = (book_id, book_details.number_of_pages, book_details.publisher, book_details.language)
            mycursor.execute(query_insert, val_insert)

        # Commit the transaction
        mydb.commit()

        return {"data": f"Book details updated successfully for BookID {book_id}"}

    except (ProgrammingError, OperationalError, DatabaseError) as e:
        print(f"Database Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e

    finally:
        mycursor.close()
        mydb.close()
        