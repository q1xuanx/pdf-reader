from fastapi import APIRouter, Depends
from asyncpg import Connection
from ..schema.file_request import FileRequest, FileResponse
from ..schema.data_table import ExtractResponse
from ..services import pdf_services
from app.dependencies import get_db_pool



router = APIRouter(tags=['read-pdf'])

@router.post('/read') 
async def read_pdf(file : FileRequest, conn : Connection = Depends(get_db_pool)) -> ExtractResponse:
    return await pdf_services.read_file_pdf(conn, file.fileData, file.fileName)

@router.get('/download')
def download_pdf(fileName : str) -> FileResponse: 
    return pdf_services.download_file(fileName)