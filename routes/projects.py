from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import SessionLocal
from backend import crud, schemas

router = APIRouter()

async def get_db():
    async with SessionLocal() as db:
        yield db

@router.post("/projects/", response_model=schemas.Project)
async def create_project(project: schemas.ProjectCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_project(db=db, project=project)
