from fastapi import FastAPI
from .routers import read_pdf

app = FastAPI()
app.include_router(read_pdf.router, prefix='/pdf')