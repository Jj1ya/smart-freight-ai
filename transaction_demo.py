# transaction_demo.py
from database.connector import get_connection
from database.user_dao import UserDAO
from database.shipment_dao import ShipmentDAO
import sys

def process_order_transaction(user_id, weight, make_error=False):
    conn = get_connection() # 1. 여기서 딱 한 번 연결을 맺습니다 (Session Start)
    
    user_dao = UserDAO()
    ship_dao = ShipmentDAO()
    
    print(f"\n🚀 트랜잭션 시작 (에러 모드: {make_error})")
    
    try:
        # 1. 결제 처리 (돈 차감) - $50
        print("   1️⃣  결제 진행 중... (-$50)")
        user_dao.update_credits(user_id, -50, conn=conn) # conn을 넘겨줍니다!

        # 2. 강제 에러 발생 (시뮬레이션)
        if make_error:
            print("   🚨 앗! 서버에 커피를 쏟았습니다. (에러 발생)")
            raise Exception("Artificial Server Error")

        # 3. 배송 주문 생성
        print("   2️⃣  주문 생성 중...")
        ship_dao.create_shipment(user_id, 'KR', 'US', weight, conn=conn) # conn을 넘겨줍니다!

        # 4. 모든게 성공하면 저장 (Commit)
        conn.commit()
        print("✅ [SUCCESS] 결제와 주문이 모두 완료되었습니다.")

    except Exception as e:
        # 5. 하나라도 실패하면 되감기 (Rollback)
        conn.rollback()
        print(f"❌ [FAILED] 트랜잭션 롤백됨! 원인: {e}")
        
    finally:
        conn.close() # 연결 종료

# --- 실행 부분 ---
if __name__ == "__main__":
    dao = UserDAO()
    target_user_id = 1
    
    # 1. 초기 잔액 확인
    before = dao.get_user_by_id(target_user_id)
    print(f"💰 초기 잔액: ${before['credits']}")
    
    # 2. 실패하는 주문 시도 (롤백 테스트)
    process_order_transaction(target_user_id, 5.0, make_error=True)
    
    # 3. 롤백 후 잔액 확인 (돈이 그대로여야 함!)
    after_fail = dao.get_user_by_id(target_user_id)
    print(f"💰 롤백 후 잔액: ${after_fail['credits']} (변동 없어야 정답)")
    
    # 4. 성공하는 주문 시도
    process_order_transaction(target_user_id, 5.0, make_error=False)
    
    # 5. 성공 후 잔액 확인 (돈이 줄어야 함)
    after_success = dao.get_user_by_id(target_user_id)
    print(f"💰 성공 후 잔액: ${after_success['credits']} ($50 차감 확인)")