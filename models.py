# models.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base  # 방금 만든 database.py에서 Base를 가져옴!

class Order(Base):
    __tablename__ = "freight_orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    country_code = Column(String(2)) # ISO 2자리 코드 제한
    weight = Column(Float)
    price = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())