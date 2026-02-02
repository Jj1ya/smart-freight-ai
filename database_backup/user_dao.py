from database.connector import get_connection

class UserDAO:
    def update_credits(self, user_id, amount, conn=None):
        """
        유저의 잔액을 변경합니다. (마이너스면 차감)
        conn이 없으면 스스로 만들어서 씁니다 (하위 호환성).
        """
        created_conn = False
        if conn is None:
            conn = get_connection()
            created_conn = True
            
        cur = conn.cursor()
        try:
            # 잔액 업데이트 (단순 차감 로직)
            query = "UPDATE users SET credits = credits + %s WHERE id = %s"
            cur.execute(query, (amount, user_id))
            
            # 외부에서 conn을 받았다면, 여기서 commit 하지 않음! (부모가 알아서 함)
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

    def get_user_by_id(self, user_id):
        """ID로 유저 정보를 조회합니다."""
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, username, email, credits FROM users WHERE id = %s", (user_id,))
            row = cur.fetchone()
            if row:
                return {
                    "id": row[0], 
                    "username": row[1], 
                    "email": row[2],
                    "credits": row[3] # 지갑 잔액 추가됨
                }
            return None
        finally:
            cur.close()
            conn.close()

    def get_all_users(self, limit=10):
        """모든 유저 목록을 가져옵니다"""
        conn = get_connection()
        cur = conn.cursor()
        try:
            query = "SELECT id, username, email FROM users LIMIT %s"
            cur.execute(query, (limit,))
            rows = cur.fetchall()
            return [{"id": r[0], "username": r[1], "email": r[2]} for r in rows]
        finally:
            cur.close()
            conn.close()
            
    def get_user_by_email(self, email):
        """이메일로 유저 정보를 찾습니다."""
        conn = get_connection()
        cur = conn.cursor()
        try:
            query = "SELECT id, username, email, created_at FROM users WHERE email = %s"
            cur.execute(query, (email,))
            row = cur.fetchone()
            if row:
                return {
                    "id": row[0],
                    "username": row[1],
                    "email": row[2],
                    "created_at": row[3]
                }
            return None
        finally:
            cur.close()
            conn.close()