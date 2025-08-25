"""
安全认证模块
实现密码加密、JWT令牌生成和验证等安全功能
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.config import settings
from app.schemas import TokenData

# 创建密码加密上下文
# 使用bcrypt算法进行密码哈希
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SecurityManager:
    """
    安全管理器
    负责密码加密、JWT令牌生成和验证
    """
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        加密密码
        
        Args:
            password: 原始密码
            
        Returns:
            str: 加密后的密码哈希
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        验证密码
        
        Args:
            plain_password: 用户输入的原始密码
            hashed_password: 数据库中存储的加密密码
            
        Returns:
            bool: 密码是否正确
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        创建JWT访问令牌
        
        Args:
            data: 要编码到令牌中的数据
            expires_delta: 令牌过期时间（可选）
            
        Returns:
            str: JWT令牌字符串
        """
        # 复制数据，避免修改原始数据
        to_encode = data.copy()
        
        # 设置过期时间
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            # 使用配置中的默认过期时间
            expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        
        # 添加过期时间到令牌数据中
        to_encode.update({"exp": expire})
        
        # 生成JWT令牌
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> TokenData:
        """
        验证JWT令牌
        
        Args:
            token: JWT令牌字符串
            
        Returns:
            TokenData: 解析出的令牌数据
            
        Raises:
            HTTPException: 令牌无效时抛出异常
        """
        # 定义认证异常
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无法验证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            # 解码JWT令牌
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            
            # 获取用户名
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            
            # 创建令牌数据对象
            token_data = TokenData(username=username)
            return token_data
            
        except JWTError:
            raise credentials_exception
    
    @staticmethod
    def create_token_for_user(username: str) -> str:
        """
        为用户创建访问令牌
        
        Args:
            username: 用户名
            
        Returns:
            str: JWT令牌字符串
        """
        # 设置令牌过期时间
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        
        # 创建令牌
        access_token = SecurityManager.create_access_token(
            data={"sub": username}, 
            expires_delta=access_token_expires
        )
        
        return access_token


# 创建全局安全管理器实例
security_manager = SecurityManager()