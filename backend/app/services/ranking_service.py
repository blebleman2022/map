"""排序服务"""
from typing import List, Dict, Any, Optional
from app.services.amap_service import search_subway_stations, calculate_distance
import asyncio


async def rank_results(
    pois: List[Dict[str, Any]],
    user_location: Dict[str, float],
    sort_by: Optional[str] = None,
    proximity: Optional[str] = None,
    brands: Optional[List[str]] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """对搜索结果进行排序和筛选"""
    
    # 品牌筛选
    if brands:
        filtered = []
        for poi in pois:
            name = poi.get("name", "")
            if any(brand in name for brand in brands):
                filtered.append(poi)
        pois = filtered
    
    # 如果需要计算到地铁站的距离
    if proximity == "地铁站" or (sort_by and "地铁" in sort_by):
        # 搜索附近地铁站
        subway_stations = await search_subway_stations(
            location=user_location,
            radius=10000  # 10公里范围
        )
        
        # 为每个 POI 找到最近的地铁站
        for poi in pois:
            nearest_subway = find_nearest_subway(poi, subway_stations)
            poi["nearest_subway"] = nearest_subway
    
    # 排序
    if sort_by and "地铁" in sort_by:
        # 按距离地铁站排序
        pois.sort(key=lambda x: x.get("nearest_subway", {}).get("distance", float('inf')))
    elif sort_by and "评分" in sort_by:
        # 按评分排序（暂时用距离代替）
        pois.sort(key=lambda x: x.get("distance", float('inf')))
    else:
        # 默认按距离用户排序
        pois.sort(key=lambda x: x.get("distance", float('inf')))
    
    # 限制数量
    return pois[:limit]


def find_nearest_subway(poi: Dict[str, Any], subway_stations: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """找到最近的地铁站"""
    if not subway_stations:
        return None
    
    poi_loc = poi.get("location", {})
    min_distance = float('inf')
    nearest = None
    
    for station in subway_stations:
        station_loc = station.get("location", {})
        distance = calculate_distance(
            poi_loc.get("lat", 0), poi_loc.get("lng", 0),
            station_loc.get("lat", 0), station_loc.get("lng", 0)
        )
        
        if distance < min_distance:
            min_distance = distance
            nearest = {
                "name": station.get("name", ""),
                "line": None,  # 高德 API 可能不返回线路信息
                "exit": None,
                "distance": round(distance, 0)
            }
    
    return nearest


def calculate_score(poi: Dict[str, Any]) -> float:
    """计算综合得分"""
    score = 0.0
    
    # 距离得分（越近越高）
    distance = poi.get("distance", 10000)
    distance_score = max(0, 100 - distance / 100)
    score += distance_score * 0.6
    
    # 地铁站距离得分
    if poi.get("nearest_subway"):
        subway_distance = poi["nearest_subway"].get("distance", 10000)
        subway_score = max(0, 100 - subway_distance / 10)
        score += subway_score * 0.4
    
    return score

