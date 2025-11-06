"""搜索路由"""
from fastapi import APIRouter, HTTPException
from app.models.request import SearchRequest
from app.models.response import SearchResponse
from app.services.amap_service import search_nearby_pois
from app.services.ranking_service import rank_results

router = APIRouter(prefix="/api", tags=["search"])


@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """搜索地点"""
    try:
        # 构建关键词
        keywords = None
        if request.brands:
            keywords = "|".join(request.brands)
        elif request.subcategory:
            keywords = request.subcategory
        
        # 搜索 POI
        pois = await search_nearby_pois(
            location={"lat": request.location.lat, "lng": request.location.lng},
            category=request.category,
            radius=request.radius,
            keywords=keywords,
            limit=request.limit * 2  # 多获取一些用于筛选
        )
        
        if not pois:
            return SearchResponse(
                success=False,
                data={"total": 0, "results": []},
                message="未找到符合条件的地点，请尝试放宽搜索条件"
            )
        
        # 排序和筛选
        ranked_pois = await rank_results(
            pois=pois,
            user_location={"lat": request.location.lat, "lng": request.location.lng},
            sort_by=request.sort_by,
            proximity=request.proximity,
            brands=request.brands,
            limit=request.limit
        )
        
        return SearchResponse(
            success=True,
            data={
                "total": len(ranked_pois),
                "results": ranked_pois
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

