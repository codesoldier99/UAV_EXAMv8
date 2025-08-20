"""
应用配置设置
"""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置类"""
    
    # 应用基础配置
    app_name: str = "UAV考点运营管理系统"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # 数据库配置
    database_url: str = os.getenv(
        "DATABASE_URL", 
        "mysql+pymysql://root:123456@localhost:3306/uav_exam"
    )
    
    # Redis配置
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # JWT配置
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # 微信小程序配置
    wechat_app_id: str = os.getenv("WECHAT_APP_ID", "")
    wechat_app_secret: str = os.getenv("WECHAT_APP_SECRET", "")
    
    # 文件上传配置
    upload_path: str = "uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    
    # 安全配置
    cors_origins: list = ["*"]  # 生产环境应该配置具体域名
    
    # 邮件配置
    smtp_server: str = os.getenv("SMTP_SERVER", "")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_username: str = os.getenv("SMTP_USERNAME", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    """获取应用配置的单例"""
    return Settings()


# 全局配置实例
settings = get_settings()