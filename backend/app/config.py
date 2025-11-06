"""配置管理"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置"""
    
    # 高德地图配置
    amap_api_key: str = ""
    amap_base_url: str = "https://restapi.amap.com/v3"
    
    # LLM 配置
    dashscope_api_key: str = ""
    openai_api_key: str = ""
    siliconflow_api_key: str = ""
    
    # 服务配置
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS 配置
    cors_origins: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()

