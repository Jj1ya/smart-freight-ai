# database/shipment_dao.py
from database.connector import get_connection

class ShipmentDAO:
    def create_shipment(self, user_id, origin, dest, weight):
        """새 배송 주문을 생성합니다."""
        conn = get_connection()
        cur = conn.cursor()
        try:
            # status는 Default 값('PENDING')이 들어가므로 생략 가능
            query = """
                INSERT INTO shipments (user_id, origin_country, dest_country, weight_kg)
                VALUES (%s, %s, %s, %s)
                RETURNING id, created_at;
            """
            cur.execute(query, (user_id, origin, dest, weight))
            row = cur.fetchone()
            conn.commit()
            return {"id": row[0], "created_at": row[1]}
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    def get_shipments_by_user(self, user_id):
        """특정 유저의 모든 배송 내역을 조회합니다."""
        conn = get_connection()
        cur = conn.cursor()
        try:
            # 최신 주문이 위로 오도록 정렬 (ORDER BY created_at DESC)
            query = """
                SELECT id, origin_country, dest_country, weight_kg, status, created_at
                FROM shipments
                WHERE user_id = %s
                ORDER BY created_at DESC
            """
            cur.execute(query, (user_id,))
            rows = cur.fetchall()
            
            # 리스트 컴프리헨션으로 변환
            return [
                {
                    "id": r[0],
                    "origin": r[1],
                    "destination": r[2],
                    "weight": r[3],
                    "status": r[4],
                    "date": r[5]
                }
                for r in rows
            ]
            
        finally:
            cur.close()
            conn.close()