from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load biến môi trường từ .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Tạo engine async
engine = create_async_engine(DATABASE_URL, echo=True)

# Tạo session factory
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Khai báo Base cho ORM
Base = declarative_base()
