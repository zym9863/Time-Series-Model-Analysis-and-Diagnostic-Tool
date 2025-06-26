# 时间序列模型分析与诊断工具 - FastAPI服务

这是一个基于FastAPI的REST API服务，提供时间序列模型分析与诊断功能，包括AR模型平稳性检验和MA模型可逆性检验。

## 🚀 快速开始

### 使用uv包管理器（推荐）

```bash
# 1. 安装uv（如果还没有安装）
pip install uv

# 2. 安装依赖
uv sync

# 3. 启动开发服务器
uv run python app.py --reload

# 或者使用部署脚本
python deploy.py setup  # 初始化项目
python deploy.py dev    # 启动开发服务器
```

### 使用传统pip

```bash
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 3. 安装依赖
pip install -e .

# 4. 启动服务器
python app.py
```

### 使用Docker

```bash
# 1. 构建并运行（推荐）
docker-compose up -d

# 2. 或者手动构建
docker build -t tsdiag-api .
docker run -p 8000:8000 tsdiag-api

# 3. 使用部署脚本
python deploy.py docker-compose
```

## 📖 API文档

启动服务后，可以通过以下地址访问API文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **健康检查**: http://localhost:8000/health

## 🔧 API端点

### 基础检验

- `POST /api/v1/ar/check` - AR模型平稳性检验
- `POST /api/v1/ma/check` - MA模型可逆性检验
- `POST /api/v1/arma/check` - ARMA模型综合检验

### 快速检验

- `POST /api/v1/ar/quick` - 快速AR检验（仅返回布尔值）
- `POST /api/v1/ma/quick` - 快速MA检验（仅返回布尔值）
- `POST /api/v1/arma/quick` - 快速ARMA检验（仅返回布尔值）

### 高级分析

- `POST /api/v1/stability/analyze` - 模型稳定性分析
- `POST /api/v1/batch/analyze` - 批量模型分析

## 📝 使用示例

### Python客户端

```python
import requests

# 基础检验
data = {"coefficients": [0.5, 0.3], "verbose": True}
response = requests.post("http://localhost:8000/api/v1/ar/check", json=data)
result = response.json()
print(f"平稳性: {result['is_stationary']}")

# 快速检验
data = {"coefficients": [0.5, 0.3]}
response = requests.post("http://localhost:8000/api/v1/ar/quick", json=data)
is_stationary = response.json()["result"]
```

### cURL

```bash
# AR模型检验
curl -X POST "http://localhost:8000/api/v1/ar/check" \
     -H "Content-Type: application/json" \
     -d '{"coefficients": [0.5, 0.3], "verbose": true}'

# MA模型检验
curl -X POST "http://localhost:8000/api/v1/ma/check" \
     -H "Content-Type: application/json" \
     -d '{"coefficients": [0.4, 0.2], "verbose": true}'

# ARMA模型检验
curl -X POST "http://localhost:8000/api/v1/arma/check" \
     -H "Content-Type: application/json" \
     -d '{"ar_coefficients": [0.5, 0.3], "ma_coefficients": [0.4, 0.2], "verbose": true}'
```

### JavaScript/fetch

```javascript
// AR模型检验
const response = await fetch('http://localhost:8000/api/v1/ar/check', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ coefficients: [0.5, 0.3], verbose: true })
});
const result = await response.json();
console.log('平稳性:', result.is_stationary);
```

## 📊 客户端示例

运行完整的客户端示例：

```bash
# 确保API服务正在运行，然后执行：
uv run python examples/fastapi_client_demo.py
```

## ⚙️ 配置选项

### 环境变量

复制 `.env.example` 到 `.env` 并根据需要修改配置：

```bash
cp .env.example .env
```

### 命令行参数

```bash
python app.py --help
```

常用选项：
- `--host`: 服务器地址（默认: 0.0.0.0）
- `--port`: 端口号（默认: 8000）
- `--reload`: 启用热重载（开发模式）
- `--workers`: 工作进程数（生产模式）
- `--log-level`: 日志级别

## 🚀 部署

### 开发环境

```bash
python deploy.py dev
```

### 生产环境

```bash
# 本地生产环境
python deploy.py prod

# Docker生产环境
python deploy.py docker-compose

# Linux systemd服务
python deploy.py systemd
```

### 使用反向代理（生产环境推荐）

使用Docker Compose with Nginx：

```bash
docker-compose --profile production up -d
```

这将启动：
- FastAPI应用（端口8000）
- Nginx反向代理（端口80）

## 🧪 测试

```bash
# 运行单元测试
python deploy.py test

# 或者直接使用pytest
uv run python -m pytest tests/ -v
```

## 📁 项目结构

```
├── src/tsdiag/
│   ├── __init__.py
│   ├── api.py              # 高级API接口
│   ├── core.py             # 核心计算模块
│   ├── fastapi_app.py      # FastAPI应用 (新增)
│   ├── stationarity.py     # 平稳性检验
│   └── invertibility.py    # 可逆性检验
├── examples/
│   ├── fastapi_client_demo.py  # FastAPI客户端示例 (新增)
│   ├── basic_usage.py
│   ├── batch_analysis.py
│   └── demo.py
├── tests/                  # 测试文件
├── app.py                  # 启动脚本 (新增)
├── deploy.py               # 部署脚本 (新增)
├── Dockerfile              # Docker配置 (新增)
├── docker-compose.yml      # Docker Compose配置 (新增)
├── nginx.conf              # Nginx配置 (新增)
├── .env.example            # 环境变量示例 (新增)
├── pyproject.toml          # 项目配置（已更新）
└── README_API.md           # API文档 (本文件)
```

## 🔍 监控和日志

### 健康检查

```bash
curl http://localhost:8000/health
```

### 日志查看

```bash
# Docker容器日志
docker-compose logs -f tsdiag-api

# systemd服务日志（Linux）
sudo journalctl -u tsdiag-api -f
```

### 性能监控

API提供以下监控指标：
- 请求响应时间
- 请求成功/失败率
- 并发连接数

可以集成Prometheus + Grafana进行可视化监控。

## ❓ 常见问题

### 1. 服务启动失败

检查端口是否被占用：
```bash
# Windows
netstat -an | findstr :8000

# Linux/Mac
lsof -i :8000
```

### 2. 依赖安装问题

确保使用正确的Python版本（>=3.8）：
```bash
python --version
uv python list
```

### 3. Docker构建失败

确保Docker服务正在运行，并有足够的磁盘空间。

### 4. API请求超时

检查模型系数是否过大，复杂的计算可能需要更长时间。

## 📞 支持

如果遇到问题或有建议，请：
1. 查看API文档：http://localhost:8000/docs
2. 运行健康检查：http://localhost:8000/health
3. 查看日志文件
4. 提交Issue到项目仓库

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。
