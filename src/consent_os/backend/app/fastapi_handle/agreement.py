from app.fastapi_handle.main import app, get_db


@app.get("/agreements")
def get_user_agreements(user_id: str):
    return None


@app.get("/agreements/{agreement_id}")
def get_agreement(user_id: str, agreement_id: str):
    return agreement_id


@app.get("/agreements/upload")
def get_uploaded_agreement(
    user_id: str, agreement: bytes | str, reason: str, title: str
):
    return agreement


@app.delete("/agreements/{agreement_id}/delete")
def delete_agreement(user_id):
    return


@app.get("/agreements/upload/analyse")
def analyse_agreement(agreement: bytes | str, reason: str):
    return agreement


@app.get("/contract")
def get_text(user_id: str, infomation: str):
    return "contract added"
