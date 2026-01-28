# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from database.user_dao import UserDAO  # ✅ Week 3의 유산인 DAO를 가져옵니다
from database.shipment_dao import ShipmentDAO

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
    새로운 배송 주문을 생성합니다.
    """
    dao = ShipmentDAO()
    # Pydantic(req)이 검증한 데이터를 꺼내서 DAO에게 전달
    new_id = dao.create_shipment(req.user_id, req.origin, req.destination, req.weight)
    
    return {"message": "주문 접수 완료", "shipment_id": new_id}