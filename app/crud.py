"""
数据库操作模块 (CRUD)
实现用户相关的数据库增删改查操作
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from typing import Optional
from datetime import datetime

from app.database import User
from app.schemas import UserCreate, UserInDB
from app.security import security_manager


class UserCRUD:
    """
    用户数据库操作类
    实现用户相关的所有数据库操作
    """
    
    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """
        根据用户名获取用户
        
        Args:
            db: 数据库会话
            username: 用户名
            
        Returns:
            Optional[User]: 用户对象，如果不存在则返回None
        """
        try:
            # 构建查询语句
            query = select(User).where(User.username == username)
            result = await db.execute(query)
            user = result.scalar_one_or_none()
            return user
        except Exception as e:
            print(f"获取用户失败: {e}")
            return None
    
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """
        根据邮箱获取用户
        
        Args:
            db: 数据库会话
            email: 邮箱地址
            
        Returns:
            Optional[User]: 用户对象，如果不存在则返回None
        """
        try:
            query = select(User).where(User.email == email)
            result = await db.execute(query)
            user = result.scalar_one_or_none()
            return user
        except Exception as e:
            print(f"获取用户失败: {e}")
            return None
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """
        根据用户ID获取用户
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            
        Returns:
            Optional[User]: 用户对象，如果不存在则返回None
        """
        try:
            query = select(User).where(User.id == user_id)
            result = await db.execute(query)
            user = result.scalar_one_or_none()
            return user
        except Exception as e:
            print(f"获取用户失败: {e}")
            return None
    
    @staticmethod
    async def create_user(db: AsyncSession, user_create: UserCreate) -> Optional[User]:
        """
        创建新用户
        
        Args:
            db: 数据库会话
            user_create: 用户创建数据
            
        Returns:
            Optional[User]: 创建的用户对象，如果失败则返回None
        """
        try:
            # 加密密码
            hashed_password = security_manager.hash_password(user_create.password)
            
            # 创建用户对象
            db_user = User(
                username=user_create.username,
                email=user_create.email,
                hashed_password=hashed_password,
                is_active=True,
                created_at=datetime.utcnow()
            )
            
            # 添加到数据库
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)
            
            return db_user
            
        except IntegrityError as e:
            # 处理唯一约束违反错误（用户名或邮箱已存在）
            await db.rollback()
            print(f"用户创建失败，可能是用户名或邮箱已存在: {e}")
            return None
        except Exception as e:
            await db.rollback()
            print(f"用户创建失败: {e}")
            return None
    
    @staticmethod
    async def authenticate_user(db: AsyncSession, username: str, password: str) -> Optional[User]:
        """
        验证用户登录
        
        Args:
            db: 数据库会话
            username: 用户名
            password: 密码
            
        Returns:
            Optional[User]: 验证成功返回用户对象，否则返回None
        """
        try:
            # 获取用户
            user = await UserCRUD.get_user_by_username(db, username)
            if not user:
                return None
            
            # 验证密码
            if not security_manager.verify_password(password, user.hashed_password):
                return None
            
            # 更新最后登录时间
            user.last_login = datetime.utcnow()
            await db.commit()
            
            return user
            
        except Exception as e:
            print(f"用户认证失败: {e}")
            return None
    
    @staticmethod
    async def update_user_last_login(db: AsyncSession, user_id: int) -> bool:
        """
        更新用户最后登录时间
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            
        Returns:
            bool: 更新是否成功
        """
        try:
            user = await UserCRUD.get_user_by_id(db, user_id)
            if user:
                user.last_login = datetime.utcnow()
                await db.commit()
                return True
            return False
        except Exception as e:
            await db.rollback()
            print(f"更新登录时间失败: {e}")
            return False


# 创建全局CRUD实例
user_crud = UserCRUD()