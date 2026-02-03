# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError # DB 에러 잡기용

import models, schemas
from database import SessionLocal, engine

# DB 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API Endpoints ---

# [POST] 주문 생성 (안전장치 추가됨)
@app.post("/orders", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    try:
        # 1. 비즈니스 로직
        calculated_price = order.weight * 4.5
        
        # 2. 모델 생성
        db_order = models.Order(
            user_id=order.user_id,
            country_code=order.country_code, # schemas에서 이미 검증됨 (자동 대문자 변환)
            weight=order.weight,
            price=calculated_price
        )
        
        # 3. DB 저장 시도
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order

    except SQLAlchemyError as e:
        db.rollback() # [중요] 에러 나면 DB 되돌리기!
        print(f"Database Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="데이터베이스 저장 중 오류가 발생했습니다."
        )
    except Exception as e:
        print(f"Unknown Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="알 수 없는 서버 오류가 발생했습니다."
        )

# [GET] 주문 목록 조회
@app.get("/orders", response_model=list[schemas.OrderResponse])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = db.query(models.Order).order_by(models.Order.id.desc()).offset(skip).limit(limit).all()
    return orders

# [GET] 특정 주문 조회 (새로 추가됨: 404 에러 처리 실습용)
@app.get("/orders/{order_id}", response_model=schemas.OrderResponse)
def read_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    
    if order is None:
        # 없는 주문을 찾으면 404 에러를 '직접' 발생시킴
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"주문 ID {order_id}번을 찾을 수 없습니다."
        )
    
    return order