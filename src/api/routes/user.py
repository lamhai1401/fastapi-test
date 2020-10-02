from fastapi import APIRouter, Depends
from typing import List
from fastapi import HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from src.models import User, UserIn_Pydantic, User_Pydantic, Response, UserInScheme
from src.auth.oauth2 import verify_token, oauth2_scheme, get_password_hash
from pydantic import BaseModel
from src.utils import errors

router = APIRouter()


#  async def get_current_user(token: str = Depends(oauth2_scheme))
@router.get(
    "/",
    response_model=List[UserInScheme],
)
async def get_users(token: str = Depends(oauth2_scheme)):
    await verify_token(token)
    try:
        users = await User_Pydantic.from_queryset(User.all())
        return [UserInScheme(**user.dict()) for user in users]
    except Exception as ex:
        raise errors.Error404(str(ex))


@router.post("/", response_model=User_Pydantic)
async def create_user(user: UserInScheme):
    if not user.password:
        raise errors.Error404("Missing password")
    user.password_hash = get_password_hash(user.password)
    pydantic = UserIn_Pydantic(**user.dict(exclude={'password'}, exclude_unset=True))
    user_obj = await User.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.get(
    "/{user_id}",
    response_model=UserInScheme,
    # responses={404: {"model": HTTPNotFoundError}}
)
async def get_user(user_id: int):
    try:
        user = await User_Pydantic.from_queryset_single(User.get(id=user_id))
        return UserInScheme(**user.dict())
    except Exception as ex:
        raise HTTPException(
            status_code=404,
            detail="User with id {} not found err: {}".format(user_id, ex)
        )


@router.post(
    "/{user_id}",
    response_model=UserIn_Pydantic,
    # responses={404: {"model": HTTPNotFoundError}}
)
async def update_user(user_id: int, user: UserIn_Pydantic):
    try:
        await User.filter(id=user_id).update(**user.dict(exclude_unset=True))
        result = await User_Pydantic.from_queryset_single(User.get(id=user_id))
        return result.copy(include={'username', 'display_name'})
    except Exception as ex:
        raise await errors.Error404("Update user with id {} failed: {}".format(user_id, ex))


@router.delete(
    "/{user_id}",
    response_model=Response,
    # responses={404: {"model": HTTPNotFoundError}}
)
async def delete_user(user_id: int):
    deleted_count = await User.filter(id=user_id).delete()
    if not deleted_count:
        raise await errors.Error404(f"User {user_id} not found")  # noqa: E501
    return Response(message=f"Deleted user {user_id}")
