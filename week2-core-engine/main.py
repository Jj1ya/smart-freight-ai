# main.py
from app.strategies import FedExStrategy, UPSStrategy, ShippingCostCalculator

def main():
    weight = 1.0
    width, height, depth = 50.0, 50.0, 50.0  
    print(f"📦 물품 정보: {weight}kg, 크기 {width}x{height}x{depth} inch\n")

    # 1. FedEx 전략 사용
    calculator = ShippingCostCalculator(FedExStrategy())
    cost = calculator.calculate(weight, width, height, depth)
    print(f"🚀 FedEx 요금: ${cost:.2f}")

    # 2. UPS 전략으로 교체 (코드 수정 없이 부품만 교체!)
    calculator = ShippingCostCalculator(UPSStrategy())
    cost = calculator.calculate(weight, width, height, depth)
    print(f"🚚 UPS 요금:   ${cost:.2f}")

if __name__ == "__main__":
    main()