"""请求模型定义"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, List


class Location(BaseModel):
    """位置信息"""
    lat: float = Field(..., description="纬度", ge=-90, le=90)
    lng: float = Field(..., description="经度", ge=-180, le=180)


class ParseQueryRequest(BaseModel):
    """解析查询请求"""
    message: str = Field(..., min_length=1, max_length=500, description="用户查询消息")
    location: Location = Field(..., description="用户位置")


class SearchRequest(BaseModel):
    """搜索请求"""
    category: str = Field(..., description="地点类型")
    subcategory: Optional[str] = Field(None, description="子类型")
    radius: int = Field(5000, ge=100, le=50000, description="搜索半径（米）")
    limit: int = Field(10, ge=1, le=20, description="返回数量")
    sort_by: Optional[str] = Field(None, description="排序方式")
    brands: Optional[List[str]] = Field(None, description="品牌筛选")
    proximity: Optional[str] = Field(None, description="靠近的地点类型")
    location: Location = Field(..., description="用户位置")


class RouteRequest(BaseModel):
    """路线规划请求"""
    origin: Location = Field(..., description="起点")
    destination: Location = Field(..., description="终点")
    mode: str = Field("walking", description="出行方式: walking, driving, transit")

