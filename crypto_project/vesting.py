import asyncpg
from datetime import datetime, timedelta

# Kết nối database
DB_URL = "postgresql://neondb_owner:npg_puzIOU3Y5VET@ep-bitter-cloud-a8dztndt-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

async def connect_db():
    """ Kết nối database """
    return await asyncpg.create_pool(DB_URL)

async def fetch_projects():
    """ Truy vấn dữ liệu từ project_info & token_allocation """
    pool = await connect_db()
    async with pool.acquire() as conn:
        query = """
        SELECT pi.project_id, pi.total_supply, pi.launch_date, 
               ta.allocation_id, ta.category, ta.percentage, 
               ta.cliff_months, ta.vesting_months, ta.initial_unlock,
               ta.unlock_schedule
        FROM project_info pi
        JOIN token_allocation ta ON pi.project_id = ta.project_id;
        """
        return await conn.fetch(query)

async def calculate_vesting():
    """ Tính toán lịch vesting schedule """
    projects = await fetch_projects()
    vesting_data = []

    for project in projects:
        project_id = project["project_id"]
        total_supply = project["total_supply"]
        allocation_id = project["allocation_id"]
        percentage = project["percentage"]
        cliff_months = project["cliff_months"]
        vesting_months = project["vesting_months"]
        initial_unlock = project["initial_unlock"]
        unlock_schedule = project["unlock_schedule"]

        # Kiểm tra launch_date hợp lệ
        launch_date_str = project["launch_date"]
        if launch_date_str is None:
            print(f"⚠️ Warning: Project {project_id} has no launch_date. Skipping...")
            continue

        launch_date = datetime.strptime(launch_date_str, "%Y-%m-%d").date()

        # Tính tổng số token phân bổ
        total_tokens = (total_supply * percentage) / 100

        # Initial Unlock (Tháng 0)
        unlocked_tge = (total_tokens * initial_unlock) / 100
        vesting_data.append((allocation_id, 0, unlocked_tge))

        # Ngày bắt đầu vesting sau cliff
        vesting_start_date = launch_date + timedelta(days=cliff_months * 30)

        # Phân bổ vesting theo kiểu unlock_schedule
        if vesting_months > 0:
            if unlock_schedule == "linear":
                tokens_per_month = (total_tokens - unlocked_tge) / vesting_months
                for month in range(1, vesting_months + 1):
                    vesting_data.append((allocation_id, month, tokens_per_month))

            elif unlock_schedule == "quarterly":
                tokens_per_quarter = (total_tokens - unlocked_tge) / (vesting_months / 3)
                for quarter in range(1, int(vesting_months / 3) + 1):
                    month_number = quarter * 3
                    vesting_data.append((allocation_id, month_number, tokens_per_quarter))

            elif unlock_schedule == "monthly":
                tokens_per_month = (total_tokens - unlocked_tge) / vesting_months
                for month in range(1, vesting_months + 1):
                    vesting_data.append((allocation_id, month, tokens_per_month))

    return vesting_data

async def insert_vesting_schedule():
    """ Lưu lịch vesting vào database """
    vesting_records = await calculate_vesting()
    pool = await connect_db()
    async with pool.acquire() as conn:
        query = """
        INSERT INTO vesting_schedule (allocation_id, month_number, unlocked_tokens)
        VALUES ($1, $2, $3)
        """
        await conn.executemany(query, vesting_records)
    print("✅ Dữ liệu vesting đã được lưu thành công!")

# Chạy chương trình
if __name__ == "__main__":
    import asyncio
    asyncio.run(insert_vesting_schedule())
