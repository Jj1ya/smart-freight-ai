# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

# 우리가 만든 파일들 불러오기 (Import)
import models, schemas
from database import SessionLocal, engine

# 1. DB 테이블 생성 (models.py의 내용을 보고 자동으로 만듦)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 2. CORS 설정 (프론트엔드 연동용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 곳에서 접속 허용 (보안상 실무에선 프론트엔드 주소만 적어야 함)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. DB 세션 관리자 (Dependency)
# 한 번 쓰고 나면 문(Connection)을 꼭 닫아주는 역할
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API 라우터 (여기가 핵심!) ---

# [POST] 주문 생성 (검증 로직 포함)
# response_model=schemas.OrderResponse : 응답할 때 이 양식으로 바꿔서 줘라!
@app.post("/orders", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # 1. 비즈니스 로직 (가격 계산)
    # 1kg당 $4.5 (하드코딩 대신 나중에 설정으로 뺄 수 있음)
    calculated_price = order.weight * 4.5
    
    # 2. DB 모델 생성 (schemas -> models 변환)
    db_order = models.Order(
        user_id=order.user_id,
        country_code=order.country_code,
        weight=order.weight,
        price=calculated_price
    )
    
    # 3. 저장 및 확정
    db.add(db_order)
    db.commit()
    db.refresh(db_order) # DB에서 생성된 ID, 시간 등을 다시 받아옴
    
    return db_order

# [GET] 주문 목록 조회 (새로 추가된 기능!)
# 리스트 형태로 반환 (List[schemas.OrderResponse])
@app.get("/orders", response_model=list[schemas.OrderResponse])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = db.query(models.Order).offset(skip).limit(limit).all()
    return orders