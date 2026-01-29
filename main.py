# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from database.user_dao import UserDAO  # ✅ Week 3의 유산인 DAO를 가져옵니다
from database.shipment_dao import ShipmentDAO
from database.connector import get_connection
from core.calculator import ShippingCalculator

app = FastAPI()

# 1. 기본 접속 (Home)
@app.get("/")
def read_root():
    return {"message": "Welcome to Smart Freight AI Server", "status": "online"}

# 2. 헬스 체크
@app.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}

# 3. ✅ [New] 전체 유저 조회 API
@app.get("/users")
def get_all_users():
    """
    DB에 저장된 모든 유저 목록을 가져옵니다.
    """
    dao = UserDAO()
    users = dao.get_all_users()
    return {"count": len(users), "users": users}

# 4. ✅ [New] 특정 유저 조회 API (경로 파라미터)
@app.get("/users/{user_id}")
def get_user(user_id: int):
    """
    특정 ID를 가진 유저 한 명을 조회합니다.
    """
    dao = UserDAO()
    user = dao.get_user_by_id(user_id)
    if user:
        return user
    else:
        return {"error": "User not found"}


# ✅ [New] 데이터 검증을 위한 설계도 (Schema)
class ShipmentRequest(BaseModel):
    user_id: int
    origin: str
    destination: str
    weight: float

# ✅ [New] 배송 주문 생성 API (POST)
@app.post("/shipments")
def create_shipment(req: ShipmentRequest):
    """
    주문 접수 -> 배송비 계산 -> 결제 -> 저장 (All-in-One Transaction)
    """
    # 1. 도구 준비
    calculator = ShippingCalculator()
    user_dao = UserDAO()
    ship_dao = ShipmentDAO()
    
    # 2. 트랜잭션 시작 (안전벨트 착용)
    conn = get_connection()
    
    try:
        # A. 배송비 계산
        cost = calculator.calculate_cost(req.weight, 'DHL')
        
        # B. 결제 진행
        user_dao.update_credits(req.user_id, -cost, conn=conn)
        
        # C. 주문 저장
        new_id = ship_dao.create_shipment(
            req.user_id, req.origin, req.destination, req.weight, 
            cost=cost, # ✅ 이 부분이 핵심입니다!
            conn=conn
        )
        
        # D. 커밋
        conn.commit()
        
        # ✅ 응답도 이렇게 풍성하게 바뀌어야 합니다.
        return {
            "message": "주문 및 결제 완료",
            "shipment_id": new_id,
            "cost": cost,
            "status": "PAID"
        }
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()