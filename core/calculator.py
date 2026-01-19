# core/calculator.py

class ShippingCalculator:
    """
    배송비 계산을 담당하는 핵심 로직 (Week 2의 진화형)
    """
    
    # 운송사별 kg당 요금 (가상의 비즈니스 규칙)
    RATES = {
        'DHL': 5.0,   # DHL은 kg당 $5
        'FedEx': 4.0, # FedEx는 kg당 $4
        'UPS': 3.5    # UPS는 kg당 $3.5
    }

    def calculate_cost(self, weight_kg: float, carrier: str) -> float:
        """
        무게와 운송사를 받아 최종 배송비를 계산합니다.
        """
        # 1. 운송사 유효성 체크
        if carrier not in self.RATES:
            raise ValueError(f"❌ 지원하지 않는 운송사입니다: {carrier}")
            
        # 2. 기본 요금 계산
        rate_per_kg = self.RATES[carrier]
        base_cost = weight_kg * rate_per_kg

        # 3. (옵션) 10kg 이상이면 대량 화물 할인 10% 적용
        if weight_kg >= 10.0:
            base_cost *= 0.9  # 10% 할인
            
        # 소수점 2자리 반올림
        return round(base_cost, 2)