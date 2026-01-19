# database/user_dao.py
from database.connector import get_connection

class UserDAO:
    def create_user(self, username, email):
        """새로운 유저를 생성하고 생성된 ID를 반환합니다."""
        conn = get_connection()
        cur = conn.cursor()
        try:
            # SQL Injection 방지를 위해 %s 바인딩 사용
            query = """
                INSERT INTO users (username, email) 
                VALUES (%s, %s) 
                RETURNING id;
            """
            cur.execute(query, (username, email))
            new_id = cur.fetchone()[0]
            conn.commit() # 변경사항 저장
            return new_id
            
        except Exception as e:
            conn.rollback() # 에러나면 되돌리기
            print(f"❌ Failed to create user: {e}")
            raise e
            
        finally:
            cur.close()
            conn.close()

    def get_user_by_email(self, email):
        """이메일로 유저 정보를 찾습니다."""
        conn = get_connection()
        cur = conn.cursor()
        try:
            query = "SELECT id, username, email, created_at FROM users WHERE email = %s"
            cur.execute(query, (email,)) # 튜플 (email,) 주의!
            
            row = cur.fetchone()
            if row:
                # 튜플(row)을 딕셔너리로 변환하여 반환 (사용하기 편하게)
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

    def get_all_users(self, limit=10):
        """모든 유저 목록을 가져옵니다 (기본 10명 제한)"""
        conn = get_connection()
        cur = conn.cursor()
        try:
            query = "SELECT id, username, email FROM users LIMIT %s"
            cur.execute(query, (limit,))
            
            rows = cur.fetchall()
            # List Comprehension으로 결과 가공
            return [{"id": r[0], "username": r[1], "email": r[2]} for r in rows]
            
        finally:
            cur.close()
            conn.close()