from app.settings import settings
import asyncpg

async def create_con(): 
    return await asyncpg.create_pool(
        user=settings.POSTGRES_USER, 
        password=settings.POSTGRES_PASSWORD,
        database=settings.POSTGRES_DB,
        host=settings.POSTGRES_SERVER,
        port=settings.POSTGRES_PORT
    )

async def close_con(pool):
    await pool.close()