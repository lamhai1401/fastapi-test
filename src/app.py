from typing import Optional, List
from fastapi import FastAPI, Body, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.gzip import GZipMiddleware


app = FastAPI()

# CORS
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://0.0.0.0:8080",
]

# app.add_middleware(HTTPSRedirectMiddleware)  # force redirect to https
app.add_middleware(GZipMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


# @app.get("/items/{item_id}")
# async def read_item(item_id):
#     return {"item_id": item_id}


# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip: skip + limit]


# @app.post("/items/")
# async def create_item(item: Item):  # khai báo dưới dạng parameter
#     resp = item.dict()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         resp.update({"price_with_tax": price_with_tax})
#     return resp


# @app.put("/items/{item_id}")
# async def create_item(item_id: int, item: Item):
#     return {"item_id": item_id, **item.dict()}


# @app.patch("/item/")
# async def update_item(
#     *,
#     item_id: int,
#     item: Item,
#     user: User,
#     importance: int = Body(..., gt=0),
#     q: Optional[str] = None
# ):
#     results = {
#         "item_id": item_id,
#         "item": item,
#         "user": user,
#         "importance": importance
#     }

#     if q:
#         results.update({"q": q})
#     return results


# @app.post("/offers/")
# async def create_offer(offer: Offer = Body(..., embed=True)):
#     return offer


# class Response(BaseModel):
#     data: Optional[str] = None
#     success: bool = False
#     # message: str


# class Message(BaseModel):
#     message: str


# responses = {
#     404: {"description": "Item not found"},
#     302: {"description": "The item was moved"},
#     403: {"description": "Not enough privileges"},
#     404: {"model": Message, "description": "The item was not found"},
#     200: {
#         "content": {"img/jpg": {}},
#         "description": "Return the JSON item or an image.",
#     }
# }


# @app.get(
#     "/resp/{data}",
#     response_model=Response,
#     responses=responses
# )
# async def read_item(item_id: str, img: Optional[bool] = None):
#     if item_id == "foo":
#         return {"id": "foo", "value": "there goes my hero"}
#     # if img:
#     #     return FileResponse("img.jpg", media_type="image/jpg")
#     else:
#         return JSONResponse(
#             status_code=status.HTTP_404_NOT_FOUND,
#             content={"message": "Item not found"})
