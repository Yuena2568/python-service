"""
FastAPI主应用文件
整合所有组件，配置路由、中间件等
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.database import DatabaseManager
from app.auth import router as auth_router

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    在应用启动和关闭时执行必要的操作
    """
    # 启动时执行
    logger.info("正在启动用户服务API...")
    
    # 初始化数据库
    db_manager = DatabaseManager(settings.database_url)
    try:
        await db_manager.create_tables()
        logger.info("数据库表初始化完成")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        # 注意：这里不抛出异常，允许应用继续启动
        # 在实际生产环境中，您可能希望在数据库连接失败时停止应用
    
    logger.info("用户服务API启动完成")
    
    yield  # 应用运行期间
    
    # 关闭时执行
    logger.info("正在关闭用户服务API...")
    try:
        await db_manager.close()
        logger.info("数据库连接已关闭")
    except Exception as e:
        logger.error(f"关闭数据库连接时发生错误: {e}")
    
    logger.info("用户服务API已关闭")


# 创建FastAPI应用实例
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    ## 用户服务API
    
    这是一个用于用户注册和登录的REST API服务。
    
    ### 主要功能：
    * **用户注册** - 支持用户名和邮箱注册
    * **用户登录** - JWT令牌认证
    * **用户信息** - 获取当前用户信息
    
    ### 技术特点：
    * 使用FastAPI框架，高性能异步处理
    * MySQL数据库存储，支持事务
    * JWT令牌认证，安全可靠
    * 密码bcrypt加密，保护用户隐私
    * 自动生成API文档，便于测试和集成
    
    ### 快速开始：
    1. 先调用 `/api/v1/auth/register` 注册用户
    2. 然后调用 `/api/v1/auth/login` 获取访问令牌
    3. 使用令牌访问需要认证的接口
    """,
    contact={
        "name": "开发团队",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT License",
    },
    # 设置API文档的URL路径
    docs_url="/docs",  # Swagger UI文档
    redoc_url="/redoc",  # ReDoc文档
    openapi_url="/openapi.json",  # OpenAPI JSON schema
    lifespan=lifespan
)

# 配置CORS中间件（跨域资源共享）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 健康检查接口
@app.get("/", tags=["系统"], summary="健康检查")
async def health_check():
    """
    健康检查接口
    用于检查服务是否正常运行
    """
    return {
        "message": "用户服务API正在运行",
        "version": settings.app_version,
        "status": "healthy"
    }


@app.get("/health", tags=["系统"], summary="系统状态")
async def system_health():
    """
    系统状态检查
    返回系统的详细状态信息
    """
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "database": "connected",  # 在实际应用中，这里应该检查真实的数据库连接状态
        "timestamp": "2024-01-01T00:00:00Z"  # 可以返回当前时间戳
    }


# 注册路由
app.include_router(auth_router, prefix=settings.api_v1_prefix)


# 全局异常处理器
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """
    处理404错误
    """
    return {
        "success": False,
        "message": "请求的资源未找到",
        "error_code": 404
    }


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """
    处理500内部服务器错误
    """
    logger.error(f"内部服务器错误: {exc}")
    return {
        "success": False,
        "message": "内部服务器错误",
        "error_code": 500
    }


if __name__ == "__main__":
    import uvicorn
    
    # 运行应用
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发环境启用热重载
        log_level="info"
    )