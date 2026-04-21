import uvicorn
import sys
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app.sql_handle.database import engine
from app.sql_handle.models import Base


Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    uvicorn.run("fastapi_handle.main:app", reload=True)
