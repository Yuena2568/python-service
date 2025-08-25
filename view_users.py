"""
数据库用户查看脚本
用于查看MySQL数据库中的所有用户信息
"""

import asyncio
import sys
from datetime import datetime
from sqlalchemy import select
from app.config import settings
from app.database import DatabaseManager, User

class UserViewer:
    """用户查看器"""
    
    def __init__(self):
        """初始化数据库管理器"""
        self.db_manager = DatabaseManager(settings.database_url)
    
    async def get_all_users(self):
        """获取所有用户"""
        try:
            async for session in self.db_manager.get_session():
                # 查询所有用户
                query = select(User).order_by(User.id)
                result = await session.execute(query)
                users = result.scalars().all()
                
                return users
        except Exception as e:
            print(f"❌ 获取用户列表失败: {e}")
            return []
    
    async def get_user_by_id(self, user_id):
        """根据ID获取用户"""
        try:
            async for session in self.db_manager.get_session():
                query = select(User).where(User.id == user_id)
                result = await session.execute(query)
                user = result.scalar_one_or_none()
                return user
        except Exception as e:
            print(f"❌ 获取用户失败: {e}")
            return None
    
    async def get_user_by_username(self, username):
        """根据用户名获取用户"""
        try:
            async for session in self.db_manager.get_session():
                query = select(User).where(User.username == username)
                result = await session.execute(query)
                user = result.scalar_one_or_none()
                return user
        except Exception as e:
            print(f"❌ 获取用户失败: {e}")
            return None
    
    def format_datetime(self, dt):
        """格式化日期时间"""
        if dt:
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        return "未记录"
    
    def display_users(self, users):
        """显示用户列表"""
        if not users:
            print("📭 数据库中没有用户")
            return
        
        print(f"\n📊 数据库中共有 {len(users)} 个用户:")
        print("=" * 100)
        print(f"{'ID':<4} {'用户名':<15} {'邮箱':<25} {'状态':<6} {'注册时间':<19} {'最后登录':<19}")
        print("=" * 100)
        
        for user in users:
            status = "✅ 活跃" if user.is_active else "❌ 禁用"
            created_at = self.format_datetime(user.created_at)
            last_login = self.format_datetime(user.last_login)
            
            print(f"{user.id:<4} {user.username:<15} {user.email:<25} {status:<6} {created_at:<19} {last_login:<19}")
    
    def display_user_detail(self, user):
        """显示用户详细信息"""
        if not user:
            print("❌ 用户不存在")
            return
        
        print(f"\n👤 用户详细信息:")
        print("=" * 50)
        print(f"🆔 用户ID: {user.id}")
        print(f"👤 用户名: {user.username}")
        print(f"📧 邮箱: {user.email}")
        print(f"🔒 密码哈希: {user.hashed_password[:50]}...")
        print(f"📊 账户状态: {'✅ 活跃' if user.is_active else '❌ 禁用'}")
        print(f"📅 注册时间: {self.format_datetime(user.created_at)}")
        print(f"🕐 最后登录: {self.format_datetime(user.last_login)}")
    
    async def close(self):
        """关闭数据库连接"""
        await self.db_manager.close()

async def main():
    """主函数"""
    print("🔍 数据库用户查看器")
    print("=" * 50)
    
    # 检查数据库连接
    try:
        viewer = UserViewer()
        
        while True:
            print("\n选择操作:")
            print("1. 查看所有用户")
            print("2. 根据ID查看用户")
            print("3. 根据用户名查看用户")
            print("4. 退出")
            
            choice = input("\n请选择 (1-4): ").strip()
            
            if choice == "1":
                print("\n🔄 正在获取用户列表...")
                users = await viewer.get_all_users()
                viewer.display_users(users)
                
            elif choice == "2":
                user_id = input("请输入用户ID: ").strip()
                try:
                    user_id = int(user_id)
                    user = await viewer.get_user_by_id(user_id)
                    viewer.display_user_detail(user)
                except ValueError:
                    print("❌ 请输入有效的数字ID")
                    
            elif choice == "3":
                username = input("请输入用户名: ").strip()
                if username:
                    user = await viewer.get_user_by_username(username)
                    viewer.display_user_detail(user)
                else:
                    print("❌ 用户名不能为空")
                    
            elif choice == "4":
                print("👋 再见！")
                break
                
            else:
                print("❌ 无效选择，请重新选择")
        
        await viewer.close()
        
    except Exception as e:
        print(f"❌ 程序运行错误: {e}")
        print("请确保:")
        print("1. MySQL服务正在运行")
        print("2. 数据库配置正确")
        print("3. user_service数据库已创建")

if __name__ == "__main__":
    asyncio.run(main())