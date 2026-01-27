from database.connector import get_connection

class ShipmentDAO:
    def create_shipment(self, user_id, origin, dest, weight, conn=None):
        """새 배송 주문을 생성합니다. (트랜잭션 지원)"""
        created_conn = False
        # 외부에서 연결(conn)을 안 줬으면, 내가 직접 만든다.
        if conn is None:
            conn = get_connection()
            created_conn = True

        cur = conn.cursor()
        try:
            query = """
                INSERT INTO shipments (user_id, origin_country, dest_country, weight_kg)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """
            cur.execute(query, (user_id, origin, dest, weight))
            new_id = cur.fetchone()[0]

            # 내가 만든 연결일 때만 커밋한다. (외부에서 받았다면 커밋 보류)
            if created_conn:
                conn.commit()
            
            return new_id
            
        except Exception as e:
            # 내가 만든 연결일 때만 롤백한다.
            if created_conn:
                conn.rollback()
            raise e
        finally:
            cur.close()
            if created_conn:
                conn.close()

    def get_shipments_by_user(self, user_id):
        """특정 유저의 모든 배송 내역을 조회합니다."""
        conn = get_connection()
        cur = conn.cursor()
        try:
            query = """
                SELECT id, origin_country, dest_country, weight_kg, status, created_at
                FROM shipments
                WHERE user_id = %s
                ORDER BY created_at DESC
            """
            cur.execute(query, (user_id,))
            rows = cur.fetchall()
            
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
    


    def get_pending_shipments(self):
        """배송비가 아직 계산되지 않은(0원) 주문들을 가져옵니다."""
        conn = get_connection()
        cur = conn.cursor()
        try:
            # cost가 0이거나 NULL인 경우 조회
            query = """
                SELECT id, user_id, weight_kg 
                FROM shipments 
                WHERE cost = 0 OR cost IS NULL
            """
            cur.execute(query)
            rows = cur.fetchall()
            return [{"id": r[0], "user_id": r[1], "weight": r[2]} for r in rows]
        finally:
            cur.close()
            conn.close()

    def update_cost(self, shipment_id, cost, conn=None):
        """배송비를 업데이트합니다. (트랜잭션 지원)"""
        created_conn = False
        if conn is None:
            conn = get_connection()
            created_conn = True
            
        cur = conn.cursor()
        try:
            cur.execute("UPDATE shipments SET cost = %s, status = 'PROCESSED' WHERE id = %s", (cost, shipment_id))
            if created_conn:
                conn.commit()
        except Exception as e:
            if created_conn:
                conn.rollback()
            raise e
        finally:
            cur.close()
            if created_conn:
                conn.close()