# main.py
from app.packer import PackingEngine

def main():
    print("🤖 [AI Engine] 3D 적재 최적화 프로세스 시작...\n")

    # 1. 가상의 주문 데이터 (물건 목록)
    order_items = [
        {'name': 'iPhone 15', 'w': 2, 'h': 5, 'd': 1, 'weight': 0.5},
        {'name': 'Galaxy S24', 'w': 2, 'h': 5, 'd': 1, 'weight': 0.5},
        {'name': 'Gaming Monitor', 'w': 20, 'h': 10, 'd': 5, 'weight': 5},
        {'name': 'Keyboard', 'w': 10, 'h': 4, 'd': 1, 'weight': 1}
    ]
    
    # 물건을 좀 많이 만들어볼까요? (아이폰 5개 추가)
    for _ in range(5):
        order_items.append({'name': 'iPhone 15 Box', 'w': 2, 'h': 5, 'd': 1, 'weight': 0.5})

    print(f"📦 주문 들어온 물건 수: {len(order_items)}개")

    # 2. AI 엔진 호출
    engine = PackingEngine()
    result = engine.pack_items(order_items)

    # 3. 결과 리포트
    print("-" * 40)
    print(f"✅ 추천 박스: {result['selected_box']}")
    print(f"📊 공간 효율(적재율): {result['efficiency']}")
    print(f"📥 담긴 물건 수: {result['total_items']}개")
    print(f"📝 담긴 목록: {result['packed_items']}")
    print("-" * 40)

if __name__ == "__main__":
    main()