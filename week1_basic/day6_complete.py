import sqlite3
import requests
from fastapi import FastAPI

app = FastAPI()

# 1. 데이터베이스 준비 (금고 설치)
# check_same_thread=False: 웹 서버(여러 사람이 동시 접속)에서 DB를 쓰려면 이 옵션이 필요합니다.
conn = sqlite3.connect("final_logistics.db", check_same_thread=False)
cursor = conn.cursor()

# 2. 테이블 만들기 (장부 준비)
# 서버가 켜질 때 딱 한 번 실행됩니다.
cursor.execute("""
    CREATE TABLE IF NOT EXISTS trade_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_country TEXT,
        price REAL,
        weight REAL,
        exchange_rate REAL,
        total_cost INTEGER
    )
""")
conn.commit()
print("✅ DB 연결 및 테이블 준비 완료!")

# 3. 환율 가져오는 함수 (API)
def get_exchange_rate(code):
    try:
        url = f"https://api.frankfurter.app/latest?from={code}&to=KRW"
        response = requests.get(url)
        data = response.json()
        return data['rates']['KRW']
    except:
        return 1400.0 # 에러 시 비상용 환율

# --- API 설계 ---

@app.get("/")
def read_root():
    return {"message": "Smart Freight AI System is Online 🟢"}

# 기능 1: 계산하고 + 저장하기
@app.get("/calculate")
def calculate_and_save(from_country: str, price: float, weight: float):
    # A. 환율 조회
    rate = get_exchange_rate(from_country)
    
    # B. 비용 계산
    krw_price = price * rate
    duty = krw_price * 0.08
    shipping = weight * 10000
    total = int(krw_price + duty + shipping)
    
    # C. DB에 저장 (Insert) -> 여기가 오늘 추가된 핵심!
    sql = "INSERT INTO trade_history (from_country, price, weight, exchange_rate, total_cost) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(sql, (from_country, price, weight, rate, total))
    conn.commit() # 쾅! 저장
    
    # D. 결과 반환
    return {
        "status": "Saved ✅",
        "country": from_country,
        "total_cost_krw": total,
        "applied_rate": rate
    }

    
# 기능 2. 저장된 기록 불러오기 (History)
# 기존의 show_history 함수를 이걸로 교체하세요!
@app.get("/history")
def show_history():
    # 1. DB에서 데이터 가져오기
    cursor.execute("SELECT * FROM trade_history ORDER BY id DESC")
    rows = cursor.fetchall()
    
    # 2. 보기 좋게 포장하기 (Formatting)
    clean_history = []
    for row in rows:
        # row는 (1, 'USD', 100.0, 5.0, 1430.5, 185000) 같은 순서로 들어있습니다.
        # 이걸 이름표(Key)를 붙여서 딕셔너리로 만듭니다.
        record = {
            "id": row[0],
            "country": row[1],          # 나라
            "product_price": row[2],    # 물건 가격
            "weight": row[3],           # 무게
            "applied_rate": row[4],     # ★ 요청하신 환율 정보!
            "total_cost_krw": row[5]    # 최종 비용
        }
        clean_history.append(record)
        
    return {"saved_records": clean_history}


# 임의로 만들어진 홈페이지 들어가고 싶으면 /docs 붙이기