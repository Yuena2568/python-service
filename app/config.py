"""
应用配置文件
管理应用的所有配置参数，包括数据库连接、JWT设置等
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    应用设置类
    使用Pydantic的BaseSettings来管理配置，支持从环境变量读取配置
    """
    
    # 数据库配置
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = ""
    db_name: str = "user_service"
    
    # JWT配置
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # 应用配置
    app_name: str = "用户服务API"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # API配置
    api_v1_prefix: str = "/api/v1"
    
    class Config:
        # 指定环境变量文件位置
        env_file = ".env"
        # 设置环境变量前缀（可选）
        env_prefix = ""
    
    @property
    def database_url(self) -> str:
        """
        构建数据库连接URL
        使用aiomysql驱动进行异步数据库连接
        
        Returns:
            str: 完整的数据库连接URL
        """
        return f"mysql+aiomysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


# 创建全局设置实例
settings = Settings()