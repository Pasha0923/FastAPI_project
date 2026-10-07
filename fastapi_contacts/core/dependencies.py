from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import decode_access_token, oauth2_scheme
from db.database import get_db
from models.user import User
from repository.user import UserRepository


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])

    except (ValueError, KeyError, TypeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})

    user_repository = UserRepository(db)
    user = await user_repository.get_by_id(user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found", headers={"WWW-Authenticate": "Bearer"})

    return user