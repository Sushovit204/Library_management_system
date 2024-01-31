from schemas.user import Users, UsersResponse
from psycopg2 import DatabaseError, OperationalError, ProgrammingError
from fastapi import HTTPException, status, APIRouter
from db.database import create_connection, create_cursor
import utilis
from typing import List


router = APIRouter(
    prefix="/user",
    tags=["User"]
)

# endpoint for creating new users
@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_user(user:Users):
    try:
        # Create a connection
        mydb = create_connection()

        # Create a cursor
        mycursor = create_cursor(mydb)
        #Hashing the password
        hashed_password = utilis.hash(user.password)
        user.password = hashed_password

        query = "INSERT INTO USERS(name, email, password, membership_date) VALUES (%s,%s,%s,%s)"
        val = (user.name, user.email, user.password, user.membership_date)
        with mydb.cursor() as cursor:
            cursor.execute(query, val)
            mydb.commit()
        return {"data": "User Created Successfully"}
    
    except (ProgrammingError, OperationalError, DatabaseError) as e:
        print(f"Database Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e
    # except psycopg2.IntegrityError as e:
        
    #     #Throws error if email already in use
    #     if "email" in str (e):
    #         raise HTTPException(status_code=status.HTTP_409_CONFLICT,
    #                             detail="Email already in use")
    finally:
        mycursor.close()
        mydb.close()


# endpoint to list all users
@router.get("/list", response_model=List[UsersResponse])
def list_all_users():
    try:
        # Create a connection
        mydb = create_connection()

        # Create a cursor
        mycursor = create_cursor(mydb)
        query = "SELECT name, email, membership_date FROM USERS"
        mycursor.execute(query)
        users = mycursor.fetchall()

        # Convert tuples to dictionaries
        user_dicts = [{"name": user[0], "email": user[1], "membership_date": user[2]} for user in users]
        return user_dicts
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
@router.get("/{user_id}", response_model=UsersResponse)
def get_user_by_id(user_id: int):
    try:
        # Create a connection
        mydb = create_connection()

        # Create a cursor
        mycursor = create_cursor(mydb)

        query = "SELECT name, email, membership_date FROM USERS WHERE user_id = %s"
        val = (user_id,)
        mycursor.execute(query, val)
        user = mycursor.fetchone()
        if user:
            # Convert tuples to dictionaries
            user_dict = {"name": user[0], "email": user[1], "membership_date": user[2]}
            return user_dict
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found",
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