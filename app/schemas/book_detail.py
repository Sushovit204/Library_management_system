from pydantic import BaseModel

class BookDetails(BaseModel):
    number_of_pages : int
    publisher : str
    language : str 