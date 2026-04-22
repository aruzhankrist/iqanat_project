from fastapi import FastAPI

from app.fastapi_handle.account import app as account_router
from app.fastapi_handle.history import app as history_router
from app.fastapi_handle.settings import app as settings_router
from app.fastapi_handle.agreement import app as agreement_router


app = FastAPI()
app.include_router(agreement_router)
app.include_router(account_router)
app.include_router(settings_router)
app.include_router(history_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
