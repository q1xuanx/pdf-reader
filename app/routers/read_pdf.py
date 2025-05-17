from fastapi import APIRouter
from ..models.file_request import FileRequest, FileResponse
from ..models.data_table import ExtractResponse
from ..services import pdf_services

router = APIRouter(tags=['read-pdf'])

@router.post('/read') 
def read_pdf(file : FileRequest) -> ExtractResponse:
    return pdf_services.read_file_pdf(file.fileData, file.fileName)

@router.get('/download')
def download_pdf(fileName : str) -> FileResponse: 
    return pdf_services.download_file(fileName)