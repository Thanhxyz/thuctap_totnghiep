from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend import models, schemas

async def create_project(db: AsyncSession, project: schemas.ProjectCreate):
    new_project = models.Project(name=project.name, description=project.description)
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return new_project

async def create_allocation(db: AsyncSession, allocation: schemas.AllocationCreate):
    new_allocation = models.Allocation(project_id=allocation.project_id, amount=allocation.amount)
    db.add(new_allocation)
    await db.commit()
    await db.refresh(new_allocation)
    return new_allocation

async def create_vesting_schedule(db: AsyncSession, vesting: schemas.VestingScheduleCreate):
    new_vesting = models.VestingSchedule(
        allocation_id=vesting.allocation_id,
        unlock_date=vesting.unlock_date,
        amount=vesting.amount
    )
    db.add(new_vesting)
    await db.commit()
    await db.refresh(new_vesting)
    return new_vesting
