#!/usr/bin/env python3
"""
UAV考点运营管理系统快速启动脚本
"""
import subprocess
import time
import os
import sys

def run_command(command, cwd=None):
    """执行命令"""
    try:
        print(f"执行: {command}")
        result = subprocess.run(command, shell=True, cwd=cwd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        return False

def install_dependencies():
    """安装依赖"""
    print("📦 安装后端依赖...")
    backend_dir = os.path.join(os.getcwd(), "backend")
    if os.path.exists(os.path.join(backend_dir, "requirements.txt")):
        return run_command("pip install -r requirements.txt", cwd=backend_dir)
    return True

def start_backend():
    """启动后端服务"""
    print("🚀 启动后端服务...")
    backend_dir = os.path.join(os.getcwd(), "backend")
    
    # 创建环境文件
    env_file = os.path.join(backend_dir, ".env")
    if not os.path.exists(env_file):
        env_example = os.path.join(backend_dir, ".env.example")
        if os.path.exists(env_example):
            import shutil
            shutil.copy(env_example, env_file)
            print("✅ 创建环境配置文件")
    
    # 启动FastAPI服务
    return run_command("uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload", cwd=backend_dir)

def main():
    """主函数"""
    print("🚀 UAV考点运营管理系统快速启动")
    print("="*50)
    
    # 安装依赖
    if not install_dependencies():
        print("❌ 依赖安装失败")
        return
    
    # 启动后端
    print("\n启动后端服务...")
    print("访问地址:")
    print("- 健康检查: http://localhost:8000/health")
    print("- API文档: http://localhost:8000/api/v1/docs")
    print("- 按 Ctrl+C 停止服务")
    
    try:
        start_backend()
    except KeyboardInterrupt:
        print("\n服务已停止")

if __name__ == "__main__":
    main()