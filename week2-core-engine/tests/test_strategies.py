import pytest
from app.strategies import FedExStrategy, UPSStrategy, ShippingCostCalculator

# 1. FedEx 요금 계산 테스트
def test_fedex_calculation():
    # 시나리오: 10kg, 작은 박스 (부피무게 적용 안 됨)
    strategy = FedExStrategy()
    # 공식: 10.0 + (10kg * 2.0) = 30.0
    cost = strategy.calculate_cost(weight=10, width=10, height=10, depth=10)
    
    assert cost == 40.0  # assert: "이거 아니면 에러 터뜨려!"라는 뜻

# 2. UPS 요금 계산 테스트
def test_ups_calculation():
    # 시나리오: 10kg, 작은 박스
    strategy = UPSStrategy()
    # 공식: 15.0 + (10kg * 1.5) = 30.0
    cost = strategy.calculate_cost(weight=10, width=10, height=10, depth=10)
    
    assert cost == 40.0

# 3. [심화] 부피 무게 적용 테스트 (솜뭉치 시나리오)
def test_dimensional_weight_logic():
    # 시나리오: 무게는 1kg지만, 부피는 엄청 큼(50x50x50)
    # FedEx Dim Factor: 139
    # 부피무게 = (50*50*50) / 139 = 899.28...
    
    strategy = FedExStrategy()
    cost = strategy.calculate_cost(weight=1, width=50, height=50, depth=50)
    
    # 단순 무게(1kg) 요금인 $12가 아니라, 부피무게 요금이 나와야 함
    # 10 + (899.28 * 2) ≈ 1808.5...
    assert cost > 1000  # 정확한 값보다는 "요금 폭탄이 맞는지" 확인