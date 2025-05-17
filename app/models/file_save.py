from pydantic import BaseModel
from datetime import datetime


class CreateFile(BaseModel): 
    name_file : str

class FileSave(CreateFile): 
    created_date : datetime
    @classmethod
    def from_record(cls, record): 
        return cls(**dict(record))