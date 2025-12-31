import asyncpg
from backend.models import ProjectInfo, TokenAllocation

async def add_project(db: asyncpg.Pool, project: ProjectInfo):
    query = """
    INSERT INTO project_info (project_id, project_name, total_supply, launch_date, website, category)
    VALUES ($1, $2, $3, $4, $5, $6)
    """
    await db.execute(query, project.project_id, project.project_name, project.total_supply,
                     project.launch_date, project.website, project.category)

async def add_token_allocation(db: asyncpg.Pool, allocation: TokenAllocation):
    query = """
    INSERT INTO token_allocation (allocation_id, project_id, category, percentage, cliff_months, vesting_months, initial_unlock)
    VALUES ($1, $2, $3, $4, $5, $6, $7)
    """
    await db.execute(query, allocation.allocation_id, allocation.project_id, allocation.category,
                     allocation.percentage, allocation.cliff_months, allocation.vesting_months,
                     allocation.initial_unlock)
