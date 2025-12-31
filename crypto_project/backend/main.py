from fastapi import FastAPI, Depends
from backend.database import connect_to_db
from backend.crud import add_project, add_token_allocation
from backend.vesting import calculate_vesting_schedule
from backend.models import ProjectInfo, TokenAllocation

app = FastAPI()

@app.on_event("startup")
async def startup():
    app.state.db = await connect_to_db()

@app.post("/projects/")
async def create_project(project: ProjectInfo):
    await add_project(app.state.db, project)
    return {"message": "Dự án đã được thêm thành công"}

@app.post("/allocations/")
async def create_allocation(allocation: TokenAllocation):
    await add_token_allocation(app.state.db, allocation)
    await calculate_vesting_schedule(app.state.db, allocation.project_id)
    return {"message": "Phân bổ token đã được thêm và tính toán vesting"}
