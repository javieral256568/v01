from fastapi import FastAPI, Request
from pydantic import BaseModel

## .\uvicorn_start.bat
## .\uvicorn_stop.bat

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None

@app.post("/items/")
async def create_item(item: Item, request: Request):
    content_type = request.headers.get("content-type")
<<<<<<< HEAD
    print("name:",item.name," desc:",item.description)

=======
    print("name:",item.name," desc:",item.desciption)
>>>>>>> a056bd7962c5a2adb6c07ec10bcaba472afbd047
    return {
        "name": item.name,
        "description2": item.description,
        "content_type": content_type
    }
