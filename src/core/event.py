from typing import Callable
from fastapi import FastAPI
from loguru import logger
from src.db import connectDB


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        connectDB(app)
    return start_app
