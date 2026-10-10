from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from db.database  import get_db
from routes.auth import router as auth_router
from routes.contacts import router as contacts_router


if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(title="Contacts API", description="REST API for managing contacts", version="1.0.0", swagger_ui_parameters={"persistAuthorization": True})


@app.get("/")
async def root():
    return {"message": "Contacts API is running"}


@app.get("/health/db")
async def database_health(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {"database": result.scalar()}

app.include_router(auth_router)
app.include_router(contacts_router)