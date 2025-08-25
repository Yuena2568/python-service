# MySQL密码重置指南

## 方法一：使用MySQL Workbench重置密码

1. 打开MySQL Workbench
2. 点击"重置密码"或"Reset Password"
3. 输入新密码

## 方法二：使用命令行重置密码

1. 停止MySQL服务：
   ```
   net stop MySQL80
   ```

2. 以跳过权限验证模式启动MySQL：
   ```
   mysqld --skip-grant-tables
   ```

3. 打开新的命令行窗口，连接MySQL：
   ```
   mysql -u root
   ```

4. 重置密码：
   ```sql
   USE mysql;
   UPDATE user SET authentication_string=PASSWORD('您的新密码') WHERE User='root';
   FLUSH PRIVILEGES;
   EXIT;
   ```

5. 重启MySQL服务：
   ```
   net start MySQL80
   ```

## 方法三：重新安装MySQL（最简单）

如果上述方法太复杂，可以：
1. 卸载MySQL
2. 重新安装
3. 在安装过程中设置新密码

## 安装MySQL的建议密码

为了方便测试，建议设置一个简单的密码，比如：
- `123456`
- `root123`
- `password`

注意：生产环境中请使用复杂密码！