"""API 测试脚本 - 无需真实 API Key"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# 直接导入函数，避免配置依赖
import math

def parse_with_rules_local(message: str):
    """本地规则引擎（简化版）"""
    import re
    result = {
        "category": "餐饮",
        "subcategory": None,
        "radius": 5000,
        "limit": 10,
        "sort_by": None,
        "brands": None,
        "proximity": None
    }

    # 提取类型
    if "酒店" in message or "宾馆" in message:
        result["category"] = "酒店"
        if "经济型" in message or "快捷" in message:
            result["subcategory"] = "经济型酒店"
    elif "咖啡" in message or "星巴克" in message:
        result["category"] = "咖啡厅"
    elif "便利店" in message:
        result["category"] = "便利店"
    elif "地铁" in message:
        result["category"] = "地铁站"

    # 提取距离
    distance_match = re.search(r'(\d+)\s*(公里|km|千米)', message)
    if distance_match:
        result["radius"] = int(distance_match.group(1)) * 1000

    meter_match = re.search(r'(\d+)\s*(米|m)', message)
    if meter_match:
        result["radius"] = int(meter_match.group(1))

    # 提取数量
    count_match = re.search(r'(\d+)\s*个', message)
    if count_match:
        result["limit"] = min(int(count_match.group(1)), 20)

    # 提取排序
    if "地铁" in message and ("最近" in message or "近" in message):
        result["sort_by"] = "距离地铁站最近"
        result["proximity"] = "地铁站"

    return result

def test_rule_engine():
    """测试规则引擎"""
    print("=" * 50)
    print("测试规则引擎解析")
    print("=" * 50)

    test_cases = [
        "附近的星巴克",
        "1公里内的便利店",
        "附近5公里内离地铁站口最近的3个知名经济型连锁酒店门店",
        "500米内24小时营业的药店",
    ]

    for query in test_cases:
        print(f"\n查询: {query}")
        result = parse_with_rules_local(query)
        print(f"解析结果:")
        print(f"  - 类型: {result['category']}")
        print(f"  - 子类型: {result['subcategory']}")
        print(f"  - 半径: {result['radius']}米")
        print(f"  - 数量: {result['limit']}")
        print(f"  - 排序: {result['sort_by']}")
        print(f"  - 品牌: {result['brands']}")

def calculate_distance_local(lat1, lng1, lat2, lng2):
    """计算两点间距离（米）"""
    R = 6371000  # 地球半径（米）

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lng2 - lng1)

    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def test_distance_calculation():
    """测试距离计算"""
    print("\n" + "=" * 50)
    print("测试距离计算")
    print("=" * 50)

    # 北京天安门到国贸
    lat1, lng1 = 39.9042, 116.4074  # 天安门
    lat2, lng2 = 39.9088, 116.4577  # 国贸

    distance = calculate_distance_local(lat1, lng1, lat2, lng2)
    print(f"\n天安门 → 国贸")
    print(f"距离: {distance:.0f}米 ({distance/1000:.2f}公里)")

def main():
    print("\nDollyNav API 功能测试\n")
    
    test_rule_engine()
    test_distance_calculation()
    
    print("\n" + "=" * 50)
    print("测试完成！")
    print("=" * 50)
    print("\n提示: 这些是离线测试，不需要 API Key")
    print("要测试完整功能，请配置 API Key 后启动服务")

if __name__ == "__main__":
    main()

