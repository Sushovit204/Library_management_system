from schemas.user import Users
from psycopg2 import DatabaseError, OperationalError, ProgrammingError
from fastapi import HTTPException, status, APIRouter
from db.database import create_connection, create_cursor
import utilis

# Create a connection
mydb = create_connection()

# Create a cursor
mycursor = create_cursor(mydb)

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

#creating new users
@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_user(user:Users):
    try:
        #Hashing the password
        hashed_password = utilis.hash(user.password)
        user.password = hashed_password

        query = "INSERT INTO USERS(name, email, password, membership_date) VALUES (%s,%s,%s,%s)"
        val = (user.name, user.email, user.password, user.membership_date)
        mycursor.execute(query, val)
        mydb.commit()
        return{"data":"User Created Successfully"}
    
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