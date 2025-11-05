"""响应模型定义"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class SubwayInfo(BaseModel):
    """地铁站信息"""
    name: str
    line: Optional[str] = None
    exit: Optional[str] = None
    distance: float  # 距离（米）


class POIResult(BaseModel):
    """POI 搜索结果"""
    id: str
    name: str
    category: str
    brand: Optional[str] = None
    location: Dict[str, float]
    address: str
    distance: float  # 距离用户（米）
    rating: Optional[float] = None
    phone: Optional[str] = None
    nearest_subway: Optional[SubwayInfo] = None


class ParsedQuery(BaseModel):
    """解析后的查询"""
    category: str
    subcategory: Optional[str] = None
    radius: int
    limit: int
    sort_by: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None


class ParseQueryResponse(BaseModel):
    """解析查询响应"""
    success: bool
    data: ParsedQuery
    display: Dict[str, str]
    message: Optional[str] = None


class SearchResponse(BaseModel):
    """搜索响应"""
    success: bool
    data: Dict[str, Any]
    message: Optional[str] = None


class RouteStep(BaseModel):
    """路线步骤"""
    instruction: str
    distance: float
    duration: float


class RouteResponse(BaseModel):
    """路线响应"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

