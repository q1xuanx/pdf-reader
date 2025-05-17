from fastapi import FastAPI
from .routers import read_pdf, files
from contextlib import asynccontextmanager
from .utils.database import database


@asynccontextmanager
async def lifespan(app : FastAPI):
    app.state.db_pool = await database.create_con()
    print('Connect DB success')
    yield
    await database.close_con(app.state.db_pool)
    print('Database closed')

app = FastAPI(lifespan=lifespan)

app.include_router(read_pdf.router, prefix='/pdf')
app.include_router(files.router, prefix='/s3')