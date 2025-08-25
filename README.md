# 🚀 Python用户服务API

一个基于FastAPI的现代化用户认证服务，提供完整的用户注册、登录和JWT令牌认证功能。

## ✨ 特性

- 🔐 **安全认证** - JWT令牌 + bcrypt密码加密
- 🚀 **高性能** - FastAPI异步框架 + MySQL异步连接
- 📖 **自动文档** - Swagger UI + ReDoc自动生成
- 🛠️ **工具齐全** - 完整的管理和测试工具集
- 📋 **完整文档** - 详细的使用文档和快速参考

## 🏗️ 技术架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   前端/客户端    │    │   FastAPI服务   │    │   MySQL数据库   │
│                │    │                │    │                │
│  • Apifox      │◄──►│  • 用户注册     │◄──►│  • user_service │
│  • 浏览器      │    │  • 用户登录     │    │  • users表      │
│  • PowerShell  │    │  • JWT认证      │    │  • 加密存储     │
│  • Python脚本  │    │  • API文档      │    │  • 事务支持     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ 技术栈

- **FastAPI 0.116.1** - 现代、快速的Web框架
- **MySQL 8.0+** - 关系型数据库
- **SQLAlchemy 2.0** - 异步ORM框架
- **JWT** - JSON Web Token认证
- **bcrypt** - 密码加密算法
- **Pydantic** - 数据验证和序列化
- **Uvicorn** - ASGI服务器

## 🚀 快速开始

### 1. 环境要求
- Python 3.8+
- MySQL 5.7+
- Git

### 2. 克隆项目
```bash
git clone https://github.com/你的用户名/python-service.git
cd python-service
```

### 3. 创建虚拟环境
```bash
python -m venv python-service
python-service\Scripts\activate  # Windows
# source python-service/bin/activate  # Linux/Mac
```

### 4. 安装依赖
```bash
pip install -r requirements.txt
```

### 5. 配置数据库
复制环境配置文件并修改数据库连接信息：
```bash
cp .env.example .env
# 编辑.env文件，设置数据库密码
```

### 6. 初始化数据库
```bash
python init_db.py
```

### 7. 启动服务
```bash
python -m app.main
```

服务将在 http://localhost:8000 启动

## 📖 API文档

启动服务后，访问以下地址查看API文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 主要接口

### 用户注册
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "用户名",
  "email": "邮箱@example.com",
  "password": "密码123"
}
```

### 用户登录
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "用户名",
  "password": "密码123"
}
```

## 🛠️ 实用工具

### 用户注册工具
```bash
# 交互式用户注册
python simple_register.py

# 注册演示
python register_demo.py
```

### 用户查看工具
```bash
# 快速查看所有用户
python quick_view.py

# 详细用户管理
python view_users.py
```

### 系统检查工具
```bash
# 检查MySQL连接
python check_mysql.py

# MySQL安装指导
python mysql_setup_guide.py
```

## 📋 数据库结构

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME NULL
);
```

## 🔐 安全特性

- ✅ 密码bcrypt加密存储
- ✅ JWT令牌认证
- ✅ 输入数据验证
- ✅ SQL注入防护
- ✅ 密码强度验证

## 📚 文档

- [📖 完整使用文档](./使用文档.md)
- [⚡ 快速参考手册](./快速参考.md)
- [📝 项目总结](./项目总结.md)

## 🧪 测试

### 使用PowerShell测试
```powershell
# 注册用户
$body = @{username="testuser";email="test@example.com";password="test123"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/register" -Method Post -Body $body -ContentType "application/json"

# 用户登录
$loginBody = @{username="testuser";password="test123"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/login" -Method Post -Body $loginBody -ContentType "application/json"
```

### 使用Apifox测试
1. 导入API文档：`http://localhost:8000/openapi.json`
2. 配置环境变量：`base_url = http://localhost:8000`
3. 测试注册和登录接口

## 🚀 部署

### Docker部署
```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 生产环境配置
```bash
# 使用Gunicorn启动
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## 📁 项目结构

```
python-service/
├── app/                     # 核心应用
│   ├── __init__.py         # 包标识
│   ├── main.py             # 应用入口
│   ├── auth.py             # 认证接口
│   ├── database.py         # 数据库模型
│   ├── config.py           # 配置管理
│   ├── schemas.py          # 数据验证
│   ├── security.py         # 安全功能
│   └── crud.py             # 数据操作
├── simple_register.py      # 用户注册工具
├── quick_view.py           # 快速查看用户
├── check_mysql.py          # MySQL检查
├── init_db.py              # 数据库初始化
├── requirements.txt        # 依赖列表
├── .env.example            # 环境配置模板
└── README.md               # 项目说明
```

## 🤝 贡献

欢迎提交Issues和Pull Requests！

## 📄 许可证

本项目采用 [MIT License](LICENSE)

## 🔗 相关链接

- [FastAPI官网](https://fastapi.tiangolo.com/)
- [SQLAlchemy文档](https://docs.sqlalchemy.org/)
- [Pydantic文档](https://pydantic-docs.helpmanual.io/)

---

⭐ 如果这个项目对您有帮助，请给它一个Star！