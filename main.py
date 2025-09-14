from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None

@app.post("/items/")
async def create_item(item: Item):
    return {"name": item.name, "description": item.description}