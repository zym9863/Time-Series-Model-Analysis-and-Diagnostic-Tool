#!/usr/bin/env python3
"""
时间序列模型分析与诊断工具的FastAPI服务启动脚本
"""

import uvicorn
import argparse
import sys
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from tsdiag.fastapi_app import app


def main():
    parser = argparse.ArgumentParser(description="启动时间序列模型分析与诊断工具的FastAPI服务")
    parser.add_argument("--host", default="0.0.0.0", help="服务器主机地址 (默认: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="服务器端口 (默认: 8000)")
    parser.add_argument("--reload", action="store_true", help="启用自动重载 (开发模式)")
    parser.add_argument("--workers", type=int, default=1, help="工作进程数量 (默认: 1)")
    parser.add_argument("--log-level", default="info", 
                       choices=["critical", "error", "warning", "info", "debug"],
                       help="日志级别 (默认: info)")
    
    args = parser.parse_args()
    
    print(f"🚀 启动时间序列模型分析与诊断API服务...")
    print(f"📍 地址: http://{args.host}:{args.port}")
    print(f"📖 API文档: http://{args.host}:{args.port}/docs")
    print(f"📚 ReDoc文档: http://{args.host}:{args.port}/redoc")
    print(f"❤️  健康检查: http://{args.host}:{args.port}/health")
    
    uvicorn.run(
        "tsdiag.fastapi_app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        workers=args.workers if not args.reload else 1,  # reload模式下只能使用1个worker
        log_level=args.log_level,
        access_log=True
    )


if __name__ == "__main__":
    main()
