from pydantic import BaseModel
from typing import Optional

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    class Config:
        from_attributes = True  # Đổi từ orm_mode thành from_attributes

class AllocationBase(BaseModel):
    project_id: int
    amount: float

class AllocationCreate(AllocationBase):
    pass

class Allocation(AllocationBase):
    id: int
    class Config:
        from_attributes = True  # Đổi từ orm_mode thành from_attributes

class VestingScheduleBase(BaseModel):
    allocation_id: int
    unlock_date: str
    amount: float

class VestingScheduleCreate(VestingScheduleBase):
    pass

class VestingSchedule(VestingScheduleBase):
    id: int
    class Config:
        from_attributes = True  # Đổi từ orm_mode thành from_attributes
