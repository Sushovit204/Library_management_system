from pydantic import BaseModel
from datetime import date


class Books(BaseModel):
    title : str
    isbn : str 
    published_date : date
    genre : str 