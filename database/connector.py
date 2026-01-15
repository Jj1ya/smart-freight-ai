import os
import psycopg2
from dotenv import load_dotenv

# 1. 환경 변수 로드
load_dotenv()

# 경로 설정 (현재 파일 위치 기준)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

def get_connection():
    """DB 연결 객체 반환 (재사용 목적)"""
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )

def init_db():
    """schema.sql을 읽어서 PostgreSQL 테이블 생성"""
    if not os.path.exists(SCHEMA_PATH):
        print(f"❌ [Error] Schema file not found: {SCHEMA_PATH}")
        return

    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        # 스키마 파일 읽기
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # 실행 (Postgres는 executescript가 없어서 execute로 처리 가능하거나, 
        # 여러 구문일 경우 ; 로 구분된 처리가 필요함. psycopg2는 다중 쿼리 지원함)
        cur.execute(sql_script)
        
        conn.commit()
        print("✅ [Success] PostgreSQL Tables created successfully.")

    except Exception as e:
        print(f"❌ [Error] DB Initialization Failed: {e}")
        if conn:
            conn.rollback() # 에러 시 롤백
            
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # 이 파일을 직접 실행하면 테이블 생성 시도
    init_db()