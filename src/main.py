import uvicorn
from .api import router
from fastapi import FastAPI, Depends
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from src.api.errors.http_error import http_error_handler
from src.api.errors.validation_error import http422_error_handler
from src.core.event import create_start_app_handler, create_end_app_handler
from src.core.config import API_PREFIX


# CORS
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8000",
]

app = FastAPI(debug=False)

# connecting to db
app.add_event_handler("startup", create_start_app_handler(app))
app.add_event_handler("shutdown", create_end_app_handler)
app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(RequestValidationError, http422_error_handler)

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

#  this imports the route in the user into the main file
app.include_router(router, prefix=API_PREFIX)
