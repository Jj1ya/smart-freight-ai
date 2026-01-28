# main.py
from database.user_dao import UserDAO
from database.shipment_dao import ShipmentDAO

def main():
    user_dao = UserDAO()
    shipment_dao = ShipmentDAO()

    print("--- 🔍 1. 운송장을 조회할 유저 찾기 ---")
    # 예시로 ID가 1번인 유저를 가져옵니다.
    # (실제로는 로그인한 유저 ID를 쓰겠지만, 지금은 테스트니까요)
    all_users = user_dao.get_all_users(limit=1)
    if not all_users:
        print("❌ 유저가 없습니다. Seeding을 먼저 해주세요.")
        return

    target_user = all_users[0]
    user_id = target_user['id']
    print(f"👤 대상 유저: {target_user['username']} (ID: {user_id})")

    print(f"\n--- 📦 2. {target_user['username']}님의 배송 내역 조회 ---")
    my_shipments = shipment_dao.get_shipments_by_user(user_id)
    
    if my_shipments:
        print(f"총 {len(my_shipments)}건의 주문이 발견되었습니다.\n")
        print(f"{'주문번호':<10} {'출발':<5} {'도착':<5} {'상태':<12} {'무게(kg)':<10}")
        print("-" * 50)
        
        for s in my_shipments:
            print(f"{s['id']:<10} {s['origin']:<5} {s['destination']:<5} {s['status']:<12} {s['weight']:<10}")
    else:
        print("📭 아직 주문 내역이 없습니다.")

    # (옵션) 새 주문 넣어보기 테스트
    # print("\n--- 3. 신규 주문 생성 테스트 ---")
    # new_shipment = shipment_dao.create_shipment(user_id, 'KR', 'US', 5.5)
    # print(f"✅ 새 주문 접수 완료: ID {new_shipment['id']}")

if __name__ == "__main__":
    main()