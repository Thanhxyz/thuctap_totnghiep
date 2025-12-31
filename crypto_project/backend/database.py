import asyncpg
import os

# Thay vì DATABASE_URL, bạn đang dùng DB_URL
DB_URL = "postgresql://neondb_owner:npg_puzIOU3Y5VET@ep-bitter-cloud-a8dztndt-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

async def connect_to_db():
    if not DB_URL:
        raise ValueError("Database URL is not set")
    
    try:
        return await asyncpg.create_pool(DB_URL)
    except Exception as e:
        print(f"Database connection error: {e}")
        raise
