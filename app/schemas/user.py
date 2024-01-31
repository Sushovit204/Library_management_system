from pydantic import BaseModel, EmailStr
from datetime import date

class Users(BaseModel):
    name : str
    email : EmailStr
    password : str
    membership_date : date

class UsersResponse(BaseModel):
    name : str
    email : str
    membership_date : date