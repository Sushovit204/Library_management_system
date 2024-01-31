from pydantic import BaseModel
from datetime import date

class BorrowedBooks(BaseModel):
    """"schema validation for borrowedbooks"""
    user_id : int
    book_id : int
    borrow_date : date
    return_date : None
