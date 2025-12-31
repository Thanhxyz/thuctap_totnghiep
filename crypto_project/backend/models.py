from pydantic import BaseModel
from datetime import date

class ProjectInfo(BaseModel):
    project_id: int
    project_name: str
    total_supply: int
    launch_date: date
    website: str
    category: str

class TokenAllocation(BaseModel):
    allocation_id: int
    project_id: int
    category: str
    percentage: float
    cliff_months: int
    vesting_months: int
    initial_unlock: float
