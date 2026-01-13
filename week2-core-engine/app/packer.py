from py3dbp import Packer, Bin, Item

class PackingEngine:
    def __init__(self):
        # 초기화 시점에는 별도 작업 없음
        pass

    def pack_items(self, items_data: list):
        # 테스트할 박스 후보군 (작은 순서대로 정렬)
        box_types = [
            Bin('Small-Box', 10, 10, 10, 100),
            Bin('Medium-Box', 20, 20, 20, 200),
            Bin('Large-Box',  50, 50, 50, 500)
        ]

        # 1. 각 박스 종류별로 "모두 다 들어가는지" 시뮬레이션
        for box in box_types:
            # 매번 새로운 패커를 만들어서 테스트 (초기화)
            packer = Packer()
            packer.add_bin(box)

            # 물건 담기
            for i in items_data:
                packer.add_item(Item(i['name'], i['w'], i['h'], i['d'], i['weight']))
            
            # 계산 시작
            packer.pack()
            
            # [검증 로직] 
            # 주문한 물건 개수 == 박스에 담긴 물건 개수 인가?
            target_bin = packer.bins[0]
            
            if len(target_bin.items) == len(items_data):
                # 빙고! 다 들어가는 박스를 찾음. 
                
                # 부피 효율 계산
                bin_volume = target_bin.width * target_bin.height * target_bin.depth
                
                # 담긴 물건들의 부피 합
                total_item_volume = 0
                for item in target_bin.items:
                    total_item_volume += (item.width * item.height * item.depth)

                # 0으로 나누기 방지 및 효율 계산
                if bin_volume > 0:
                    efficiency = (total_item_volume / bin_volume) * 100
                else:
                    efficiency = 0

                return {
                    "selected_box": target_bin.name,
                    "total_items": len(target_bin.items),
                    "efficiency": f"{efficiency:.2f}%",
                    "packed_items": [item.name for item in target_bin.items]
                }

        # 여기까지 왔다는 건, 제일 큰 박스에도 다 안 들어간다는 뜻
        return {
            "selected_box": "None (Too Big)",
            "total_items": 0,
            "efficiency": "0.00%",
            "packed_items": []
        }