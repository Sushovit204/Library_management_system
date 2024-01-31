from pydantic import BaseModel

class BookDetails(BaseModel):
    book_id : int
    number_of_pages : int
    publisher : str
    language : str 