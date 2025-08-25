@echo off
chcp 65001
echo 正在配置MySQL...

REM 创建MySQL目录
if not exist "C:\mysql" mkdir "C:\mysql"
if not exist "C:\mysql\data" mkdir "C:\mysql\data"

echo MySQL目录创建完成

REM 提示用户解压MySQL
echo.
echo 请将下载的MySQL ZIP文件解压到 C:\mysql 目录
echo 解压后的结构应该是: C:\mysql\bin, C:\mysql\lib 等
echo.
pause

REM 初始化MySQL
echo 初始化MySQL数据库...
cd /d C:\mysql\bin
mysqld --initialize --console

echo.
echo 请记住上面显示的临时root密码！
echo.
pause

REM 安装MySQL服务
echo 安装MySQL服务...
mysqld install MySQL

echo 启动MySQL服务...
net start MySQL

echo MySQL安装完成！
echo 现在您可以使用临时密码登录并设置新密码
echo 命令: mysql -u root -p
pause