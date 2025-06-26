#!/usr/bin/env python3
"""
时间序列模型分析与诊断工具FastAPI服务的部署脚本
"""

import os
import sys
import subprocess
import argparse
import platform
from pathlib import Path


def run_command(command, description, check=True):
    """运行命令并显示进度"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(f"📝 输出: {result.stdout.strip()}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ 错误: {e}")
        if e.stderr:
            print(f"📝 错误信息: {e.stderr.strip()}")
        sys.exit(1)


def check_requirements():
    """检查必要的工具是否已安装"""
    print("🔍 检查系统要求...")
    
    # 检查Python版本
    python_version = platform.python_version()
    print(f"📍 Python版本: {python_version}")
    
    # 检查uv是否安装
    try:
        result = subprocess.run("uv --version", shell=True, capture_output=True, text=True, check=True)
        print(f"📍 uv版本: {result.stdout.strip()}")
    except subprocess.CalledProcessError:
        print("❌ uv包管理器未安装，正在安装...")
        if platform.system() == "Windows":
            run_command("pip install uv", "安装uv")
        else:
            run_command("curl -LsSf https://astral.sh/uv/install.sh | sh", "安装uv")


def install_dependencies():
    """安装项目依赖"""
    print("📦 安装项目依赖...")
    run_command("uv sync", "使用uv同步依赖")


def run_development_server():
    """运行开发服务器"""
    print("🚀 启动开发服务器...")
    print("📍 服务地址: http://localhost:8000")
    print("📖 API文档: http://localhost:8000/docs")
    print("📚 ReDoc文档: http://localhost:8000/redoc")
    print("❤️  健康检查: http://localhost:8000/health")
    print("\n按 Ctrl+C 停止服务器")
    
    try:
        subprocess.run("uv run python app.py --reload", shell=True, check=True)
    except KeyboardInterrupt:
        print("\n🛑 服务器已停止")


def run_production_server():
    """运行生产服务器"""
    print("🚀 启动生产服务器...")
    print("📍 服务地址: http://localhost:8000")
    print("📖 API文档: http://localhost:8000/docs")
    print("📚 ReDoc文档: http://localhost:8000/redoc")
    print("❤️  健康检查: http://localhost:8000/health")
    print("\n按 Ctrl+C 停止服务器")
    
    try:
        subprocess.run("uv run python app.py --workers 4", shell=True, check=True)
    except KeyboardInterrupt:
        print("\n🛑 服务器已停止")


def build_docker_image():
    """构建Docker镜像"""
    print("🐳 构建Docker镜像...")
    run_command("docker build -t tsdiag-api .", "构建Docker镜像")
    print("✅ Docker镜像构建完成: tsdiag-api")


def run_docker_container():
    """运行Docker容器"""
    print("🐳 启动Docker容器...")
    run_command("docker run -d -p 8000:8000 --name tsdiag-api-container tsdiag-api", "启动Docker容器")
    print("✅ Docker容器已启动")
    print("📍 服务地址: http://localhost:8000")


def run_docker_compose():
    """使用Docker Compose运行"""
    print("🐳 使用Docker Compose启动服务...")
    try:
        subprocess.run("docker-compose up -d", shell=True, check=True)
        print("✅ 服务已通过Docker Compose启动")
        print("📍 服务地址: http://localhost:8000")
    except KeyboardInterrupt:
        print("\n🛑 正在停止服务...")
        subprocess.run("docker-compose down", shell=True)


def run_tests():
    """运行测试"""
    print("🧪 运行测试...")
    run_command("uv run python -m pytest tests/ -v", "运行单元测试")


def setup_systemd_service():
    """设置systemd服务（仅Linux）"""
    if platform.system() != "Linux":
        print("❌ systemd服务仅在Linux系统上可用")
        return
    
    print("⚙️  设置systemd服务...")
    
    current_dir = Path.cwd()
    service_content = f"""[Unit]
Description=Time Series Model Analysis and Diagnostic Tool API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory={current_dir}
Environment=PATH={current_dir}/.venv/bin
ExecStart={current_dir}/.venv/bin/python app.py --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
"""
    
    service_file = "/etc/systemd/system/tsdiag-api.service"
    print(f"📝 创建服务文件: {service_file}")
    print("⚠️  需要sudo权限")
    
    with open("/tmp/tsdiag-api.service", "w") as f:
        f.write(service_content)
    
    run_command(f"sudo mv /tmp/tsdiag-api.service {service_file}", "移动服务文件")
    run_command("sudo systemctl daemon-reload", "重新加载systemd")
    run_command("sudo systemctl enable tsdiag-api", "启用服务")
    run_command("sudo systemctl start tsdiag-api", "启动服务")
    
    print("✅ systemd服务已设置并启动")
    print("📍 查看状态: sudo systemctl status tsdiag-api")
    print("📍 查看日志: sudo journalctl -u tsdiag-api -f")


def main():
    parser = argparse.ArgumentParser(description="时间序列模型分析与诊断工具FastAPI服务部署脚本")
    parser.add_argument("action", choices=[
        "setup", "dev", "prod", "docker-build", "docker-run", 
        "docker-compose", "test", "systemd", "check"
    ], help="要执行的操作")
    
    args = parser.parse_args()
    
    print("🎯 时间序列模型分析与诊断工具 - FastAPI服务部署")
    print("=" * 60)
    
    if args.action == "check":
        check_requirements()
    
    elif args.action == "setup":
        check_requirements()
        install_dependencies()
        print("✅ 项目设置完成!")
        print("🚀 运行开发服务器: python deploy.py dev")
        print("🐳 使用Docker: python deploy.py docker-compose")
    
    elif args.action == "dev":
        run_development_server()
    
    elif args.action == "prod":
        run_production_server()
    
    elif args.action == "docker-build":
        build_docker_image()
    
    elif args.action == "docker-run":
        build_docker_image()
        run_docker_container()
    
    elif args.action == "docker-compose":
        run_docker_compose()
    
    elif args.action == "test":
        run_tests()
    
    elif args.action == "systemd":
        setup_systemd_service()


if __name__ == "__main__":
    main()
