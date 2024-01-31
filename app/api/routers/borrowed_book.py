from psycopg2 import DatabaseError, OperationalError, ProgrammingError
from fastapi import HTTPException, status, APIRouter
from db.database import create_connection, create_cursor
from datetime import date
from typing import List
from schemas.borrowed_book import BorrowedBooks

router = APIRouter(
    prefix="/books",
    tags=["Borrow"]
)


from datetime import date

@router.post("/borrow/{user_id}/{book_id}", status_code=status.HTTP_201_CREATED)
def borrow_book(user_id: int, book_id: int):
    try:
        # Create a connection
        mydb = create_connection()

        # Create a cursor
        mycursor = create_cursor(mydb)

        # Check if the user and book exist
        query_check = "SELECT user_id FROM USERS WHERE user_id=%s"
        val_check = (user_id,)
        mycursor.execute(query_check, val_check)
        existing_user_id = mycursor.fetchone()

        query_check = "SELECT book_id FROM BOOKS WHERE book_id=%s"
        val_check = (book_id,)
        mycursor.execute(query_check, val_check)
        existing_book_id = mycursor.fetchone()

        if existing_user_id and existing_book_id:
            # Insert a new row in borrowed_books
            query_insert = "INSERT INTO BORROWED_BOOKS(user_id, book_id, borrow_date) VALUES (%s, %s, %s)"
            val_insert = (user_id, book_id, date.today())
            mycursor.execute(query_insert, val_insert)
            mydb.commit()
            return {"data": f"Book borrowed successfully by UserID {user_id}"}

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} or Book with ID {book_id} not found",
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


@router.put("/return/{user_id}/{book_id}", status_code=status.HTTP_200_OK)
def return_book(user_id: int, book_id: int):
    try:
        # Create a connection
        mydb = create_connection()

        # Create a cursor
        mycursor = create_cursor(mydb)

        # Check if the user and book combination exists in borrowed_books
        query_check = "SELECT * FROM BORROWED_BOOKS WHERE user_id=%s AND book_id=%s"
        val_check = (user_id, book_id)
        mycursor.execute(query_check, val_check)
        existing_borrowed_book = mycursor.fetchone()

        if existing_borrowed_book:
            # Update the return_date in borrowed_books
            query_update = "UPDATE BORROWED_BOOKS SET return_date=%s WHERE user_id=%s AND book_id=%s"
            val_update = (date.today(), user_id, book_id)
            mycursor.execute(query_update, val_update)
            mydb.commit()

            return {"data": f"Book returned successfully by UserID {user_id}"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {book_id} is not currently borrowed by UserID {user_id}",
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


@router.get("/list_borrowed_books", response_model=List[BorrowedBooks])
def list_all_borrowed_books():
    try:
        # Create a connection
        mydb = create_connection()

        # Create a cursor
        mycursor = create_cursor(mydb)

        # Retrieve all borrowed books
        query = "SELECT user_id, book_id, borrow_date, return_date FROM BORROWED_BOOKS WHERE return_date IS NULL "
        mycursor.execute(query)
        borrowed_books = mycursor.fetchall()

        # Checking for empty data
        if not borrowed_books:
            return []
        
        # Converting tuples into dictonary
        borrowed_books_dicts = [{"user_id":borrowed_book[0], "book_id":borrowed_book[1], "borrow_date":borrowed_book[2], "return_date":borrowed_book[3]} for borrowed_book in borrowed_books]
        return borrowed_books_dicts
    
    except (ProgrammingError, OperationalError, DatabaseError) as e:
        print(f"Database Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e
    finally:
        mycursor.close()
        mydb.close()
    