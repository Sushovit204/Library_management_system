from pydantic import BaseModel

class BorrowedBooks(BaseModel):
    user_id : int
    book_id : int
    borrow_date : str
    return_date : str