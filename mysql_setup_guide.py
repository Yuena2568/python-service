"""
MySQL安装状态检查和指导工具
帮助检查MySQL安装状态并提供详细的安装指导
"""

import subprocess
import webbrowser
import os
import sys

def check_mysql_installation():
    """检查MySQL是否已安装"""
    print("🔍 检查MySQL安装状态...")
    
    # 检查MySQL命令是否可用
    try:
        result = subprocess.run(['mysql', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ MySQL命令行工具已安装")
            print(f"版本信息: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        print("❌ MySQL命令行工具未找到")
    
    # 检查MySQL服务
    try:
        result = subprocess.run(['sc', 'query', 'MySQL80'], 
                              capture_output=True, text=True)
        if 'SERVICE_NAME' in result.stdout:
            print("✅ MySQL服务已安装")
            if 'RUNNING' in result.stdout:
                print("✅ MySQL服务正在运行")
                return True
            else:
                print("⚠️  MySQL服务已安装但未运行")
                print("尝试启动服务...")
                start_result = subprocess.run(['net', 'start', 'MySQL'], 
                                            capture_output=True, text=True)
                if start_result.returncode == 0:
                    print("✅ MySQL服务启动成功")
                    return True
                else:
                    print("❌ MySQL服务启动失败")
                    return False
    except Exception as e:
        print(f"❌ 检查MySQL服务时出错: {e}")
    
    return False

def provide_installation_guide():
    """提供安装指导"""
    print("\n" + "="*60)
    print("📋 MySQL 8.0 安装指导")
    print("="*60)
    
    print("""
🌟 推荐安装方法：

1️⃣  访问MySQL官网下载页面
   https://dev.mysql.com/downloads/installer/

2️⃣  选择安装包
   - 下载 "mysql-installer-community-8.x.x.x.msi"
   - 大小约 2MB (会在线下载所需组件)

3️⃣  安装配置
   - 双击运行下载的 .msi 文件
   - 选择 "Server only" 安装类型
   - 保持默认端口 3306
   - 设置 root 密码为: 123456
   - 勾选 "Start the MySQL Server at System Startup"

4️⃣  验证安装
   - 安装完成后，运行此脚本再次检查
   - 或者在命令行输入: mysql -u root -p

⚠️  重要提示：
   - 记住设置的root密码 (建议: 123456)
   - 安装过程中选择"Use Strong Password Encryption"
   - 确保端口3306没有被其他程序占用
""")

def open_download_page():
    """打开MySQL下载页面"""
    try:
        print("🌐 正在打开MySQL官方下载页面...")
        webbrowser.open("https://dev.mysql.com/downloads/installer/")
        print("✅ 已在浏览器中打开下载页面")
        return True
    except Exception as e:
        print(f"❌ 无法打开浏览器: {e}")
        print("请手动访问: https://dev.mysql.com/downloads/installer/")
        return False

def create_post_installation_guide():
    """创建安装后配置指南"""
    guide_content = """
# MySQL安装后配置指南

## 安装完成后的验证步骤

1. **检查服务状态**
   - 按 Win+R，输入 `services.msc`
   - 找到 "MySQL80" 服务，确保状态为"正在运行"

2. **测试连接**
   - 按 Win+R，输入 `cmd`
   - 输入: `mysql -u root -p`
   - 输入密码: 123456
   - 如果能进入MySQL命令行，说明安装成功

3. **创建项目数据库**
   在MySQL命令行中执行:
   ```sql
   CREATE DATABASE user_service CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   SHOW DATABASES;
   EXIT;
   ```

4. **运行项目检查**
   ```bash
   python check_mysql.py
   ```

## 常见问题解决

### 问题1: MySQL服务无法启动
- 检查端口3306是否被占用
- 以管理员身份运行命令: `net start MySQL`

### 问题2: 密码错误
- 确认密码是否为 123456
- 如需重置密码，参考 mysql_password_reset.md

### 问题3: 连接被拒绝
- 检查防火墙设置
- 确认MySQL服务正在运行
"""
    
    with open("mysql_post_install_guide.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    
    print("✅ 已创建安装后配置指南: mysql_post_install_guide.md")

def main():
    """主函数"""
    print("🚀 MySQL安装检查工具")
    print("="*50)
    
    # 检查MySQL安装状态
    if check_mysql_installation():
        print("\n🎉 MySQL已正确安装并运行！")
        print("您可以继续使用项目了。")
        
        # 运行项目检查
        print("\n运行项目数据库检查...")
        os.system("python check_mysql.py")
        
    else:
        print("\n❌ MySQL未安装或未正确配置")
        provide_installation_guide()
        
        # 询问是否打开下载页面
        while True:
            choice = input("\n是否现在打开MySQL下载页面？ (y/n): ").lower().strip()
            if choice in ['y', 'yes', '是']:
                open_download_page()
                break
            elif choice in ['n', 'no', '否']:
                print("请手动访问: https://dev.mysql.com/downloads/installer/")
                break
            else:
                print("请输入 y 或 n")
        
        # 创建安装后指南
        create_post_installation_guide()
        
        print("\n📋 下一步:")
        print("1. 下载并安装MySQL")
        print("2. 安装完成后再次运行此脚本: python mysql_setup_guide.py")
        print("3. 或者运行检查脚本: python check_mysql.py")

if __name__ == "__main__":
    main()