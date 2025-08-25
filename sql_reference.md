# MySQL查询用户参考手册

## 连接数据库
```bash
mysql -u root -p123456
```

## 基本查询命令

### 1. 选择数据库
```sql
USE user_service;
```

### 2. 查看所有用户
```sql
SELECT id, username, email, is_active, created_at, last_login FROM users;
```

### 3. 查看用户总数
```sql
SELECT COUNT(*) as total_users FROM users;
```

### 4. 查看活跃用户
```sql
SELECT * FROM users WHERE is_active = TRUE;
```

### 5. 按注册时间排序
```sql
SELECT * FROM users ORDER BY created_at DESC;
```

### 6. 查找特定用户
```sql
SELECT * FROM users WHERE username = 'admin';
SELECT * FROM users WHERE email = 'admin@example.com';
SELECT * FROM users WHERE id = 1;
```

### 7. 今日注册用户
```sql
SELECT * FROM users WHERE DATE(created_at) = CURDATE();
```

### 8. 最近登录用户
```sql
SELECT * FROM users WHERE last_login IS NOT NULL ORDER BY last_login DESC LIMIT 5;
```

### 9. 查看表结构
```sql
DESCRIBE users;
```

### 10. 用户活跃度统计
```sql
SELECT 
    COUNT(*) as total,
    SUM(is_active) as active,
    COUNT(*) - SUM(is_active) as inactive
FROM users;
```

## Python脚本命令

### 快速查看所有用户
```bash
python quick_view.py
```

### 详细用户管理
```bash
python view_users.py
```

### 注册新用户
```bash
python simple_register.py
```