"""
用户认证API路由
实现用户注册、登录等认证相关的API接口
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DatabaseManager
from app.config import settings
from app.schemas import UserCreate, UserLogin, UserResponse, Token, APIResponse
from app.crud import user_crud
from app.security import security_manager

# 创建路由器
router = APIRouter(prefix="/auth", tags=["认证"])

# 创建数据库管理器实例
db_manager = DatabaseManager(settings.database_url)


async def get_db():
    """
    获取数据库会话依赖
    """
    async for session in db_manager.get_session():
        yield session


@router.post("/register", response_model=APIResponse, summary="用户注册")
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    用户注册接口
    
    Args:
        user_data: 用户注册数据（用户名、邮箱、密码）
        db: 数据库会话
        
    Returns:
        APIResponse: 注册结果
        
    Raises:
        HTTPException: 用户名或邮箱已存在时抛出异常
    """
    try:
        # 检查用户名是否已存在
        existing_user = await user_crud.get_user_by_username(db, user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        
        # 检查邮箱是否已存在
        existing_email = await user_crud.get_user_by_email(db, user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被注册"
            )
        
        # 创建用户
        new_user = await user_crud.create_user(db, user_data)
        if not new_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="用户创建失败"
            )
        
        # 创建用户响应数据
        user_response = UserResponse.from_orm(new_user)
        
        return APIResponse.success_response(
            message="用户注册成功",
            data={
                "user": user_response.dict(),
                "user_id": new_user.id
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"注册过程中发生错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="注册过程中发生错误"
        )


@router.post("/login", response_model=dict, summary="用户登录")
async def login_user(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    用户登录接口
    
    Args:
        login_data: 用户登录数据（用户名、密码）
        db: 数据库会话
        
    Returns:
        dict: 登录结果，包含访问令牌和用户信息
        
    Raises:
        HTTPException: 用户名或密码错误时抛出异常
    """
    try:
        # 验证用户登录
        user = await user_crud.authenticate_user(db, login_data.username, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 检查用户是否被禁用
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户账户已被禁用"
            )
        
        # 创建访问令牌
        access_token = security_manager.create_token_for_user(user.username)
        
        # 创建用户响应数据
        user_response = UserResponse.from_orm(user)
        
        return {
            "success": True,
            "message": "登录成功",
            "data": {
                "access_token": access_token,
                "token_type": "bearer",
                "user": user_response.dict()
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"登录过程中发生错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="登录过程中发生错误"
        )


@router.get("/me", response_model=UserResponse, summary="获取当前用户信息")
async def get_current_user_info(
    db: AsyncSession = Depends(get_db),
    # 这里我们先简化，后面会添加认证依赖
):
    """
    获取当前登录用户信息接口
    
    Args:
        db: 数据库会话
        
    Returns:
        UserResponse: 当前用户信息
    """
    # 这是一个示例接口，实际使用时需要添加JWT认证
    # 目前先返回一个示例响应
    return {
        "message": "此接口需要在完成JWT认证后实现"
    }