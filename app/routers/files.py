from ..services import save_file_services
from app.dependencies import get_db_pool
from fastapi import APIRouter, Depends
from asyncpg import Connection

router = APIRouter(tags=['files'])

@router.get('/files')
async def get_list_file(conn : Connection = Depends(get_db_pool), limit : int = 10, page : int = 1): 
    return await save_file_services.get_list_pdf_uploaded(conn, limit, (page - 1) * limit)

@router.post('/download/{fileName}')
async def download_file(fileName : str):
    return save_file_services.download_file(fileName)
