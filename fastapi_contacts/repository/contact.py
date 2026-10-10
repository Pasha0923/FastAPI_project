from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.contact import Contact


class ContactRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, contact: Contact) -> Contact:
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def get_all_by_user(self, user_id: int) -> list[Contact]:
        # «Выбери контакты из таблицы contacts, но только те, у которых user_id равен ID текущего пользователя».
        result = await self.db.execute(select(Contact).where(Contact.user_id == user_id))
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