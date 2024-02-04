from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from models import Base
from routers import admin, auth, todos, users

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://williamjphelps.com/todosapp"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
