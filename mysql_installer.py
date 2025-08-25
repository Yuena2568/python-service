"""
MySQL 8.0 自动化安装指南
此脚本将帮助您完成MySQL的下载和安装配置
"""

import os
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

class MySQLInstaller:
    def __init__(self):
        self.mysql_version = "8.0.35"
        self.download_url = f"https://dev.mysql.com/get/mysql-{self.mysql_version}-winx64.zip"
        self.install_path = "C:\\mysql"
        self.data_path = "C:\\mysql\\data"
        
    def download_mysql(self):
        """下载MySQL安装包"""
        print("🔄 开始下载MySQL...")
        print("由于网络限制，建议您手动下载MySQL")
        print(f"下载地址: {self.download_url}")
        print("或访问: https://dev.mysql.com/downloads/mysql/")
        print("选择: Windows (x86, 64-bit), ZIP Archive")
        
    def manual_installation_guide(self):
        """手动安装指南"""
        print("\n" + "="*60)
        print("📋 MySQL 手动安装指南")
        print("="*60)
        
        steps = [
            "1. 访问 https://dev.mysql.com/downloads/mysql/",
            "2. 选择 'Windows (x86, 64-bit), ZIP Archive'",
            "3. 点击 'Download' (可以选择 'No thanks, just start my download')",
            "4. 下载完成后，解压到 C:\\mysql 目录",
            "5. 创建 C:\\mysql\\data 目录",
            "6. 配置MySQL环境变量",
            "7. 初始化MySQL数据库",
            "8. 安装MySQL服务",
            "9. 启动MySQL服务",
            "10. 设置root密码"
        ]
        
        for step in steps:
            print(f"   {step}")
            
        print("\n" + "="*60)
        return True
    
    def create_mysql_config(self):
        """创建MySQL配置文件"""
        config_content = """[mysqld]
# 设置3306端口
port=3306
# 设置mysql的安装目录
basedir=C:\\mysql
# 设置mysql数据库的数据的存放目录
datadir=C:\\mysql\\data
# 允许最大连接数
max_connections=200
# 允许连接失败的次数
max_connect_errors=10
# 服务端使用的字符集默认为UTF8
character-set-server=utf8mb4
# 创建新表时将使用的默认存储引擎
default-storage-engine=INNODB
# 默认使用"mysql_native_password"插件认证
default_authentication_plugin=mysql_native_password

[mysql]
# 设置mysql客户端默认字符集
default-character-set=utf8mb4

[client]
# 设置mysql客户端连接服务端时默认使用的端口
port=3306
default-character-set=utf8mb4
"""
        
        config_path = "mysql_config.ini"
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print(f"✅ MySQL配置文件已创建: {config_path}")
        return config_path
    
    def create_installation_batch(self):
        """创建安装批处理文件"""
        batch_content = """@echo off
echo 正在配置MySQL...

REM 创建MySQL目录
if not exist "C:\\mysql" mkdir "C:\\mysql"
if not exist "C:\\mysql\\data" mkdir "C:\\mysql\\data"

echo ✅ MySQL目录创建完成

REM 提示用户解压MySQL
echo 📁 请将下载的MySQL ZIP文件解压到 C:\\mysql 目录
echo 解压后的结构应该是: C:\\mysql\\bin, C:\\mysql\\lib 等
pause

REM 添加环境变量
echo 📝 添加MySQL到环境变量...
setx PATH "%PATH%;C:\\mysql\\bin" /M

REM 初始化MySQL
echo 🔧 初始化MySQL数据库...
cd /d C:\\mysql\\bin
mysqld --initialize --console

echo ⚠️  请记住上面显示的临时root密码！
pause

REM 安装MySQL服务
echo 🔧 安装MySQL服务...
mysqld install MySQL

echo 🚀 启动MySQL服务...
net start MySQL

echo ✅ MySQL安装完成！
echo 现在您可以使用临时密码登录并设置新密码
echo 命令: mysql -u root -p
pause
"""
        
        batch_path = "install_mysql.bat"
        with open(batch_path, 'w', encoding='gbk') as f:
            f.write(batch_content)
        
        print(f"✅ 安装批处理文件已创建: {batch_path}")
        return batch_path

def main():
    """主函数"""
    installer = MySQLInstaller()
    
    print("🚀 MySQL安装助手")
    print("=" * 50)
    
    # 显示手动安装指南
    installer.manual_installation_guide()
    
    # 创建配置文件
    installer.create_mysql_config()
    
    # 创建安装批处理文件
    installer.create_installation_batch()
    
    print("\n📋 下一步操作:")
    print("1. 手动下载MySQL ZIP文件")
    print("2. 以管理员身份运行 install_mysql.bat")
    print("3. 按照批处理文件的提示操作")
    print("4. 记住临时密码并设置新密码")
    
    return True

if __name__ == "__main__":
    main()