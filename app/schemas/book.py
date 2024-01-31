from pydantic import BaseModel

class Books(BaseModel):
    title : str
    isbn : str 
    published_date : str
    genre : str 