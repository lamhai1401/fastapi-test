from fastapi import FastAPI, Depends
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_queryset_creator
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# CORS
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8000",
]

# Config DB
TORTOISE_ORM = {
    "connections": {
        # "default": "sqlite://:memory:",
        "default": "mysql://username:password@127.0.0.1:3306/asynctest"
    },
    "apps": {
        "models": {
            "models": ["src.models"],
            "default_connection": "default"
        }
    },
}
app = FastAPI(debug=False)

register_tortoise(
    app=app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True
)

# add middleware
app.add_middleware(GZipMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}