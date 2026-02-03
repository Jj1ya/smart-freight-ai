# schemas.py
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

# 1. 공통 속성 및 검증 로직
class OrderBase(BaseModel):
    user_id: str
    
    # 예전에는 길이만 체크했지만, 이제는 설명(description)과 예시(example)도 추가합니다.
    country_code: str = Field(..., description="ISO 2자리 국가 코드 (KR, US, JP, CN)")
    weight: float = Field(..., gt=0, description="화물 무게 (kg)")

    # [New] Pydantic Validator: 복잡한 검증 로직 추가
    @field_validator('country_code')
    def validate_country(cls, v):
        # 허용된 국가 리스트 (실무에선 DB나 Config에서 가져오기도 함)
        allowed_countries = ['KR', 'US', 'JP', 'CN']
        upper_code = v.upper() # 대문자로 변환
        if upper_code not in allowed_countries:
            raise ValueError(f"지원하지 않는 국가입니다: {v}. (허용: {allowed_countries})")
        return upper_code

    @field_validator('weight')
    def validate_weight(cls, v):
        if v > 1000:
            raise ValueError("화물이 너무 무겁습니다. (최대 1000kg)")
        return v

# 2. 데이터 생성용 (Create)
class OrderCreate(OrderBase):
    pass

# 3. 응답용 (Response)
class OrderResponse(OrderBase):
    id: int
    price: float
    created_at: datetime

    class Config:
        from_attributes = True