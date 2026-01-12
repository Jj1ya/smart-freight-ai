from fastapi import FastAPI
import requests

app = FastAPI()

# [변경 1] 함수가 '어느 나라 돈(from_code)'인지 입력을 받도록 수정
def get_real_time_rate(from_code):
    try:
        # URL에 f-string을 써서 from_code를 쏙 집어넣음 (USD 자리에 변수가 들어감)
        # to=KRW는 일단 고정 (우리는 한국으로 수입하니까)
        url = f"https://api.frankfurter.app/latest?from={from_code}&to=KRW"
        
        response = requests.get(url)
        data = response.json()
        return data['rates']['KRW']
    except:
        print("환율 조회 실패, 기본값 사용")
        return 1400.0 

@app.get("/")
def read_root():
    return {"message": "Global Logistics AI Server is Running! 🌍"}

# [변경 2] API가 '출발 국가(from_country)'를 입력받도록 수정
# 기본값(default)은 "USD"로 설정
@app.get("/calculate")
def calculate_shipping(from_country: str, price: float, weight: float):
    
    # 1. 사용자가 입력한 나라(from_country)의 환율을 가져옴
    rate = get_real_time_rate(from_country)
    
    # 2. 계산 로직 (나머지는 동일)
    krw_price = price * rate
    duty = krw_price * 0.08
    shipping = weight * 10000 
    total = krw_price + duty + shipping
    
    return {
        "buy_from": from_country,  # 어느 나라에서 샀는지 표시
        "product_price": price,
        "exchange_rate": rate,
        "total_estimated_krw": int(total),
        "breakdown": {
            "duty": int(duty),
            "shipping": int(shipping)
        }
    }