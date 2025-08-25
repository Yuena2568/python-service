"""
数据库初始化脚本
用于创建数据库和表结构
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings
from app.database import DatabaseManager
import aiomysql
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_database_if_not_exists():
    """
    如果数据库不存在，则创建数据库
    """
    try:
        # 连接到MySQL服务器（不指定数据库）
        connection = await aiomysql.connect(
            host=settings.db_host,
            port=settings.db_port,
            user=settings.db_user,
            password=settings.db_password,
        )
        
        async with connection.cursor() as cursor:
            # 创建数据库（如果不存在）
            await cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            logger.info(f"数据库 '{settings.db_name}' 创建成功或已存在")
        
        await connection.ensure_closed()
        
    except Exception as e:
        logger.error(f"创建数据库失败: {e}")
        raise


async def initialize_database():
    """
    初始化数据库：创建数据库和表
    """
    try:
        # 1. 创建数据库
        await create_database_if_not_exists()
        
        # 2. 创建数据库管理器并创建表
        db_manager = DatabaseManager(settings.database_url)
        await db_manager.create_tables()
        
        # 3. 关闭数据库连接
        await db_manager.close()
        
        logger.info("数据库初始化完成")
        
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise


if __name__ == "__main__":
    """
    运行数据库初始化
    使用方法：python init_db.py
    """
    print("开始初始化数据库...")
    print(f"数据库配置：{settings.db_host}:{settings.db_port}/{settings.db_name}")
    print("=" * 50)
    
    try:
        asyncio.run(initialize_database())
        print("=" * 50)
        print("数据库初始化成功！")
    except Exception as e:
        print("=" * 50)
        print(f"数据库初始化失败：{e}")
        print("请检查MySQL服务是否启动，以及数据库配置是否正确。")
        print("您可以修改 .env 文件中的数据库配置。")
        sys.exit(1)