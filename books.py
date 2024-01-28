from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def bookstore():
    return {"message": "Welcome to the Bookstore!"}

@app.get("/books")
async def read_all_books():
    return [
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
        {"title": "The Trial", "author": "Franz Kafka"},
    ]