# Создаём SQLAlchemy Base (фундамент всех наших моделей.)
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


# {
#   "email": "test@example.com",
#   "password": "password123"
# }