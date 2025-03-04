from fastapi import FastAPI
from routes import projects, allocations, vesting
from backend.database import engine, Base

app = FastAPI()

# Đăng ký các route
app.include_router(projects.router, prefix="/api")
app.include_router(allocations.router, prefix="/api")
app.include_router(vesting.router, prefix="/api")

@app.get("/")
def home():
    return {"message": "Welcome to Vesting API"}

# Khởi tạo bảng database
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

import asyncio
asyncio.run(init_db())
