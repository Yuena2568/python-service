"""
API测试脚本
用于测试用户注册和登录功能
"""

import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def test_health_check():
    """测试健康检查接口"""
    print("=" * 50)
    print("测试健康检查接口")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"请求失败: {e}")
        return False

def test_user_register():
    """测试用户注册接口"""
    print("=" * 50)
    print("测试用户注册接口")
    print("=" * 50)
    
    # 测试数据
    user_data = {
        "username": "testuser123",
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/auth/register",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"请求失败: {e}")
        return False

def test_user_login():
    """测试用户登录接口"""
    print("=" * 50)
    print("测试用户登录接口")
    print("=" * 50)
    
    # 登录数据
    login_data = {
        "username": "testuser123",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        if response.status_code == 200:
            # 保存令牌以供后续使用
            data = response.json()
            if "data" in data and "access_token" in data["data"]:
                return data["data"]["access_token"]
        
        return None
        
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def main():
    """主测试函数"""
    print("开始API功能测试")
    print("请确保:")
    print("1. FastAPI服务正在运行 (python -m app.main)")
    print("2. MySQL服务已启动并配置正确")
    print()
    
    # 测试健康检查
    if not test_health_check():
        print("❌ 健康检查失败，请检查服务是否启动")
        return
    
    print("✅ 健康检查通过")
    
    # 测试用户注册
    if test_user_register():
        print("✅ 用户注册测试通过")
        
        # 测试用户登录
        token = test_user_login()
        if token:
            print("✅ 用户登录测试通过")
            print(f"获取到访问令牌: {token[:20]}...")
        else:
            print("❌ 用户登录测试失败")
    else:
        print("❌ 用户注册测试失败")
        print("这可能是因为:")
        print("- MySQL数据库未启动")
        print("- 数据库连接配置错误")
        print("- 用户名或邮箱已存在")

if __name__ == "__main__":
    main()