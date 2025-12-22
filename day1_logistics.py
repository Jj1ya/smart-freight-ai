# [미션] 물건 가격과 무게를 입력하면, 관세와 배송비를 포함한 최종 가격을 계산하시오.

def calculate_total_cost(price, weight, tax_rate):
    # 1. 관세 계산 (가격 * 관세율)
    duty = price * tax_rate
    
    # 2. 배송비 계산 (기본 $10 + kg당 $2) -> 이런 게 '비즈니스 로직'입니다.
    shipping_cost = 10 + (weight * 2)
    
    # 3. 총합
    total = price + duty + shipping_cost
    
    return total

# --- 실행 테스트 ---
# 상품: $1000짜리 노트북, 무게: 2kg, 관세율: 10%(0.1)
product_price = 1000
product_weight = 2
current_tax_rate = 0.1

final_cost = calculate_total_cost(product_price, product_weight, current_tax_rate)

# f-string: 파이썬에서 변수를 출력할 때 가장 많이 쓰는 문법입니다.
print(f"상품 가격: ${product_price}")
print(f"예상 관세 및 배송비 포함 최종 금액: ${final_cost}")