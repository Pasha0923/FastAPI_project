from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from db.database  import get_db

if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

app = FastAPI(
    title="Contacts API",
    description="REST API for managing contacts",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {"message": "Contacts API is running"}


@app.get("/health/db")
async def database_health(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {"database": result.scalar()}