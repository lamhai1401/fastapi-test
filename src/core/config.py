import logging
import sys
import os
from typing import List
from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret
from src.core.logging import InterceptHandler

API_PREFIX = "/api"
JWT_TOKEN_PREFIX = "Token"  # noqa: S105 在做用户校验时，需要把这个前缀加上，并加空格
VERSION = "1.0.0"
config = Config(".env")
DEBUG: bool = config("DEBUG", cast=bool, default=False)

# db config
DATABASE_URL: str = os.getenv("DB_CONNECTION") or config("DB_CONNECTION", cast=str)  # noqa: E501
HOST: str = os.getenv("HOST") or config("HOST", cast=str, default="127.0.0.1")  # noqa: E501
PORT: int = int(os.getenv("PORT")) if "PORT" in os.environ else config("PORT", cast=int, default=3306)  # noqa: E501
USER: str = os.getenv("USER") or config("USER", cast=str, default="username")
PWD: str = os.getenv("PWD") or config("PWD", cast=str, default="password")
DB: str = os.getenv("DB") or config("DB", cast=str, default="db")

SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)
PROJECT_NAME: str = config(
    "PROJECT_NAME",
    default="FastAPI example application"
)
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS", cast=CommaSeparatedStrings, default=""
)

# logging configuration
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
