from fastapi import HTTPException, status


async def Error401(msg: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=msg,
        headers={"WWW-Authenticate": "Bearer"},
    )


async def Error404(msg: str) -> HTTPException:
    return HTTPException(
        status_code=404,
        detail=msg
    )
