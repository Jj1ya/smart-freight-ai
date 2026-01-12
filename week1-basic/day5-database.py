import sqlite3  # 파이썬에 내장된 '가벼운 DB' 도구

# 1. DB 연결 (없으면 새로 만들고, 있으면 연결함)
# 'logistics_history.db'라는 파일이 폴더에 생길 겁니다.
conn = sqlite3.connect("logistics_history.db")
cursor = conn.cursor() # 커서(Cursor): 명령어를 대신 수행해주는 일꾼

# 2. 테이블(표) 만들기 (엑셀 시트 만드는 것과 비슷)
# IF NOT EXISTS: "이미 있으면 만들지 마" (에러 방지)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS shipment_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT,
        country_code TEXT,
        price REAL,
        weight REAL,
        total_cost INTEGER
    )
""")
conn.commit() # ★ 중요: 저장(Commit)을 안 하면 다 날아갑니다!
print("✅ DB 및 테이블 생성 완료!")

# 3. 데이터 저장 함수 (INSERT)
def save_shipment(product, country, price, weight, cost):
    sql = """
        INSERT INTO shipment_history (product_name, country_code, price, weight, total_cost)
        VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(sql, (product, country, price, weight, cost))
    conn.commit() # 저장 쾅!
    print(f"💾 저장 완료: {product} ({country})")

# 4. 데이터 조회 함수 (SELECT)
def show_all_history():
    print("\n--- 📋 저장된 견적 내역 불러오기 ---")
    # *: 모든 컬럼을 다 가져와라
    cursor.execute("SELECT * FROM shipment_history")
    rows = cursor.fetchall() # 조회된 모든 줄(Row)을 가져와라
    
    for row in rows:
        # row는 (1, 'Galaxy S25', 'USD', ...) 형태의 튜플로 나옵니다.
        print(f"ID:{row[0]} | 품명:{row[1]} | 국가:{row[2]} | 최종비용:{row[5]:,}원")

# --- 실행 테스트 ---
if __name__ == "__main__":
    # 가짜 데이터로 저장 테스트
    save_shipment("Tesla Model Y Parts", "USD", 5000, 100, 8500000)
    save_shipment("iPhone 16 Pro", "JPY", 1200, 0.5, 1500000)
    save_shipment("French Wine", "EUR", 50, 2.0, 120000)
    
    # 저장된 것 확인
    show_all_history()

    # 연결 종료 (매너)
    conn.close()