from fastapi import FastAPI

app = FastAPI()

SHOWS = [
    {"name": "Breaking Bad", "network": "AMC"},
    {"name": "The Wire", "network": "HBO"},
    {"name": "Game of Thrones", "network": "HBO"},
    {"name": "Stranger Things", "network": "Netflix"},
]


@app.get("/shows")
async def get_shows():
    return SHOWS
