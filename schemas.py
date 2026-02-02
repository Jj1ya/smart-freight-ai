# schemas.py
from pydantic import BaseModel, Field
from datetime import datetime

# 1. 기본 틀 (공통 속성)
class OrderBase(BaseModel):
    user_id: str
    country_code: str = Field(..., min_length=2, max_length=2, description="ISO 2자리 국가 코드 (예: KR, US)")
    weight: float = Field(..., gt=0, description="무게는 0보다 커야 합니다")

# 2. 데이터 받을 때 (Create)
# 사용자가 주문할 때는 위 3가지만 보내면 됩니다.
class OrderCreate(OrderBase):
    pass

# 3. 데이터 줄 때 (Response)
# 우리가 사용자에게 돌려줄 때는 ID, 가격, 생성시간을 포함합니다.
class OrderResponse(OrderBase):
    id: int
    price: float
    created_at: datetime

    class Config:
        from_attributes = True  # ORM 객체(DB 데이터)를 Pydantic 모델로 읽을 수 있게 함