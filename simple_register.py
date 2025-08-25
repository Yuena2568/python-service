"""
简化用户注册脚本
专门用于注册新用户，提供清晰的指导和错误提示
"""

import requests
import json
import re

BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def validate_email(email):
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """验证密码格式"""
    if len(password) < 8:
        return False, "密码长度至少8个字符"
    
    has_letter = any(c.isalpha() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    if not has_letter:
        return False, "密码必须包含字母"
    if not has_digit:
        return False, "密码必须包含数字"
    
    return True, "密码格式正确"

def register_new_user():
    """注册新用户"""
    print("🎯 用户注册助手")
    print("=" * 50)
    print("密码要求：至少8位，必须包含字母和数字")
    print("用户名要求：3-50个字符，只能包含字母、数字、下划线")
    print("=" * 50)
    
    # 获取用户输入
    while True:
        username = input("\n请输入用户名: ").strip()
        if not username:
            print("❌ 用户名不能为空")
            continue
        if len(username) < 3 or len(username) > 50:
            print("❌ 用户名长度必须在3-50个字符之间")
            continue
        if not username.replace('_', '').isalnum():
            print("❌ 用户名只能包含字母、数字和下划线")
            continue
        break
    
    while True:
        email = input("请输入邮箱: ").strip()
        if not email:
            print("❌ 邮箱不能为空")
            continue
        if not validate_email(email):
            print("❌ 邮箱格式不正确，请输入有效的邮箱地址")
            continue
        break
    
    while True:
        password = input("请输入密码: ").strip()
        if not password:
            print("❌ 密码不能为空")
            continue
        
        is_valid, message = validate_password(password)
        if not is_valid:
            print(f"❌ {message}")
            continue
        break
    
    # 准备注册数据
    user_data = {
        "username": username,
        "email": email,
        "password": password
    }
    
    print(f"\n📋 注册信息确认:")
    print(f"用户名: {username}")
    print(f"邮箱: {email}")
    print(f"密码: {'*' * len(password)}")
    
    confirm = input("\n确认注册？(y/n): ").lower().strip()
    if confirm not in ['y', 'yes', '是']:
        print("❌ 注册已取消")
        return False
    
    # 发送注册请求
    try:
        print("\n🔄 正在注册...")
        response = requests.post(
            f"{API_BASE}/auth/register",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("🎉 用户注册成功！")
            print(f"✅ 用户ID: {result.get('data', {}).get('user_id', 'N/A')}")
            print(f"✅ 用户名: {username}")
            print(f"✅ 邮箱: {email}")
            
            # 询问是否立即登录
            login_now = input("\n是否立即登录测试？(y/n): ").lower().strip()
            if login_now in ['y', 'yes', '是']:
                test_login(username, password)
            
            return True
            
        else:
            print("❌ 用户注册失败")
            try:
                error_detail = response.json()
                if "detail" in error_detail:
                    if isinstance(error_detail["detail"], list):
                        for error in error_detail["detail"]:
                            if "msg" in error:
                                print(f"错误信息: {error['msg']}")
                    else:
                        print(f"错误信息: {error_detail['detail']}")
                else:
                    print(f"错误信息: {error_detail}")
            except:
                print(f"错误信息: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API服务")
        print("请确保API服务正在运行: python -m app.main")
        return False
    except Exception as e:
        print(f"❌ 注册过程中发生错误: {e}")
        return False

def test_login(username, password):
    """测试登录"""
    print(f"\n🔐 测试登录用户: {username}")
    print("=" * 30)
    
    login_data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 登录成功！")
            print("🎟️  已获取访问令牌")
            if "data" in result and "user" in result["data"]:
                user_info = result["data"]["user"]
                print(f"👤 用户信息:")
                print(f"   - ID: {user_info.get('id')}")
                print(f"   - 用户名: {user_info.get('username')}")
                print(f"   - 邮箱: {user_info.get('email')}")
                print(f"   - 注册时间: {user_info.get('created_at', '').split('T')[0] if user_info.get('created_at') else 'N/A'}")
        else:
            print("❌ 登录失败")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 登录测试失败: {e}")

def main():
    """主函数"""
    print("🚀 用户注册系统")
    print("📖 API文档: http://localhost:8000/docs")
    print()
    
    # 检查API服务状态
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print("❌ API服务未正常运行，请先启动服务")
            print("启动命令: python -m app.main")
            return
    except:
        print("❌ 无法连接到API服务，请先启动服务")
        print("启动命令: python -m app.main")
        return
    
    register_new_user()

if __name__ == "__main__":
    main()