"""
GitHub仓库上传脚本
自动化将项目上传到GitHub的完整流程
"""

import subprocess
import os
import sys

def run_command(command, description=""):
    """
    执行命令并显示结果
    
    Args:
        command: 要执行的命令
        description: 命令描述
    """
    if description:
        print(f"\n🔄 {description}")
        print(f"执行命令: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            if result.stdout:
                print(f"✅ 成功: {result.stdout.strip()}")
            return True
        else:
            if result.stderr:
                print(f"❌ 错误: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ 执行命令时发生异常: {e}")
        return False

def check_git_config():
    """检查Git配置"""
    print("🔍 检查Git配置...")
    
    # 检查用户名
    result = subprocess.run("git config --global user.name", shell=True, capture_output=True, text=True)
    if result.returncode != 0 or not result.stdout.strip():
        print("⚠️  Git用户名未配置")
        name = input("请输入您的Git用户名: ").strip()
        run_command(f'git config --global user.name "{name}"', "配置Git用户名")
    else:
        print(f"✅ Git用户名: {result.stdout.strip()}")
    
    # 检查邮箱
    result = subprocess.run("git config --global user.email", shell=True, capture_output=True, text=True)
    if result.returncode != 0 or not result.stdout.strip():
        print("⚠️  Git邮箱未配置")
        email = input("请输入您的Git邮箱: ").strip()
        run_command(f'git config --global user.email "{email}"', "配置Git邮箱")
    else:
        print(f"✅ Git邮箱: {result.stdout.strip()}")

def init_git_repo():
    """初始化Git仓库"""
    print("\n📁 初始化Git仓库...")
    
    # 检查是否已经是Git仓库
    if os.path.exists(".git"):
        print("✅ Git仓库已存在")
        return True
    
    # 初始化仓库
    if not run_command("git init", "初始化Git仓库"):
        return False
    
    # 添加所有文件
    if not run_command("git add .", "添加所有文件到暂存区"):
        return False
    
    # 提交初始版本
    commit_message = "🎉 Initial commit: Python用户服务API v1.0.0\n\n✨ 功能:\n- 用户注册登录\n- JWT认证\n- FastAPI + MySQL\n- 完整工具集"
    if not run_command(f'git commit -m "{commit_message}"', "提交初始版本"):
        return False
    
    return True

def add_remote_and_push():
    """添加远程仓库并推送"""
    print("\n🌐 配置远程仓库...")
    
    # 获取GitHub仓库URL
    print("\n请在GitHub上创建新仓库，然后提供仓库信息:")
    print("📋 仓库创建步骤:")
    print("1. 访问 https://github.com/new")
    print("2. 仓库名建议: python-service 或 user-auth-api")
    print("3. 设为Public或Private")
    print("4. 不要初始化README、.gitignore或License（我们已经创建了）")
    print("5. 点击 'Create repository'")
    
    # 获取用户输入
    github_username = input("\n请输入您的GitHub用户名: ").strip()
    repo_name = input("请输入仓库名称 (建议: python-service): ").strip()
    
    if not repo_name:
        repo_name = "python-service"
    
    # 构建仓库URL
    repo_url = f"https://github.com/{github_username}/{repo_name}.git"
    
    print(f"\n🔗 仓库URL: {repo_url}")
    
    # 检查是否已有远程仓库
    result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
    if "origin" in result.stdout:
        print("⚠️  检测到已有远程仓库，将更新...")
        run_command("git remote remove origin", "移除现有远程仓库")
    
    # 添加远程仓库
    if not run_command(f"git remote add origin {repo_url}", "添加远程仓库"):
        return False
    
    # 推送到GitHub
    print("\n📤 推送到GitHub...")
    
    # 创建并切换到main分支
    run_command("git branch -M main", "切换到main分支")
    
    # 推送代码
    if not run_command("git push -u origin main", "推送代码到GitHub"):
        print("❌ 推送失败，可能需要身份验证")
        print("\n🔐 如果需要身份验证，请:")
        print("1. 使用GitHub Personal Access Token")
        print("2. 或配置SSH密钥")
        print("3. 详见: https://docs.github.com/zh/authentication")
        return False
    
    print(f"\n🎉 成功！项目已上传到: https://github.com/{github_username}/{repo_name}")
    return True

def create_github_workflow():
    """创建GitHub Actions工作流"""
    print("\n⚙️ 创建GitHub Actions工作流...")
    
    # 创建.github/workflows目录
    os.makedirs(".github/workflows", exist_ok=True)
    
    workflow_content = """name: Python API Test

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: test123
          MYSQL_DATABASE: user_service
        ports:
          - 3306:3306
        options: >-
          --health-cmd="mysqladmin ping"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=3

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Set up environment
      run: |
        cp .env.example .env
        sed -i 's/your_mysql_password_here/test123/' .env
    
    - name: Initialize database
      run: |
        python init_db.py
    
    - name: Test API health
      run: |
        python -m app.main &
        sleep 10
        curl -f http://localhost:8000/ || exit 1
"""
    
    with open(".github/workflows/test.yml", "w", encoding="utf-8") as f:
        f.write(workflow_content)
    
    print("✅ GitHub Actions工作流已创建")

def display_next_steps(github_username, repo_name):
    """显示后续步骤"""
    print("\n" + "="*60)
    print("🎉 项目上传完成！")
    print("="*60)
    
    print(f"\n📋 您的仓库信息:")
    print(f"🔗 仓库地址: https://github.com/{github_username}/{repo_name}")
    print(f"📖 README: https://github.com/{github_username}/{repo_name}#readme")
    print(f"📥 克隆命令: git clone https://github.com/{github_username}/{repo_name}.git")
    
    print(f"\n🚀 后续可以做的事:")
    print("1. 📝 编辑仓库描述和标签")
    print("2. ⭐ 邀请朋友给仓库Star")
    print("3. 🔄 设置GitHub Pages展示API文档")
    print("4. 🏷️  创建Release版本")
    print("5. 📊 查看GitHub Actions构建状态")
    print("6. 🤝 邀请协作者")
    
    print(f"\n📱 分享您的项目:")
    print(f"💬 项目链接: https://github.com/{github_username}/{repo_name}")
    print("🌟 记得给项目写个好的描述!")

def main():
    """主函数"""
    print("🚀 GitHub项目上传工具")
    print("="*50)
    
    # 检查当前目录
    if not os.path.exists("app"):
        print("❌ 请在项目根目录运行此脚本")
        sys.exit(1)
    
    # 步骤1: 检查Git配置
    check_git_config()
    
    # 步骤2: 初始化Git仓库
    if not init_git_repo():
        print("❌ Git仓库初始化失败")
        sys.exit(1)
    
    # 步骤3: 创建GitHub工作流
    create_github_workflow()
    
    # 步骤4: 添加新文件并提交
    run_command("git add .", "添加新文件")
    run_command('git commit -m "🔧 Add GitHub workflow and documentation"', "提交更新")
    
    # 步骤5: 推送到GitHub
    print("\n" + "="*50)
    print("📤 准备上传到GitHub")
    print("="*50)
    
    try:
        # 获取仓库信息
        github_username = input("请输入您的GitHub用户名: ").strip()
        repo_name = input("请输入仓库名称 (默认: python-service): ").strip() or "python-service"
        
        if add_remote_and_push():
            display_next_steps(github_username, repo_name)
        else:
            print("\n❌ 上传失败，请检查网络连接和GitHub账户权限")
            print("💡 可以手动执行以下命令:")
            print(f"git remote add origin https://github.com/{github_username}/{repo_name}.git")
            print("git branch -M main")
            print("git push -u origin main")
    
    except KeyboardInterrupt:
        print("\n\n⏹️  用户取消操作")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")

if __name__ == "__main__":
    main()