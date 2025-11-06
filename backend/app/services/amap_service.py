"""高德地图服务"""
import httpx
from typing import List, Dict, Any, Optional, Tuple
from app.config import get_settings
import math

settings = get_settings()


async def geocode_location(address: str, city: str = "全国") -> Optional[Dict[str, float]]:
    """地理编码：将地址转换为经纬度坐标

    Args:
        address: 地址或地点名称
        city: 城市名称，默认"全国"

    Returns:
        {"lat": 纬度, "lng": 经度} 或 None
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                "https://restapi.amap.com/v3/geocode/geo",
                params={
                    "key": settings.amap_api_key,
                    "address": address,
                    "city": city
                }
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "1" and data.get("geocodes"):
                    geocode = data["geocodes"][0]
                    location_str = geocode.get("location", "")
                    if location_str:
                        lng, lat = map(float, location_str.split(","))
                        return {"lat": lat, "lng": lng}

            return None

    except Exception as e:
        print(f"地理编码失败: {e}")
        return None


# 类型映射
CATEGORY_MAPPING = {
    "酒店": "100000",
    "餐饮": "050000",
    "咖啡厅": "050500",
    "便利店": "060100",
    "地铁站": "150500",
    "商场": "060000",
    "超市": "060200",
    "银行": "160100",
    "医院": "090000",
    "药店": "090600",
}


async def search_nearby_pois(
    location: Dict[str, float],
    category: str,
    radius: int = 5000,
    keywords: Optional[str] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """搜索附近 POI"""
    
    # 获取类型码
    type_code = CATEGORY_MAPPING.get(category, "")
    
    params = {
        "key": settings.amap_api_key,
        "location": f"{location['lng']},{location['lat']}",
        "radius": radius,
        "types": type_code,
        "offset": min(limit * 2, 50),  # 多获取一些，后续筛选
        "extensions": "all"
    }
    
    if keywords:
        params["keywords"] = keywords
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{settings.amap_base_url}/place/around",
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "1" and data.get("pois"):
                    pois = data["pois"]
                    results = []
                    
                    for poi in pois[:limit * 2]:
                        # 解析位置
                        loc_str = poi.get("location", "")
                        if not loc_str or loc_str == "":
                            continue
                            
                        lng, lat = map(float, loc_str.split(","))
                        
                        # 计算距离
                        distance = calculate_distance(
                            location["lat"], location["lng"],
                            lat, lng
                        )
                        
                        result = {
                            "id": poi.get("id", ""),
                            "name": poi.get("name", ""),
                            "category": category,
                            "location": {"lat": lat, "lng": lng},
                            "address": poi.get("address", ""),
                            "distance": distance,
                            "phone": poi.get("tel", ""),
                        }
                        
                        results.append(result)
                    
                    return results
                    
    except Exception as e:
        print(f"高德地图 API 调用失败: {e}")
    
    return []


async def search_subway_stations(
    location: Dict[str, float],
    radius: int = 5000
) -> List[Dict[str, Any]]:
    """搜索附近地铁站"""
    return await search_nearby_pois(
        location=location,
        category="地铁站",
        radius=radius,
        limit=20
    )


def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """计算两点间距离（米）- Haversine 公式"""
    R = 6371000  # 地球半径（米）
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lng2 - lng1)
    
    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


async def get_route(
    origin: Dict[str, float],
    destination: Dict[str, float],
    mode: str = "walking"
) -> Optional[Dict[str, Any]]:
    """获取路线规划"""
    
    # 模式映射
    mode_mapping = {
        "walking": "walking",
        "driving": "driving",
        "transit": "integrated"  # 公交
    }
    
    api_mode = mode_mapping.get(mode, "walking")
    
    params = {
        "key": settings.amap_api_key,
        "origin": f"{origin['lng']},{origin['lat']}",
        "destination": f"{destination['lng']},{destination['lat']}"
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{settings.amap_base_url}/direction/{api_mode}",
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "1":
                    # 解析路线
                    if api_mode == "walking":
                        route = data.get("route", {})
                        paths = route.get("paths", [])
                        if paths:
                            path = paths[0]
                            return {
                                "distance": float(path.get("distance", 0)),
                                "duration": float(path.get("duration", 0)) / 60,  # 转为分钟
                                "mode": mode,
                                "steps": parse_steps(path.get("steps", []))
                            }
                    elif api_mode == "driving":
                        route = data.get("route", {})
                        paths = route.get("paths", [])
                        if paths:
                            path = paths[0]
                            return {
                                "distance": float(path.get("distance", 0)),
                                "duration": float(path.get("duration", 0)) / 60,
                                "mode": mode,
                                "steps": parse_steps(path.get("steps", []))
                            }
                            
    except Exception as e:
        print(f"路线规划失败: {e}")
    
    return None


def parse_steps(steps: List[Dict]) -> List[Dict[str, Any]]:
    """解析路线步骤"""
    result = []
    for step in steps[:10]:  # 最多返回10步
        result.append({
            "instruction": step.get("instruction", ""),
            "distance": float(step.get("distance", 0)),
            "duration": float(step.get("duration", 0)) / 60
        })
    return result

