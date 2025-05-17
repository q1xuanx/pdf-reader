from pydantic import BaseModel
from typing import List
class TableData(BaseModel): 
    idReceive : str
    nameBankReceive: str
    accountNumber : str
    nameAccount : str 
    description: str 
    moneyPay : str
    content : str

class ExtractPdf(BaseModel): 
    name_company : str | None = None
    checked_data : List | None = None
    data_table : List[TableData] | None = None
    money_type : str | None = None
    turn : str | None = None
    total_by_text : str | None = None
    total_by_num : str | None = None

class ExtractResponse(BaseModel): 
    code : int
    status : bool
    message : str
    data : ExtractPdf | None = None