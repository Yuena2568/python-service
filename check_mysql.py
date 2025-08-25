"""
MySQL安装检查脚本
帮助检查MySQL是否正确安装和配置
"""

import subprocess
import sys
import os
from app.config import settings

def check_mysql_service():
    """检查MySQL服务是否运行"""
    print("🔍 检查MySQL服务状态...")
    try:
        # Windows下检查MySQL服务
        result = subprocess.run(['sc', 'query', 'MySQL80'], 
                              capture_output=True, text=True)
        if 'RUNNING' in result.stdout:
            print("✅ MySQL服务正在运行")
            return True
        else:
            print("❌ MySQL服务未运行")
            print("请启动MySQL服务：")
            print("1. 按 Win+R，输入 services.msc")
            print("2. 找到MySQL80服务，右键启动")
            return False
    except Exception as e:
        print(f"❌ 检查MySQL服务失败: {e}")
        return False

def check_mysql_connection():
    """检查MySQL连接"""
    print("🔍 检查MySQL连接...")
    try:
        import aiomysql
        import asyncio
        
        async def test_connection():
            try:
                connection = await aiomysql.connect(
                    host=settings.db_host,
                    port=settings.db_port,
                    user=settings.db_user,
                    password=settings.db_password,
                )
                await connection.ensure_closed()
                return True
            except Exception as e:
                print(f"❌ 数据库连接失败: {e}")
                return False
        
        result = asyncio.run(test_connection())
        if result:
            print("✅ MySQL连接成功")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
        return False

def check_env_config():
    """检查环境配置"""
    print("🔍 检查环境配置...")
    
    if not settings.db_password or settings.db_password == "请在这里输入您安装MySQL时设置的root密码":
        print("❌ 请在 .env 文件中设置正确的数据库密码")
        print(f"当前配置的密码: {settings.db_password}")
        print("请编辑 .env 文件，将 DB_PASSWORD 设置为您的MySQL root密码")
        return False
    
    print("✅ 环境配置检查通过")
    print(f"数据库主机: {settings.db_host}")
    print(f"数据库端口: {settings.db_port}")
    print(f"数据库用户: {settings.db_user}")
    print(f"数据库名称: {settings.db_name}")
    return True

def main():
    """主检查函数"""
    print("=" * 60)
    print("🚀 MySQL安装和配置检查工具")
    print("=" * 60)
    
    # 检查环境配置
    if not check_env_config():
        return
    
    # 检查MySQL服务
    if not check_mysql_service():
        return
    
    # 检查MySQL连接
    if check_mysql_connection():
        print("=" * 60)
        print("🎉 恭喜！MySQL配置正确，可以继续使用项目了")
        print("下一步可以运行：python init_db.py")
        print("=" * 60)
    else:
        print("=" * 60)
        print("❌ MySQL连接失败，请检查：")
        print("1. MySQL服务是否启动")
        print("2. .env文件中的密码是否正确")
        print("3. 用户名和端口是否正确")
        print("=" * 60)

if __name__ == "__main__":
    main()