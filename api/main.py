from fastapi import FastAPI

from api import crud

app = FastAPI(
    title="Medical Telegram Analytics API",
    description="Analytics API for Ethiopian medical Telegram channels",
    version="1.0",
)


@app.get("/")
def home():
    return {"message": "Medical Warehouse API is running."}


@app.get(
    "/api/reports/top-products",
    summary="Top mentioned products",
)
def top_products(limit: int = 10):
    return crud.get_top_products(limit)


@app.get(
    "/api/channels/{channel_name}/activity",
    summary="Channel activity",
)
def channel_activity(channel_name: str):
    return crud.get_channel_activity(channel_name)


@app.get(
    "/api/search/messages",
    summary="Search messages",
)
def search_messages(query: str, limit: int = 20):
    return crud.search_messages(query, limit)


@app.get(
    "/api/reports/visual-content",
    summary="Visual content statistics",
)
def visual_content():
    return crud.get_visual_content()