"""LLM 服务 - 自然语言解析"""
import json
import httpx
from typing import Dict, Any
from app.config import get_settings

settings = get_settings()


# 知名品牌库
BRAND_DATABASE = {
    "酒店": ["如家", "汉庭", "7天", "锦江之星", "格林豪泰", "维也纳", "全季", "桔子"],
    "咖啡": ["星巴克", "瑞幸", "Costa", "太平洋咖啡", "Manner", "Tims"],
    "便利店": ["7-11", "全家", "罗森", "便利蜂", "美宜佳"],
    "快餐": ["麦当劳", "肯德基", "汉堡王", "德克士", "必胜客"],
}


async def parse_query_with_llm(message: str, location: Dict[str, float]) -> Dict[str, Any]:
    """使用 LLM 解析用户查询"""
    
    # 构建提示词
    system_prompt = """你是一个地图搜索助手，需要将用户的自然语言转换为结构化查询。

请提取以下信息并返回 JSON 格式：
{
  "category": "地点类型（如：酒店、餐厅、便利店、地铁站、商场、咖啡厅等）",
  "subcategory": "子类型（如：经济型酒店、川菜馆等，可选）",
  "radius": 搜索半径（米，默认5000，最大50000）,
  "limit": 返回数量（默认10，最大20）,
  "sort_by": "排序方式（如：距离最近、评分最高、距离地铁站最近等，可选）",
  "brands": ["品牌列表，可选"],
  "proximity": "靠近的地点类型（如：地铁站、商场等，可选）"
}

示例：
用户："我要找附近5公里内离地铁站口最近的3个知名经济型连锁酒店门店"
返回：
{
  "category": "酒店",
  "subcategory": "经济型连锁酒店",
  "radius": 5000,
  "limit": 3,
  "sort_by": "距离地铁站最近",
  "brands": ["如家", "汉庭", "7天", "锦江之星"],
  "proximity": "地铁站"
}

只返回 JSON，不要其他解释。"""

    user_message = f"用户查询：{message}\n用户位置：纬度{location['lat']}, 经度{location['lng']}"

    # 优先使用 SiliconFlow (DeepSeek)
    if settings.siliconflow_api_key:
        return await parse_with_siliconflow(system_prompt, user_message)
    # 其次使用通义千问
    elif settings.dashscope_api_key:
        return await parse_with_dashscope(system_prompt, user_message)
    elif settings.openai_api_key:
        return await parse_with_openai(system_prompt, user_message)
    else:
        # 降级到规则引擎
        return parse_with_rules(message)


async def parse_with_siliconflow(system_prompt: str, user_message: str) -> Dict[str, Any]:
    """使用 SiliconFlow (DeepSeek-R1) 解析"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.siliconflow.cn/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.siliconflow_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1000
                }
            )

            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                # 提取 JSON
                # DeepSeek-R1 可能会有思考过程，需要提取 JSON 部分
                if "```json" in content:
                    json_str = content.split("```json")[1].split("```")[0].strip()
                elif "{" in content:
                    # 提取第一个 JSON 对象
                    start = content.index("{")
                    end = content.rindex("}") + 1
                    json_str = content[start:end]
                else:
                    json_str = content

                parsed = json.loads(json_str)
                return parsed
            else:
                print(f"SiliconFlow API 错误: {response.status_code}")
                return parse_with_rules(user_message)

    except Exception as e:
        print(f"SiliconFlow 解析失败: {e}")
        return parse_with_rules(user_message)


async def parse_with_dashscope(system_prompt: str, user_message: str) -> Dict[str, Any]:
    """使用通义千问解析"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
                headers={
                    "Authorization": f"Bearer {settings.dashscope_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "qwen-turbo",
                    "input": {
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_message}
                        ]
                    },
                    "parameters": {
                        "result_format": "message"
                    }
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["output"]["choices"][0]["message"]["content"]
                # 提取 JSON
                parsed = json.loads(content)
                return parsed
            else:
                return parse_with_rules(user_message)
                
    except Exception as e:
        print(f"LLM 解析失败: {e}")
        return parse_with_rules(user_message)


async def parse_with_openai(system_prompt: str, user_message: str) -> Dict[str, Any]:
    """使用 OpenAI 解析"""
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.openai_api_key)
        
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3
        )
        
        content = response.choices[0].message.content
        parsed = json.loads(content)
        return parsed
        
    except Exception as e:
        print(f"OpenAI 解析失败: {e}")
        return parse_with_rules(user_message)


def parse_with_rules(message: str) -> Dict[str, Any]:
    """规则引擎解析（降级方案）"""
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
    elif "商场" in message or "购物" in message:
        result["category"] = "商场"
    
    # 提取距离
    import re
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
    
    # 提取品牌
    for category, brands in BRAND_DATABASE.items():
        for brand in brands:
            if brand in message:
                result["brands"] = [brand]
                break
    
    # 提取排序
    if "地铁" in message and ("最近" in message or "近" in message):
        result["sort_by"] = "距离地铁站最近"
        result["proximity"] = "地铁站"
    
    return result

