from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI

# Config DB
TORTOISE_ORM = {
    "connections": {
        "default": "mysql://username:password@127.0.0.1:3306/asynctest"
    },
    "apps": {
        "models": {
            "models": ["src.models"],
            "default_connection": "default"
        }
    },
}


def connectDB(app: FastAPI):
    register_tortoise(
        app=app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True
    )
