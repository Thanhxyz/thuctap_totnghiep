from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import SessionLocal
from backend import crud, schemas

router = APIRouter()

async def get_db():
    async with SessionLocal() as db:
        yield db

@router.post("/allocations/", response_model=schemas.Allocation)
async def create_allocation(allocation: schemas.AllocationCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_allocation(db=db, allocation=allocation)
