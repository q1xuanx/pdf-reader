from pydantic import BaseModel
from typing import List
from ..models.file_save import FileSave
class FileRequest(BaseModel):
    fileName : str 
    fileData : str

class FileResponse(BaseModel):
    code : int
    message : str 

class FileDownload(FileResponse): 
    code: int
    message : str
    fileName : str | None = None
    url : str  | None = None
    expires_in : int | None = None

class ListFileUploaded(FileResponse):
    data : List[FileSave] | None = None
