from typing import Dict, List, Optional
from tortoise import Tortoise
from src.core.config import DATABASE_URL, HOST, PORT, DB, PWD, USER
from fastapi import FastAPI
from loguru import logger
from tortoise.contrib.fastapi import register_tortoise

# Config DB
TORTOISE_ORM = {
    "connections": {
        # "default": {
        #     "engine": "tortoise.backends.aiomysql",
        #     "credentials": {
        #         "host": "127.0.0.1",
        #         "port": "3306",
        #         "user": "username",
        #         "password": "password",
        #         "database": "asynctest"
        #     }
        # },
        "default": DATABASE_URL
    },
    "apps": {
        "models": {
            "models": ['src.models'],
            "default_connection": "default"
        }
    },
}


TORTOISE_ORM_1 = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql.client.MySQLClientl",
            "credentials": {
                "host": HOST,
                "port": PORT,
                "user": USER,
                "password": PWD,
                "database": DB
            }
        }
    },
    "apps": {
        "models": {
            "models": ['src.models'],
            "default_connection": "default"
        }
    }
}


def connectDB(app: FastAPI):
    logger.info("Connecting to {0}", repr(DATABASE_URL))
    register_tortoise(
        app=app,
        config=TORTOISE_ORM_1,
        generate_schemas=True,
        add_exception_handlers=True
    )


async def init_orm() -> None:
    await Tortoise.init(
        config=TORTOISE_ORM,
        # modules={'models': ['__main__']}  # Change here
        # config_file=None,
        # db_url=DATABASE_URL,
        # _create_db=True,
    )
    await Tortoise.generate_schemas()
    logger.info('Tortoise-ORM started, ${}, ${}'.format(Tortoise._connections, Tortoise.apps))
    # register_tortoise(
    #     app=app,
    #     config=TORTOISE_ORM,
    #     generate_schemas=True,
    #     add_exception_handlers=True
    # )


async def close_orm():
    await Tortoise.close_connections()
    logger.info('Tortoise-ORM shutting down.')
