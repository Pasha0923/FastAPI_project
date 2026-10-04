from schemas.auth import UserCreate
from models.user import User
from repository.user import UserRepository
from core.security import hash_password, verify_password , create_access_token , create_refresh_token


class UserAlreadyExistsError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register_user(self, user_data: UserCreate) -> User: 
        # Проверяем, существует ли пользователь с таким email
        existing_user = await self.user_repository.get_by_email(str(user_data.email))

        if existing_user:
            raise UserAlreadyExistsError("User with this email already exists")

        # Хешируем пароль перед сохранением в БД
        hashed_password = hash_password(user_data.password)
        # Создаём SQLAlchemy-модель User
        user = User(email=str(user_data.email), hashed_password=hashed_password)
        return await self.user_repository.create(user)

    async def authenticate_user(self,email: str,password: str) -> tuple[User, str, str]:
        # Ищем пользователя в БД
        user = await self.user_repository.get_by_email(email)

        # Проверяем email и пароль
        if user is None or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Invalid email or password")
        
        # Данные, которые попадут в JWT
        token_data = {"sub": str(user.id)}

        # Создаём пару токенов
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        return user , access_token , refresh_token