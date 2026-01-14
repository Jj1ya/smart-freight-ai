import pytest
from app.packer import PackingEngine

# 1. 작은 물건은 작은 박스에 들어가는가?
def test_pack_small_item():
    engine = PackingEngine()
    items = [
        {'name': 'Mouse', 'w': 5, 'h': 2, 'd': 5, 'weight': 0.5}
    ]
    
    result = engine.pack_items(items)
    
    assert result['selected_box'] == 'Small-Box'
    assert result['total_items'] == 1

# 2. 큰 물건은 큰 박스로 업그레이드되는가? (Best Fit)
def test_pack_large_item():
    engine = PackingEngine()
    items = [
        # Small-Box(10x10x10)에는 절대 안 들어가는 모니터
        {'name': 'Monitor', 'w': 20, 'h': 15, 'd': 5, 'weight': 5}
    ]
    
    result = engine.pack_items(items)
    
    # Small이 아니라 Medium이나 Large가 나와야 함
    assert result['selected_box'] != 'Small-Box'
    assert result['selected_box'] in ['Medium-Box', 'Large-Box']
    assert result['total_items'] == 1

# 3. [예외처리] 너무 커서 아무데도 안 들어가는 경우
def test_item_too_big():
    engine = PackingEngine()
    items = [
        # 집채만한 물건 (500x500x500)
        {'name': 'Car', 'w': 500, 'h': 500, 'd': 500, 'weight': 1000}
    ]
    
    result = engine.pack_items(items)
    
    assert result['selected_box'] == 'None (Too Big)'
    assert result['total_items'] == 0