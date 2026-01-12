from abc import ABC, abstractmethod

class ShippingStrategy(ABC):
    @abstractmethod
    def calculate_cost(self, weight: float, width: float, height: float, depth: float) -> float:
        """
        [업데이트] 이제 무게뿐만 아니라 부피(가로, 세로, 높이)도 받습니다.
        """
        pass



# app/strategies.py 수정 (이어쓰기)

class FedExStrategy(ShippingStrategy):
    def calculate_cost(self, weight: float, width: float, height: float, depth: float) -> float:
        # 1. 부피 무게 계산 (FedEx 공식: 부피 / 139)
        dim_weight = (width * height * depth) / 139.0
        
        # 2. 청구 무게 결정 (실제 무게와 부피 무게 중 더 무거운 것 선택)
        chargeable_weight = max(weight, dim_weight)
        
        # 3. 요금 계산 (기본 $10 + lb당 $3)
        return 10.0 + (chargeable_weight * 3.0)

class UPSStrategy(ShippingStrategy):
    def calculate_cost(self, weight: float, width: float, height: float, depth: float) -> float:
        # UPS는 부피 나눔 계수가 다를 수 있음 (예: 166 - 소매 기준)
        dim_weight = (width * height * depth) / 166.0
        
        chargeable_weight = max(weight, dim_weight)
        
        # UPS는 기본료가 비싸지만 무게당 요금이 쌈
        return 15.0 + (chargeable_weight * 2.5)





# app/strategies.py 수정 (맨 아래)

class ShippingCostCalculator:
    def __init__(self, strategy: ShippingStrategy):
        self._strategy = strategy

    # 파라미터 4개 받도록 수정
    def calculate(self, weight: float, width: float, height: float, depth: float) -> float:
        return self._strategy.calculate_cost(weight, width, height, depth)