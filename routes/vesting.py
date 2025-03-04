from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import SessionLocal
from backend import crud, schemas

router = APIRouter()

async def get_db():
    async with SessionLocal() as db:
        yield db

@router.post("/vesting/", response_model=schemas.VestingSchedule)
async def create_vesting(vesting: schemas.VestingScheduleCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_vesting_schedule(db=db, vesting=vesting)
