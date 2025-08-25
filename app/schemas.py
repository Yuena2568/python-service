"""
用户数据模型
定义API请求和响应的数据结构，使用Pydantic进行数据验证
"""

from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """
    用户基础模型
    包含用户的基本信息字段
    """
    username: str
    email: EmailStr
    
    @validator('username')
    def validate_username(cls, v):
        """
        验证用户名格式
        - 长度3-50个字符
        - 只能包含字母、数字、下划线
        """
        if len(v) < 3 or len(v) > 50:
            raise ValueError('用户名长度必须在3-50个字符之间')
        
        if not v.replace('_', '').isalnum():
            raise ValueError('用户名只能包含字母、数字和下划线')
        
        return v


class UserCreate(UserBase):
    """
    用户创建模型
    用于用户注册时的数据验证
    """
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        """
        验证密码强度
        - 长度至少8个字符
        - 包含字母和数字
        """
        if len(v) < 8:
            raise ValueError('密码长度至少8个字符')
        
        has_letter = any(c.isalpha() for c in v)
        has_digit = any(c.isdigit() for c in v)
        
        if not (has_letter and has_digit):
            raise ValueError('密码必须包含字母和数字')
        
        return v


class UserLogin(BaseModel):
    """
    用户登录模型
    用于用户登录时的数据验证
    """
    username: str
    password: str


class UserResponse(UserBase):
    """
    用户响应模型
    用于API返回用户信息（不包含密码）
    """
    id: int
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        # 允许从ORM模型创建Pydantic模型
        from_attributes = True


class UserInDB(UserResponse):
    """
    数据库中的用户模型
    包含加密后的密码，仅用于内部处理
    """
    hashed_password: str


class Token(BaseModel):
    """
    JWT令牌模型
    用于登录成功后返回令牌信息
    """
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """
    令牌数据模型
    用于解析JWT令牌中的用户信息
    """
    username: Optional[str] = None


class APIResponse(BaseModel):
    """
    API统一响应模型
    用于包装所有API响应，提供统一的响应格式
    """
    success: bool = True
    message: str = "操作成功"
    data: Optional[dict] = None
    
    @classmethod
    def success_response(cls, message: str = "操作成功", data: Optional[dict] = None):
        """
        创建成功响应
        
        Args:
            message: 响应消息
            data: 响应数据
            
        Returns:
            APIResponse: 成功响应实例
        """
        return cls(success=True, message=message, data=data)
    
    @classmethod
    def error_response(cls, message: str = "操作失败"):
        """
        创建错误响应
        
        Args:
            message: 错误消息
            
        Returns:
            APIResponse: 错误响应实例
        """
        return cls(success=False, message=message, data=None)