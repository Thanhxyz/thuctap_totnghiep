from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import os

# Kết nối đến Neon PostgreSQL
DATABASE_URL = "postgresql://neondb_owner:npg_puzIOU3Y5VET@ep-bitter-cloud-a8dztndt-pooler.eastus2.azure.neon.tech/neondb"

app = FastAPI()

# Cấu hình CORS để tránh lỗi khi fetch API từ frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả domain truy cập (nếu cần bảo mật, hãy giới hạn)
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả phương thức HTTP (GET, POST, ...)
    allow_headers=["*"],  # Cho phép tất cả headers
)

# Kết nối database
def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

# Định nghĩa model dữ liệu đầu vào
class Project(BaseModel):
    project_name: str
    total_supply: int
    launch_date: str
    category: str
    website: str

class TokenAllocation(BaseModel):
    project_id: int
    percentage: float
    cliff_months: int
    vesting_months: int
    initial_unlock: float

# API lấy danh sách dự án
@app.get("/projects")
def get_projects():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT project_id, project_name FROM project_info")
    projects = cur.fetchall()
    conn.close()
    return [{"id": row[0], "name": row[1]} for row in projects]

# API lấy thông tin chi tiết của một dự án
@app.get("/project_info/{project_id}")
def get_project_info(project_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT project_name, total_supply, launch_date, category, website 
        FROM project_info 
        WHERE project_id = %s
    """, (project_id,))
    project = cur.fetchone()
    conn.close()

    if project:
        return {
            "name": project[0],
            "total_supply": project[1],
            "launch_date": project[2],
            "category": project[3],
            "website": project[4]
        }
    return {"error": "Project not found"}

# API thêm dự án mới
@app.post("/add_project")
def add_project(project: Project):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO project_info (project_name, total_supply, launch_date, category, website)
        VALUES (%s, %s, %s, %s, %s) RETURNING project_id
    """, (project.project_name, project.total_supply, project.launch_date, project.category, project.website))
    project_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return {"message": "Project added successfully", "project_id": project_id}

# API thêm token allocation
@app.post("/add_allocation")
def add_allocation(allocation: TokenAllocation):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO token_allocation (project_id, percentage, cliff_months, vesting_months, initial_unlock)
        VALUES (%s, %s, %s, %s, %s) RETURNING allocation_id
    """, (allocation.project_id, allocation.percentage, allocation.cliff_months, allocation.vesting_months, allocation.initial_unlock))
    allocation_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return {"message": "Token allocation added successfully", "allocation_id": allocation_id}

# API tính toán vesting schedule và lưu vào database
@app.post("/calculate_vesting/{allocation_id}")
def calculate_vesting(allocation_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Lấy thông tin token allocation
    cur.execute("""
        SELECT project_id, percentage, cliff_months, vesting_months, initial_unlock 
        FROM token_allocation 
        WHERE allocation_id = %s
    """, (allocation_id,))
    allocation = cur.fetchone()
    
    if not allocation:
        conn.close()
        return {"error": "Allocation not found"}
    
    project_id, percentage, cliff_months, vesting_months, initial_unlock = allocation
    
    # Lấy tổng cung token của dự án
    cur.execute("""
        SELECT total_supply FROM project_info WHERE project_id = %s
    """, (project_id,))
    total_supply = cur.fetchone()[0]

    if not total_supply:
        conn.close()
        return {"error": "Project not found"}

    # Tính tổng số token theo phần trăm phân bổ
    total_tokens = (total_supply * percentage) / 100

    # Tính số token được unlock ngay tại TGE
    unlocked_tge = (total_tokens * initial_unlock) / 100

    # Xóa dữ liệu vesting cũ trước khi ghi mới
    cur.execute("DELETE FROM vesting_schedule WHERE allocation_id = %s", (allocation_id,))
    conn.commit()

    # Chèn token được unlock ngay TGE vào bảng vesting_schedule
    cur.execute("""
        INSERT INTO vesting_schedule (allocation_id, month_number, unlock_date, unlocked_tokens)
        VALUES (%s, %s, %s, %s)
    """, (allocation_id, 0, '2024-03-01', unlocked_tge))

    # Phân phối vesting theo từng tháng sau cliff period
    monthly_unlock = (total_tokens - unlocked_tge) / vesting_months

    for month in range(1, vesting_months + 1):
        unlock_month = f"2024-{month+3:02d}-01"
        cur.execute("""
            INSERT INTO vesting_schedule (allocation_id, month_number, unlock_date, unlocked_tokens)
            VALUES (%s, %s, %s, %s)
        """, (allocation_id, month, unlock_month, monthly_unlock))

    conn.commit()
    conn.close()
    
    return {"message": "Vesting schedule calculated successfully"}

# API lấy dữ liệu vesting theo project_id
@app.get("/vesting/{project_id}")
def get_vesting_data(project_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT vs.month_number, SUM(vs.unlocked_tokens)
        FROM vesting_schedule vs
        JOIN token_allocation ta ON vs.allocation_id = ta.allocation_id
        WHERE ta.project_id = %s
        GROUP BY vs.month_number
        ORDER BY vs.month_number
    """, (project_id,))
    
    data = cur.fetchall()
    conn.close()
    
    return [{"month": row[0], "tokens": row[1]} for row in data]

@app.get("/")
def home():
    return {"message": "Welcome to Tokenomics API! Use /projects or /vesting/{project_id}"}
