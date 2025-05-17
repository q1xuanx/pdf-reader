from asyncpg import Connection
from ..models.file_save import CreateFile, FileSave
from typing import List

async def save_file(conn : Connection, file : CreateFile) -> bool:
    status = await conn.execute('INSERT INTO file_save(name_file) VALUES($1)', file.name_file)
    return status.startswith('INSERT')

async def get_list_file (conn : Connection, limit : int, offset : int) -> List[FileSave]:
    records = await conn.fetch('SELECT name_file, created_date from file_save ORDER BY created_date DESC LIMIT $1 OFFSET $2', limit, offset)
    return [FileSave.from_record(record) for record in records]