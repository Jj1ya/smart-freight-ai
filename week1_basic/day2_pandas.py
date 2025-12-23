import pandas as pd

# [상황] 댈러스 창고에 들어온 화물 리스트 (가상의 엑셀 데이터)
data = {
    'Invoice_No': ['INV-001', 'INV-002', 'INV-003'],
    'Product': ['Semiconductor', 'T-Shirt', 'Auto Parts'],
    'Weight_kg': [50, 10, 100],
    'Unit_Price': [5000, 20, 300]
}

# 1. 데이터프레임(표) 만들기 (엑셀을 코드로 만든다고 생각하세요)
df = pd.DataFrame(data)

print("--- 원본 데이터 ---")
print(df)

# [미션] 무게가 30kg 이상인 'Heavy Cargo'만 골라내시오.
# 엑셀 필터 기능을 코드로 구현하는 겁니다. (SQL의 WHERE절과 같음)
heavy_cargo = df[df['Weight_kg'] >= 30]

print("\n--- 중량 화물 (30kg 이상) ---")
print(heavy_cargo)

# [미션] 총 화물 가치(Total Value)를 계산하시오.
total_value = df['Unit_Price'].sum()
print(f"\n총 화물 가치: ${total_value}")