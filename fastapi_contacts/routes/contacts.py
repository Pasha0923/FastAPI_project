from fastapi import APIRouter, Depends, status , HTTPException , Response
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_current_user
from db.database import get_db
from models.contact import Contact
from models.user import User
from repository.contact import ContactRepository
from schemas.contact import ContactCreate, ContactResponse , ContactUpdate


router = APIRouter(prefix="/contacts", tags=["Contacts"])


def get_contact_repository(db: AsyncSession = Depends(get_db)) -> ContactRepository:
    return ContactRepository(db)


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(contact_data: ContactCreate, current_user: User = Depends(get_current_user), repository: ContactRepository = Depends(get_contact_repository)):
    contact = Contact(**contact_data.model_dump(), user_id=current_user.id)
    return await repository.create(contact)

@router.get("/", response_model=list[ContactResponse])
async def get_contacts(current_user: User = Depends(get_current_user), repository: ContactRepository = Depends(get_contact_repository)):
    return await repository.get_all_by_user(current_user.id)


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int, current_user: User = Depends(get_current_user), repository: ContactRepository = Depends(get_contact_repository)):
    contact = await repository.get_by_id_for_user(contact_id=contact_id, user_id=current_user.id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.patch("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, contact_data: ContactUpdate, current_user: User = Depends(get_current_user), repository: ContactRepository = Depends(get_contact_repository)):
    update_data = contact_data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least one field must be provided")
    contact = await repository.update_for_user(contact_id=contact_id, user_id=current_user.id, update_data=update_data)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, current_user: User = Depends(get_current_user), repository: ContactRepository = Depends(get_contact_repository)) -> Response:
    deleted = await repository.delete_for_user(contact_id=contact_id, user_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)