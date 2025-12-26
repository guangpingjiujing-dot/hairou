from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI(title="シンプルシステムAPI", description="シンプルなFastAPI")

class Item(BaseModel):
    name: str
    is_done: bool = False

items = []

@app.get("/")
def root():
    return {"message": "Hello, World!"}

# curl.exe -X POST -H "Content-Type: application/json" "http://127.0.0.1:8000/items?item=apple"
# curl.exe -X POST -H "Content-Type: application/json" -d "{`"name`": `"apple`", `"is_done`": false}" "http://127.0.0.1:8000/items"

@app.post("/items")
# def create_item(item: str):
def create_item(item: Item):
    items.append(item)
    return items

# curl.exe -X GET -H "Content-Type: application/json" "http://127.0.0.1:8000/items"
@app.get("/items")
def get_items():
    return items

# curl.exe -X GET -H "Content-Type: application/json" "http://127.0.0.1:8000/items/0"
@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")
    item = items[item_id]
    return item
