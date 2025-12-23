import requests

def get_usd_krw_rate():
    """
    실시간 USD -> KRW 환율을 가져오는 함수
    """
    # 1. API 주소 (Endpoint): 여기가 데이터를 주는 '창구'입니다.
    url = "https://api.frankfurter.app/latest?from=USD&to=KRW"

    print(f"환율 서버에 접속하는 중 ...({url})")

    # 2. 요청 보내기 (GET): "환율 정보 좀 주세요!"
    try:
        response = requests.get(url)

        # 3. 상태 확인: 200번은 '성공(OK)', 404/500번은 '에러'
        if response.status_code == 200:
            # 4. 데이터 뜯기 (JSON -> Dictionary 변환)
            data = response.json()
            rate = data['rates']['KRW']
            return rate
        else:
            print("서버에 문제가 생겼습니다.")
            return 1480 # 에러나면 임시 환율 적용 (Safely Logic)
    
    except Exception as e:
        print(f"인터넷 연결 에러: {e}")
        return 1480

# ------ 어제 만든 관세 계산기에 '실시간 환율' 적용하기 ------

def calculate_logistics_cost(usd_price, weight_kg):
    # 1. 오늘 환율 가져오기 (위에서 만든 함수 사용)
    current_rate = get_usd_krw_rate()
    print(f"오늘자 적용 환율: 1달러 = {current_rate}원")

    # 2. 가격을 원화로 변환
    krw_price = usd_price * current_rate

    # 3. 관세 (12% 가정)
    duty = krw_price * 0.12

    # 4. 운송료 (kg당 1만원 가정)
    shipping = weight_kg * 10000

    total = krw_price + duty + shipping
    return total

# ----- 실행 -----
print("--- Smart Freight AI 계산기 시작 ---")
final_cost = calculate_logistics_cost(1000,5) # 1000달러짜리 노트북, 5kg
print(f"최종 예상 비용: {int(final_cost):,}원")


# (:,. -> 숫자에 3자리마다 콤마 찍어주는 포맷팅)