from pydantic import BaseModel
    
class FileRequest(BaseModel):
    fileName : str 
    fileData : str


class FileResponse(BaseModel): 
    code: int
    message : str
    fileName : str | None = None
    url : str  | None = None
    expires_in : int | None = None

