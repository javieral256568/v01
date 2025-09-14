from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None

@app.post("/items/")
async def create_item(item: Item, request: Request):
    content_type = request.headers.get("content-type")
    return {
        "name": item.name,
        "description": item.description,
        "content_type": content_type
    }