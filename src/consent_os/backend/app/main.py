import uvicorn
import sys
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app.sql_handle.database import engine
from app.sql_handle.models import Base


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    uvicorn.run("app.fastapi_handle.main:app", reload=True)
