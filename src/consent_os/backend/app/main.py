import uvicorn
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


def init_db():
    from app.sql_handle.database import engine
    from app.sql_handle.base import Base

    # ВАЖНО: импортируем ТОЛЬКО один источник моделей
    import app.sql_handle.models  # noqa: F401

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    uvicorn.run("app.fastapi_handle.main:app", reload=True)
