from app.fastapi_handle.main import app, get_db


@app.get("/history")
def get_history(user_id):
    return
