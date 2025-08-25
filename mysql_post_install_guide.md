
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
