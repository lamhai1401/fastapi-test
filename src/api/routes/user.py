from fastapi import APIRouter
from typing import List
from fastapi import HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from src.models import User, UserIn_Pydantic, User_Pydantic, Response
router = APIRouter()


@router.get("/", response_model=List[User_Pydantic])
async def get_users():
    return await User_Pydantic.from_queryset(User.all())


@router.post("/", response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = await User.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.get(
    "/{user_id}",
    response_model=User_Pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_user(user_id: int):
    try:
        return await User_Pydantic.from_queryset_single(User.get(id=user_id))
    except Exception as ex:
        raise HTTPException(
                status_code=404,
                detail="User with id {} not found err: {}".format(user_id, ex)
        )


@router.post(
    "/{user_id}",
    response_model=UserIn_Pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def update_user(user_id: int, user: UserIn_Pydantic):
    try:
        await User.filter(id=user_id).update(**user.dict(exclude_unset=True))
        result = await User_Pydantic.from_queryset_single(User.get(id=user_id))
        return result.copy(include={'username', 'display_name'})
    except Exception as ex:
        raise HTTPException(
                status_code=404,
                detail="Update user with id {} failed: {}".format(user_id, ex))


@router.delete(
    "/{user_id}",
    response_model=Response,
    responses={404: {"model": HTTPNotFoundError}}
)
async def delete_user(user_id: int):
    deleted_count = await User.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")  # noqa: E501
    return Response(message=f"Deleted user {user_id}")
