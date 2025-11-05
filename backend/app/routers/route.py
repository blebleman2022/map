"""路线规划路由"""
from fastapi import APIRouter, HTTPException
from app.models.request import RouteRequest
from app.models.response import RouteResponse
from app.services.amap_service import get_route

router = APIRouter(prefix="/api", tags=["route"])


@router.post("/route", response_model=RouteResponse)
async def plan_route(request: RouteRequest):
    """规划路线"""
    try:
        route_data = await get_route(
            origin={"lat": request.origin.lat, "lng": request.origin.lng},
            destination={"lat": request.destination.lat, "lng": request.destination.lng},
            mode=request.mode
        )
        
        if not route_data:
            return RouteResponse(
                success=False,
                message="无法规划路线，请检查起点和终点"
            )
        
        return RouteResponse(
            success=True,
            data=route_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"路线规划失败: {str(e)}")

