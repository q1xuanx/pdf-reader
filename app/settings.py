import os
from dotenv import load_dotenv

load_dotenv()

class Setting: 
    PROJECT_NAME : str = 'PDF READER'
    VERSION : str= '1.0.1'

    POSTGRES_USER : str = os.getenv('username_db')
    POSTGRES_PASSWORD : str = os.getenv('password')
    POSTGRES_PORT : str = os.getenv('port')
    POSTGRES_DB : str = os.getenv('db_name')
    POSTGRES_SERVER : str = os.getenv('server_db')
    DATABASE_URL : str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

settings = Setting