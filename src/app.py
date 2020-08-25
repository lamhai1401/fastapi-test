from typing import Optional, List
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()
fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]


class Image(BaseModel):
    url: str
    name: str


class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        None,
        title="The desc of the item",
        max_length=300
    )
    price: float = Field(
        ...,
        gt=0,
        description="The price must the greater than 0"
    )
    tax: Optional[float] = None
    tags: List[str] = []
    image: Optional[List[Image]] = None


class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    items: List[Item]


class User(BaseModel):
    username: str
    full_name: Optional[str] = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


@app.post("/items/")
async def create_item(item: Item):  # khai báo dưới dạng parameter
    resp = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        resp.update({"price_with_tax": price_with_tax})
    return resp


@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}


@app.patch("/item/")
async def update_item(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: int = Body(..., gt=0),
    q: Optional[str] = None
):
    results = {
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance
    }

    if q:
        results.update({"q": q})
    return results


@app.post("/offers/")
async def create_offer(offer: Offer = Body(..., embed=True)):
    return offer
