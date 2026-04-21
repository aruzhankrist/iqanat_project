from app.fastapi_handle.main import app, get_db


@app.get("/settings")
def get_settings(user_id: str):
    return
