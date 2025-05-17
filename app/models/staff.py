from pydantic import BaseModel

class Staff(BaseModel): 
    id_staff : str
    name_staff : str 
    level_approve : str
    note : str