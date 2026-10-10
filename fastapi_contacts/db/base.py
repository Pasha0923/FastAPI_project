# Создаём SQLAlchemy Base (фундамент всех наших моделей.)
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


# {
#   "email": "test@example.com",
#   "password": "password123"
# }

	
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzkxMzc3OTM5LCJ0eXBlIjoiYWNjZXNzIn0.iV4rgNKtwrjHvhUQ1jfIahz2poBuDlXuy1Ei5maiD7Q",
#   "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzkxOTgwOTM5LCJ0eXBlIjoicmVmcmVzaCJ9.zIWhoCkfPS6eHEHxeUP7LHSI4rx-PZAFrs35tLDen7A",
#   "token_type": "bearer"
# }