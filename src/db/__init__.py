from tortoise.contrib.fastapi import register_tortoise
from src.core.config import DATABASE_URL
from fastapi import FastAPI
from loguru import logger

# Config DB
TORTOISE_ORM = {
    "connections": {
        "default": DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": ["src.models"],
            "default_connection": "default"
        }
    },
}


def connectDB(app: FastAPI):
    logger.info("Connecting to {0}", repr(DATABASE_URL))
    register_tortoise(
        app=app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True
    )
