from pydantic import BaseModel, EmailStr

class Users(BaseModel):
    name : str
    email : EmailStr
    password : str
    membership_date : str