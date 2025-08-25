"""
数据库配置和连接管理
这个文件负责管理数据库连接、创建表等操作
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """
    数据库模型基类
    所有的数据库表都应该继承这个基类
    """
    pass


class User(Base):
    """
    用户表模型
    定义了用户的基本信息字段
    """
    __tablename__ = "users"
    
    # 主键ID，自动递增
    id = Column(Integer, primary_key=True, index=True, comment="用户唯一标识")
    
    # 用户名，唯一且不能为空
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名")
    
    # 邮箱，唯一且不能为空
    email = Column(String(100), unique=True, index=True, nullable=False, comment="邮箱地址")
    
    # 加密后的密码
    hashed_password = Column(String(255), nullable=False, comment="加密后的密码")
    
    # 用户状态：True=启用，False=禁用
    is_active = Column(Boolean, default=True, comment="用户状态")
    
    # 创建时间
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    # 最后登录时间
    last_login = Column(DateTime, nullable=True, comment="最后登录时间")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


class DatabaseManager:
    """
    数据库管理器
    负责管理数据库连接、会话创建等
    """
    
    def __init__(self, database_url: str):
        """
        初始化数据库管理器
        
        Args:
            database_url: 数据库连接URL
        """
        self.database_url = database_url
        
        # 创建异步数据库引擎
        # echo=True 会在控制台输出SQL语句，方便调试
        self.engine = create_async_engine(
            database_url,
            echo=True,  # 开发环境建议设为True，生产环境设为False
            pool_pre_ping=True,  # 连接池预检查，确保连接有效
        )
        
        # 创建异步会话工厂
        self.async_session = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False  # 提交后不过期对象
        )
    
    async def create_tables(self):
        """
        创建所有数据库表
        在首次运行应用时调用
        """
        try:
            async with self.engine.begin() as conn:
                # 创建所有继承自Base的表
                await conn.run_sync(Base.metadata.create_all)
            logger.info("数据库表创建成功")
        except Exception as e:
            logger.error(f"创建数据库表失败: {e}")
            raise
    
    async def get_session(self) -> AsyncSession:
        """
        获取数据库会话
        用于执行数据库操作
        
        Returns:
            AsyncSession: 异步数据库会话
        """
        async with self.async_session() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                logger.error(f"数据库会话错误: {e}")
                raise
            finally:
                await session.close()
    
    async def close(self):
        """
        关闭数据库连接
        在应用关闭时调用
        """
        await self.engine.dispose()
        logger.info("数据库连接已关闭")