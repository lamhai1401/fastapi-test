from fastapi import APIRouter
from typing import List
from tortoise.contrib.fastapi import HTTPNotFoundError
from src.models.user import User, UserIn_Pydantic, User_Pydantic
router = APIRouter()


@router.get("/", response_model=List[User_Pydantic])
async def get_users():
    return await User_Pydantic.from_queryset(User.all())


@router.post("/", response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = await User.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)
