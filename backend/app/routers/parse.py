"""解析路由"""
from fastapi import APIRouter, HTTPException
from app.models.request import ParseQueryRequest
from app.models.response import ParseQueryResponse, ParsedQuery
from app.services.llm_service import parse_query_with_llm

router = APIRouter(prefix="/api", tags=["parse"])


@router.post("/parse-query", response_model=ParseQueryResponse)
async def parse_query(request: ParseQueryRequest):
    """解析用户自然语言查询"""
    try:
        # 调用 LLM 解析
        parsed = await parse_query_with_llm(
            message=request.message,
            location={"lat": request.location.lat, "lng": request.location.lng}
        )
        
        # 构建响应
        data = ParsedQuery(
            category=parsed.get("category", "餐饮"),
            subcategory=parsed.get("subcategory"),
            radius=parsed.get("radius", 5000),
            limit=parsed.get("limit", 10),
            sort_by=parsed.get("sort_by"),
            filters={
                "brands": parsed.get("brands"),
                "proximity": parsed.get("proximity")
            }
        )
        
        # 构建展示信息
        display = {
            "type": data.subcategory or data.category,
            "range": f"{data.radius / 1000}公里" if data.radius >= 1000 else f"{data.radius}米",
            "count": f"{data.limit}个",
            "sort": data.sort_by or "距离最近"
        }
        
        return ParseQueryResponse(
            success=True,
            data=data,
            display=display
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"解析失败: {str(e)}")

