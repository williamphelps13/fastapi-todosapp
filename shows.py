from fastapi import FastAPI

app = FastAPI()

@app.get("/shows")
async def get_shows():
    return [
        {"name": "Game of Thrones", "network": "HBO"},
        {"name": "Stranger Things", "network": "Netflix"},
    ]