# 数据库配置（使用兼容的驱动）
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 使用pg8000作为跨平台PostgreSQL驱动
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+pg8000://user:password@localhost:5432/sqnb")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
