"""
用户注册演示脚本
演示如何通过API注册新用户和登录
"""

import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def register_demo_user():
    """注册演示用户"""
    print("🔐 用户注册演示")
    print("=" * 50)
    
    # 注册数据
    user_data = {
        "username": "demo_user",
        "email": "demo@example.com", 
        "password": "demo123456"
    }
    
    print(f"注册用户信息:")
    print(f"用户名: {user_data['username']}")
    print(f"邮箱: {user_data['email']}")
    print(f"密码: {user_data['password']}")
    print()
    
    try:
        print("🔄 正在发送注册请求...")
        response = requests.post(
            f"{API_BASE}/auth/register",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 用户注册成功！")
            print("响应内容:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return True
        else:
            print("❌ 用户注册失败")
            print("错误信息:", response.text)
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API服务")
        print("请确保API服务正在运行: python -m app.main")
        return False
    except Exception as e:
        print(f"❌ 注册过程中发生错误: {e}")
        return False

def login_demo_user():
    """登录演示用户"""
    print("\n🔑 用户登录演示")
    print("=" * 50)
    
    # 登录数据
    login_data = {
        "username": "demo_user",
        "password": "demo123456"
    }
    
    try:
        print("🔄 正在发送登录请求...")
        response = requests.post(
            f"{API_BASE}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 用户登录成功！")
            print("响应内容:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
            # 提取访问令牌
            if "data" in result and "access_token" in result["data"]:
                token = result["data"]["access_token"]
                print(f"\n🎟️  访问令牌: {token[:50]}...")
                return token
            return True
        else:
            print("❌ 用户登录失败")
            print("错误信息:", response.text)
            return False
            
    except Exception as e:
        print(f"❌ 登录过程中发生错误: {e}")
        return False

def test_api_health():
    """测试API健康状态"""
    print("🏥 API健康检查")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            result = response.json()
            print("✅ API服务运行正常")
            print(f"服务名称: {result.get('message', 'N/A')}")
            print(f"版本: {result.get('version', 'N/A')}")
            print(f"状态: {result.get('status', 'N/A')}")
            return True
        else:
            print("❌ API服务异常")
            return False
    except Exception as e:
        print(f"❌ API健康检查失败: {e}")
        return False

def register_custom_user():
    """注册自定义用户"""
    print("\n👤 注册自定义用户")
    print("=" * 50)
    
    print("请输入用户信息:")
    username = input("用户名: ").strip()
    email = input("邮箱: ").strip()
    password = input("密码 (至少8位，包含字母和数字): ").strip()
    
    if not username or not email or not password:
        print("❌ 用户信息不能为空")
        return False
    
    user_data = {
        "username": username,
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/auth/register",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 用户注册成功！")
            print(f"用户ID: {result.get('data', {}).get('user_id', 'N/A')}")
            return True
        else:
            print("❌ 用户注册失败")
            print("错误信息:", response.text)
            return False
            
    except Exception as e:
        print(f"❌ 注册过程中发生错误: {e}")
        return False

def main():
    """主函数"""
    print("🚀 用户服务API - 注册登录演示")
    print("=" * 60)
    
    # 1. 检查API服务
    if not test_api_health():
        print("\n请先启动API服务: python -m app.main")
        return
    
    print("\n选择操作:")
    print("1. 注册演示用户 (demo_user)")
    print("2. 登录演示用户")
    print("3. 注册自定义用户")
    print("4. 全部演示 (注册+登录)")
    
    choice = input("\n请选择 (1-4): ").strip()
    
    if choice == "1":
        register_demo_user()
    elif choice == "2":
        login_demo_user()
    elif choice == "3":
        register_custom_user()
    elif choice == "4":
        # 全部演示
        if register_demo_user():
            login_demo_user()
    else:
        print("❌ 无效选择")
    
    print(f"\n📖 您也可以访问API文档: {BASE_URL}/docs")
    print("在浏览器中测试所有接口！")

if __name__ == "__main__":
    main()