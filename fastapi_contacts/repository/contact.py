import calendar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.contact import Contact

from datetime import date, timedelta
from sqlalchemy import extract, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

class ContactRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, contact: Contact) -> Contact:
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    # async def get_all_by_user(self, user_id: int) -> list[Contact]:
    #     # «Выбери контакты из таблицы contacts, но только те, у которых user_id равен ID текущего пользователя».
    #     result = await self.db.execute(select(Contact).where(Contact.user_id == user_id))
    #     return list(result.scalars().all())
    async def get_all_by_user(self, user_id: int, first_name: str | None = None, last_name: str | None = None, email: str | None = None) -> list[Contact]:
        query = select(Contact).where(Contact.user_id == user_id)
        if first_name and first_name.strip():
            query = query.where(Contact.first_name.ilike(f"%{first_name.strip()}%"))
        if last_name and last_name.strip():
            query = query.where(Contact.last_name.ilike(f"%{last_name.strip()}%"))
        if email and email.strip():
            query = query.where(Contact.email.ilike(f"%{email.strip()}%"))
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_by_id_for_user(self, contact_id: int, user_id: int) -> Contact | None:
        result = await self.db.execute(select(Contact).where(Contact.id == contact_id, Contact.user_id == user_id))
        return result.scalar_one_or_none()


    async def update_for_user(self, contact_id: int, user_id: int, update_data: dict) -> Contact | None:
        result = await self.db.execute(select(Contact).where(Contact.id == contact_id, Contact.user_id == user_id))
        contact = result.scalar_one_or_none()
        if contact is None:
            return None
        for field, value in update_data.items():
            setattr(contact, field, value)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def delete_for_user(self, contact_id: int, user_id: int) -> bool:
        result = await self.db.execute(select(Contact).where(Contact.id == contact_id, Contact.user_id == user_id))
        contact = result.scalar_one_or_none()
        if contact is None:
            return False
        await self.db.delete(contact)
        await self.db.commit()
        return True

    async def get_upcoming_birthdays(self, user_id: int, days: int = 7) -> list[Contact]:
        today = date.today()
        end_date = today + timedelta(days=days)

        birthday_key = extract("month", Contact.birthday) * 100 + extract("day", Contact.birthday)
        today_key = today.month * 100 + today.day
        end_key = end_date.month * 100 + end_date.day

        query = select(Contact).where(Contact.user_id == user_id)

        if end_date.year == today.year:
            query = query.where(birthday_key >= today_key, birthday_key <= end_key)
        else:
            query = query.where(or_(birthday_key >= today_key, birthday_key <= end_key))

        if not calendar.isleap(today.year):
            query = query.where(or_(extract("month", Contact.birthday) != 2, extract("day", Contact.birthday) != 29))

        result = await self.db.execute(query)
        return list(result.scalars().all())