from database.connector import get_connection

def fetch_order_summary():
    conn = None
    try:
        # 1. database/connector.py에 있는 함수 재사용 (중복 제거!)
        # 환경변수 로드나 DB 접속 정보는 connector가 알아서 처리함
        conn = get_connection()
        cur = conn.cursor()

        print("📦 주문 정보를 조회하는 중...\n")
        
        # [주의] 이 쿼리는 'orders' 테이블이 DB에 있어야만 작동합니다.
        # Week 2에서 만든 테이블이 그대로 남아있다면 OK입니다.
        query = """
            SELECT 
                o.id, 
                o.sender_zip, 
                o.recipient_zip, 
                i.name, 
                i.weight
            FROM orders o
            JOIN order_items i ON o.id = i.order_id;
        """
        cur.execute(query)
        
        rows = cur.fetchall()

        print(f"{'주문번호':<10} {'출발지':<10} {'도착지':<10} {'상품명':<15} {'무게(lb)':<10}")
        print("-" * 60)
        
        for row in rows:
            print(f"{row[0]:<10} {row[1]:<10} {row[2]:<10} {row[3]:<15} {row[4]:<10}")

        print("\n✅ 조회 완료!")
        
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        
    finally:
        # 안전하게 닫기
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    fetch_order_summary()