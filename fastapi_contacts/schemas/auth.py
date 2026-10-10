

from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

# UserCreate — данные, которые клиент отправляет при регистрации:  POST /auth/signup
class UserCreate(BaseModel): 
    email: EmailStr
    password: str

# UserResponse — базовый ответ (поля) которые возвращаем коиенту
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# # возвращаем ответ клиенту после регистрации
# class SignupResponse(BaseModel):
#     user: UserResponse
#     detail: str = "User successfully created"


# LoginRequest — данные, которые клиент отправляет при логине:  POST /auth/login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# RefreshRequest - клиент отправляет refresh_token по маршруту POST /auth/refresh  для получения нового access_token (сам refresh_token ранее получен был ещё при аутентификации по маршруту auth/login) 
class RefreshRequest(BaseModel):
    refresh_token: str

# возвращаем клиенту после auth/login/
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class OAuth2TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"