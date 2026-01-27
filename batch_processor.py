# batch_processor.py
from database.connector import get_connection
from database.user_dao import UserDAO
from database.shipment_dao import ShipmentDAO
from core.calculator import ShippingCalculator

def run_batch_process():
    print("🏭 배치 프로세서 가동 시작...")
    
    # 1. 필요한 도구들 준비 (인스턴스 생성)
    user_dao = UserDAO()
    shipment_dao = ShipmentDAO()
    calculator = ShippingCalculator()
    
    # 2. 처리해야 할 주문 목록 가져오기 (배송비 0원인 것들)
    pending_list = shipment_dao.get_pending_shipments()
    print(f"📦 처리 대기 중인 주문: {len(pending_list)}건")
    
    success_count = 0
    fail_count = 0

    # 3. 하나씩 꺼내서 처리 (Loop)
    for shipment in pending_list:
        s_id = shipment['id']
        u_id = shipment['user_id']
        weight = shipment['weight']
        
        # --- 트랜잭션 시작 (주문 1건당 1개의 트랜잭션) ---
        conn = get_connection()
        try:
            print(f"   🔄 Processing Order #{s_id} (User {u_id}, {weight}kg)... ", end="")
            
            # A. 배송비 계산 (Week 2의 두뇌 사용)
            # (운송사는 예시로 'DHL' 고정)
            cost = calculator.calculate_cost(weight, 'DHL')
            
            # B. 고객 지갑에서 돈 차감 (Day 4의 기능)
            user_dao.update_credits(u_id, -cost, conn=conn)
            
            # C. 배송비 정보 저장 & 상태 업데이트
            shipment_dao.update_cost(s_id, cost, conn=conn)
            
            # D. 모두 성공하면 커밋
            conn.commit()
            print(f"✅ 완료! (-${cost})")
            success_count += 1
            
        except ValueError as ve:
            # 잔액 부족 등의 비즈니스 로직 에러
            conn.rollback()
            print(f"⚠️ 실패 (계산 오류): {ve}")
            fail_count += 1
        except Exception as e:
            # 시스템 에러
            conn.rollback()
            print(f"❌ 실패 (시스템 오류): {e}")
            fail_count += 1
        finally:
            conn.close()
            
    print("-" * 30)
    print(f"🎉 배치 작업 종료. 성공: {success_count}건, 실패: {fail_count}건")

if __name__ == "__main__":
    run_batch_process()