from pydantic import BaseModel
from typing import List, Optional

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    class Config:
        orm_mode = True

class AllocationBase(BaseModel):
    project_id: int
    amount: float

class AllocationCreate(AllocationBase):
    pass

class Allocation(AllocationBase):
    id: int
    class Config:
        orm_mode = True

class VestingScheduleBase(BaseModel):
    allocation_id: int
    unlock_date: str
    amount: float

class VestingScheduleCreate(VestingScheduleBase):
    pass

class VestingSchedule(VestingScheduleBase):
    id: int
    class Config:
        orm_mode = True
