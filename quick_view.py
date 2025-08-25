"""
快速查看数据库用户脚本
一键显示所有用户信息
"""

import asyncio
from sqlalchemy import select
from app.config import settings
from app.database import DatabaseManager, User

async def quick_view_users():
    """快速查看所有用户"""
    print("🔍 数据库用户快速查看")
    print("=" * 60)
    
    try:
        # 创建数据库管理器
        db_manager = DatabaseManager(settings.database_url)
        
        # 获取用户数据
        async for session in db_manager.get_session():
            query = select(User).order_by(User.id)
            result = await session.execute(query)
            users = result.scalars().all()
            
            if not users:
                print("📭 数据库中没有用户")
            else:
                print(f"📊 共找到 {len(users)} 个用户:\n")
                
                for i, user in enumerate(users, 1):
                    print(f"👤 用户 {i}:")
                    print(f"   🆔 ID: {user.id}")
                    print(f"   👤 用户名: {user.username}")
                    print(f"   📧 邮箱: {user.email}")
                    print(f"   📊 状态: {'✅ 活跃' if user.is_active else '❌ 禁用'}")
                    
                    # 格式化时间
                    created_at = user.created_at.strftime("%Y-%m-%d %H:%M:%S") if user.created_at else "未知"
                    last_login = user.last_login.strftime("%Y-%m-%d %H:%M:%S") if user.last_login else "从未登录"
                    
                    print(f"   📅 注册时间: {created_at}")
                    print(f"   🕐 最后登录: {last_login}")
                    print()
        
        # 关闭数据库连接
        await db_manager.close()
        
    except Exception as e:
        print(f"❌ 查看用户失败: {e}")
        print("请确保:")
        print("1. MySQL服务正在运行")
        print("2. 数据库连接配置正确")
        print("3. user_service数据库存在")

async def count_users():
    """统计用户数量"""
    print("📊 用户统计信息")
    print("=" * 30)
    
    try:
        db_manager = DatabaseManager(settings.database_url)
        
        async for session in db_manager.get_session():
            # 总用户数
            total_query = select(User)
            total_result = await session.execute(total_query)
            total_users = len(total_result.scalars().all())
            
            # 活跃用户数
            active_query = select(User).where(User.is_active == True)
            active_result = await session.execute(active_query)
            active_users = len(active_result.scalars().all())
            
            # 今日注册用户
            from datetime import datetime, date
            today = date.today()
            today_query = select(User).where(User.created_at >= today)
            today_result = await session.execute(today_query)
            today_users = len(today_result.scalars().all())
            
            print(f"👥 总用户数: {total_users}")
            print(f"✅ 活跃用户: {active_users}")
            print(f"❌ 禁用用户: {total_users - active_users}")
            print(f"🆕 今日注册: {today_users}")
        
        await db_manager.close()
        
    except Exception as e:
        print(f"❌ 统计失败: {e}")

if __name__ == "__main__":
    print("选择操作:")
    print("1. 查看所有用户详情")
    print("2. 查看用户统计")
    
    choice = input("请选择 (1/2): ").strip()
    
    if choice == "1":
        asyncio.run(quick_view_users())
    elif choice == "2":
        asyncio.run(count_users())
    else:
        print("默认显示所有用户:")
        asyncio.run(quick_view_users())