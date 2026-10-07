from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.dependencies import get_current_user
from models.user import User
from db.database import get_db
from repository.user import UserRepository
from schemas.auth import (LoginRequest,TokenResponse,UserCreate,UserResponse)
from services.auth import (AuthService,InvalidCredentialsError,UserAlreadyExistsError)
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    user_repository = UserRepository(db)
    return AuthService(user_repository)


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    try:
        user = await auth_service.register_user(user_data)

    except UserAlreadyExistsError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))
    return user


@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    try:
        _, access_token, refresh_token = (
            await auth_service.authenticate_user(email=str(login_data.email), password=login_data.password))

    except InvalidCredentialsError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error),headers={"WWW-Authenticate": "Bearer"})

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/token", response_model=TokenResponse)
async def token(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(get_auth_service)):
    try:
        _, access_token, refresh_token = await auth_service.authenticate_user(email=form_data.username, password=form_data.password)
    except InvalidCredentialsError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error), headers={"WWW-Authenticate": "Bearer"})
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)