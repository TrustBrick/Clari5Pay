# models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    # Phone numbers are stored as String, NOT Integer: a 10-digit number like
    # 9876543210 overflows PostgreSQL's 4-byte integer (max 2,147,483,647),
    # and storing as text also preserves leading zeros / country codes.
    phone_no = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
