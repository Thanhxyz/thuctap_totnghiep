from fastapi import FastAPI
from routes import projects, allocations, vesting
from backend.database import init_db

app = FastAPI()

# Đăng ký các route
app.include_router(projects.router, prefix="/api")
app.include_router(allocations.router, prefix="/api")
app.include_router(vesting.router, prefix="/api")

@app.get("/")
def home():
    return {"message": "Welcome to Vesting API"}

# Khởi tạo database khi ứng dụng khởi động
@app.on_event("startup")
async def startup_event():
    await init_db()  # Không dùng asyncio.run(init_db()) vì FastAPI đã có event loop riêng
