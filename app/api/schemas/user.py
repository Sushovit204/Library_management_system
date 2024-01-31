from pydantic import BaseModel, EmailStr

class User(BaseModel):
    user_id : int
    name : str
    email : EmailStr
    password : str
    membership_date : str