from fastapi import APIRouter
from src.api.routes.user import router as user_router

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "API Hello World"}

router.include_router(user_router, prefix="/user")
