from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.dependencies import get_current_user
from models.user import User
from db.database import get_db
from repository.user import UserRepository
from schemas.auth import (LoginRequest,TokenResponse,UserCreate,UserResponse, RefreshRequest)
from services.auth import (AuthService,InvalidCredentialsError,UserAlreadyExistsError, InvalidRefreshTokenError)
from fastapi.security import OAuth2PasswordRequestForm
from schemas.auth import OAuth2TokenResponse
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

# Это настоящий login нашего API: Это наш основной API login. Swagger после выполнения /auth/login не говорит:  «Ага, получил access_token — теперь автоматически считаю пользователя авторизованным». Он просто показывает тебе JSON-ответ. И GET /auth/me после этого получает 401, если ты отдельно не передал токен. (через отдельную форму с Authorize)
@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    try:
        _, access_token, refresh_token = (
            await auth_service.authenticate_user(email=str(login_data.email), password=login_data.password))

    except InvalidCredentialsError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error),headers={"WWW-Authenticate": "Bearer"})

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


# получить новый access_token по refresh_token
@router.post("/refresh", response_model=TokenResponse) # Ответ этого endpoint должен соответствовать схеме TokenResponse
async def refresh(refresh_data: RefreshRequest, auth_service: AuthService = Depends(get_auth_service)):
    try:
        access_token, refresh_token = await auth_service.refresh_tokens(refresh_data.refresh_token)
        # «У объекта auth_service вызови функцию refresh_tokens() и передай ей refresh token, который лежит внутри объекта refresh_data.»
    except InvalidRefreshTokenError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error), headers={"WWW-Authenticate": "Bearer"})
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)



@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# технический endpoint который нужен только для Swagger OAuth2 формы нужен только потому, что мы хотим, чтобы Swagger Authorize умел сам получить и сохранить токен.
# МЫ НЕ ДОЛЖНЫ вручную ходить на POST /auth/token. А для этого есть ккнопка 🔒 Authorize где ты ты вводишь email + пароль ->> Swagger сам вызывает: POST /auth/token ->> получает access_token ->> Swagger сохраняет access_token ->> ты вызываешь защищённые маршруты GET /auth/me ->> Swagger сам добавляет: Authorization: Bearer <access_token> ->> get_current_user() ->> проверить access_token и вернуть текущего пользователя и разрешить доступ ->> 200 OK
@router.post("/token", response_model=OAuth2TokenResponse)
async def token(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(get_auth_service)):
    try:
        _, access_token, _ = await auth_service.authenticate_user(email=form_data.username, password=form_data.password)
    except InvalidCredentialsError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error), headers={"WWW-Authenticate": "Bearer"})
    return OAuth2TokenResponse(access_token=access_token)