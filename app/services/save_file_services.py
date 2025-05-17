import boto3
from typing import List
from ..crud import file_save
from asyncpg import Connection
from ..models.file_save import CreateFile, FileSave
from ..schema.file_request import FileResponse, FileDownload, ListFileUploaded

bucket_name = 'iamtest001122-save-pdf-bucket'
s3 = boto3.client('s3')

async def save_file(conn : Connection, file_name : str) -> bool:
    try: 
        status = await file_save.save_file(conn, CreateFile(name_file=file_name))
        if not status:
            return False
        s3.upload_file(file_name, bucket_name, f"pdfs/{file_name}")
        return True
    except Exception as e:
        print(e)
        return False 


def download_file(fileName : str): 
    object_download = f'pdfs/{fileName}'
    try: 
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_download},
            ExpiresIn=3600
        )
        return FileDownload(
            code=200,
            message='Download success',
            fileName=fileName,
            url=url,
            expires_in=3600
        )
    except Exception as e: 
        return FileDownload(
            code=400,
            message='File not found'
        )

async def get_list_pdf_uploaded(conn : Connection, limit : int, offset : int) -> List[FileSave]: 
    list_data = await file_save.get_list_file(conn, limit, offset)
    return ListFileUploaded(
        code=200,
        message='Success',
        data=list_data
    )