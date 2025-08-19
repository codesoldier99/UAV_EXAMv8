# UAV考点运营管理系统 - 部署环境构建指南

## 🎯 概述

本指南详细说明如何构建UAV考点运营管理系统的本地开发环境和服务器生产环境，以及如何利用GitHub进行协作开发和持续部署。

---

## 🏠 本地开发环境构建

### 系统要求

#### 最小配置
- **操作系统**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **CPU**: 2核心
- **内存**: 4GB RAM
- **存储**: 20GB 可用空间
- **网络**: 稳定的互联网连接

#### 推荐配置
- **操作系统**: Windows 11, macOS 12+, Ubuntu 22.04 LTS
- **CPU**: 4核心以上
- **内存**: 8GB+ RAM
- **存储**: 50GB+ SSD
- **网络**: 高速宽带连接

### 环境准备

#### 1. 安装基础软件

**Windows环境:**
```powershell
# 安装Chocolatey包管理器
Set-ExecutionPolicy Bypass -Scope Process -Force
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# 安装必要软件
choco install git nodejs python docker-desktop -y
choco install vscode postman -y
```

**macOS环境:**
```bash
# 安装Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装必要软件
brew install git node python@3.11
brew install --cask docker visual-studio-code postman
```

**Ubuntu环境:**
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装必要软件
sudo apt install -y git curl wget build-essential
sudo apt install -y nodejs npm python3 python3-pip

# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 2. 验证安装

```bash
# 验证各项工具安装
git --version          # Git版本
node --version         # Node.js版本
python --version       # Python版本
docker --version       # Docker版本
docker-compose --version # Docker Compose版本
```

### 项目环境搭建

#### 1. 克隆项目

```bash
# 克隆主仓库
git clone https://github.com/codesoldier99/UAV_EXAMv8.git
cd UAV_EXAMv8

# 查看项目结构
ls -la
```

#### 2. 后端环境设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境 (推荐)
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，配置数据库连接等
```

#### 3. 前端环境设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install
# 或使用yarn
yarn install

# 配置环境变量
cp .env.example .env.local
# 编辑环境变量文件
```

#### 4. 数据库设置

**使用Docker快速启动:**
```bash
# 启动MySQL和Redis
docker-compose up -d mysql redis

# 等待服务启动
sleep 30

# 初始化数据库
python init_test_data.py
```

**手动安装MySQL:**
```bash
# Ubuntu
sudo apt install mysql-server redis-server

# macOS
brew install mysql redis

# Windows (使用Chocolatey)
choco install mysql redis
```

### 本地开发启动

#### 方式1: 使用快速启动脚本

```bash
# 一键启动所有服务
python quick_start.py
```

#### 方式2: 分别启动各服务

```bash
# 终端1: 启动后端
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 终端2: 启动前端
cd frontend  
npm run dev

# 终端3: 启动数据库服务
docker-compose up -d mysql redis
```

#### 方式3: 完整Docker环境

```bash
# 启动完整开发环境
docker-compose -f docker-compose.dev.yml up -d
```

### 开发工具配置

#### VS Code配置

**推荐插件:**
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.flake8",
    "ms-python.black-formatter",
    "vue.volar",
    "bradlc.vscode-tailwindcss",
    "ms-vscode.vscode-json",
    "redhat.vscode-yaml",
    "ms-azuretools.vscode-docker"
  ]
}
```

**工作区配置 (.vscode/settings.json):**
```json
{
  "python.defaultInterpreterPath": "./backend/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "files.associations": {
    "*.vue": "vue"
  }
}
```

---

## 🌐 服务器生产环境构建

### 服务器要求

#### 最小配置
- **CPU**: 2核心 2.4GHz
- **内存**: 4GB RAM
- **存储**: 40GB SSD
- **带宽**: 5Mbps
- **操作系统**: Ubuntu 20.04+ LTS

#### 推荐配置
- **CPU**: 4核心 3.0GHz+
- **内存**: 8GB+ RAM
- **存储**: 100GB+ SSD
- **带宽**: 20Mbps+
- **操作系统**: Ubuntu 22.04 LTS

#### 高性能配置 (1200并发)
- **CPU**: 8核心 3.5GHz+
- **内存**: 16GB+ RAM
- **存储**: 200GB+ NVMe SSD
- **带宽**: 100Mbps+
- **负载均衡**: 支持
- **CDN**: 推荐使用

### 服务器初始化

#### 1. 系统更新和安全配置

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装必要工具
sudo apt install -y curl wget git unzip htop

# 配置防火墙
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 3306/tcp  # MySQL (仅内网)
sudo ufw allow 6379/tcp  # Redis (仅内网)

# 创建部署用户
sudo adduser deploy
sudo usermod -aG sudo deploy
sudo usermod -aG docker deploy
```

#### 2. 安装Docker环境

```bash
# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 启动Docker服务
sudo systemctl enable docker
sudo systemctl start docker

# 验证安装
docker --version
docker-compose --version
```

#### 3. 配置Nginx (可选，用于SSL终止)

```bash
# 安装Nginx
sudo apt install -y nginx

# 配置Nginx
sudo nano /etc/nginx/sites-available/uav-system

# 启用站点
sudo ln -s /etc/nginx/sites-available/uav-system /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 生产环境部署

#### 1. 使用自动化脚本部署

```bash
# 下载项目
git clone https://github.com/codesoldier99/UAV_EXAMv8.git
cd UAV_EXAMv8

# 运行自动化部署脚本
chmod +x deploy.sh
./deploy.sh YOUR_SERVER_IP
```

#### 2. 手动部署步骤

```bash
# 1. 创建项目目录
sudo mkdir -p /opt/uav-exam
sudo chown deploy:deploy /opt/uav-exam
cd /opt/uav-exam

# 2. 克隆项目
git clone https://github.com/codesoldier99/UAV_EXAMv8.git .

# 3. 配置环境变量
cp backend/.env.example backend/.env
nano backend/.env  # 配置生产环境变量

# 4. 构建和启动服务
docker-compose -f docker-compose.prod.yml up -d --build

# 5. 初始化数据库
docker-compose exec backend python init_test_data.py

# 6. 验证部署
curl http://localhost:8000/health
```

#### 3. 生产环境配置优化

**docker-compose.prod.yml:**
```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
    volumes:
      - mysql_data:/var/lib/mysql
      - ./docker/mysql/my.cnf:/etc/mysql/conf.d/my.cnf
    command: --default-authentication-plugin=mysql_native_password

  redis:
    image: redis:7-alpine
    restart: always
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data

  backend:
    build: ./backend
    restart: always
    environment:
      - DATABASE_URL=mysql+pymysql://root:${MYSQL_ROOT_PASSWORD}@mysql:3306/${MYSQL_DATABASE}
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
    depends_on:
      - mysql
      - redis

  frontend:
    build: ./frontend
    restart: always
    environment:
      - VITE_API_URL=https://yourdomain.com
    depends_on:
      - backend

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./docker/nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./docker/nginx/ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend

volumes:
  mysql_data:
  redis_data:
```

### SSL证书配置

#### 使用Let's Encrypt (免费)

```bash
# 安装Certbot
sudo apt install -y certbot python3-certbot-nginx

# 获取SSL证书
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# 自动续期
sudo crontab -e
# 添加以下行：
# 0 12 * * * /usr/bin/certbot renew --quiet
```

#### 使用自签名证书 (开发环境)

```bash
# 创建证书目录
mkdir -p docker/nginx/ssl

# 生成自签名证书
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout docker/nginx/ssl/key.pem \
  -out docker/nginx/ssl/cert.pem
```

---

## 🔄 GitHub协作和CI/CD

### GitHub仓库设置

#### 1. 仓库结构

```
UAV_EXAMv8/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── deploy.yml
│   │   └── test.yml
│   └── ISSUE_TEMPLATE/
├── backend/
├── frontend/
├── miniprogram/
├── docker/
├── docs/
├── scripts/
├── .gitignore
├── README.md
└── CONTRIBUTING.md
```

#### 2. 分支策略

```bash
# 主分支
main          # 生产环境代码
develop       # 开发主分支

# 功能分支
feature/*     # 新功能开发
bugfix/*      # Bug修复
hotfix/*      # 紧急修复
release/*     # 发布准备
```

#### 3. Git工作流

```bash
# 1. 克隆仓库
git clone https://github.com/codesoldier99/UAV_EXAMv8.git
cd UAV_EXAMv8

# 2. 创建功能分支
git checkout -b feature/new-feature develop

# 3. 开发和提交
git add .
git commit -m "feat: 添加新功能"

# 4. 推送分支
git push origin feature/new-feature

# 5. 创建Pull Request
# 在GitHub上创建PR，合并到develop分支
```

### 持续集成配置

#### CI工作流 (.github/workflows/ci.yml)

```yaml
name: Continuous Integration

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  backend-test:
    runs-on: ubuntu-latest
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: test123
          MYSQL_DATABASE: test_db
        options: --health-cmd="mysqladmin ping" --health-interval=10s --health-timeout=5s --health-retries=3

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        cd backend
        pytest tests/ -v
    
    - name: Run API tests
      run: |
        python test_api.py

  frontend-test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install dependencies
      run: |
        cd frontend
        npm ci
    
    - name: Run tests
      run: |
        cd frontend
        npm run test
    
    - name: Build
      run: |
        cd frontend
        npm run build
```

#### 部署工作流 (.github/workflows/deploy.yml)

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]
  release:
    types: [ published ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.SERVER_HOST }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SERVER_SSH_KEY }}
        script: |
          cd /opt/uav-exam
          git pull origin main
          docker-compose -f docker-compose.prod.yml down
          docker-compose -f docker-compose.prod.yml up -d --build
          
    - name: Health Check
      run: |
        sleep 30
        curl -f http://${{ secrets.SERVER_HOST }}/health || exit 1
    
    - name: Notify Deployment
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        text: "部署完成: UAV考点管理系统已更新"
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### GitHub Secrets配置

在GitHub仓库设置中配置以下Secrets:

```
SERVER_HOST=your-server-ip
SERVER_USER=deploy
SERVER_SSH_KEY=your-private-ssh-key
MYSQL_ROOT_PASSWORD=your-mysql-password
REDIS_PASSWORD=your-redis-password
SLACK_WEBHOOK=your-slack-webhook-url
```

### 代码质量检查

#### Pre-commit配置 (.pre-commit-config.yaml)

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 22.12.0
    hooks:
      - id: black
        files: ^backend/

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        files: ^backend/

  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.34.0
    hooks:
      - id: eslint
        files: ^frontend/
```

---

## 🚀 优化和扩展

### 性能优化

#### 1. 数据库优化

```sql
-- 创建复合索引
CREATE INDEX idx_user_role_institution ON users(role, institution_id);
CREATE INDEX idx_schedule_date_venue ON schedules(schedule_date, venue_id);

-- 分区表 (大数据量时)
ALTER TABLE checkins PARTITION BY RANGE (YEAR(checkin_time));
```

#### 2. 缓存策略

```python
# Redis缓存配置
CACHE_CONFIG = {
    "venues_status": {"ttl": 60},      # 考场状态缓存1分钟
    "user_sessions": {"ttl": 3600},    # 用户会话缓存1小时
    "system_stats": {"ttl": 300},      # 系统统计缓存5分钟
}
```

#### 3. 负载均衡

```nginx
upstream backend_servers {
    server backend1:8000 weight=3;
    server backend2:8000 weight=2;
    server backend3:8000 weight=1;
    keepalive 32;
}
```

### 监控和日志

#### 1. 应用监控

```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

  elasticsearch:
    image: elasticsearch:7.17.0
    environment:
      - discovery.type=single-node
    ports:
      - "9200:9200"

  kibana:
    image: kibana:7.17.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
```

#### 2. 日志聚合

```python
# 日志配置
LOGGING_CONFIG = {
    "version": 1,
    "handlers": {
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/var/log/uav-system.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        }
    }
}
```

### 安全加固

#### 1. 网络安全

```bash
# 防火墙规则
sudo ufw deny 3306  # 禁止外网访问MySQL
sudo ufw deny 6379  # 禁止外网访问Redis
sudo ufw limit ssh  # 限制SSH连接频率
```

#### 2. 应用安全

```python
# 安全中间件配置
SECURITY_CONFIG = {
    "CORS_ORIGINS": ["https://yourdomain.com"],
    "RATE_LIMIT": "100/minute",
    "SESSION_TIMEOUT": 3600,
    "PASSWORD_MIN_LENGTH": 8,
    "JWT_EXPIRE_MINUTES": 60
}
```

---

## 📋 运维检查清单

### 日常维护

- [ ] **每日检查**
  - [ ] 服务状态监控
  - [ ] 错误日志检查
  - [ ] 数据库性能监控
  - [ ] 磁盘空间检查

- [ ] **每周检查**
  - [ ] 系统更新检查
  - [ ] 安全补丁更新
  - [ ] 数据备份验证
  - [ ] 性能报告分析

- [ ] **每月检查**
  - [ ] 容量规划评估
  - [ ] 安全审计
  - [ ] 灾难恢复测试
  - [ ] 用户反馈收集

### 故障处理

#### 常见问题排查

```bash
# 1. 服务无法启动
docker-compose logs backend
docker-compose ps

# 2. 数据库连接失败
docker-compose exec mysql mysql -u root -p
telnet localhost 3306

# 3. 内存不足
free -h
docker stats

# 4. 磁盘空间不足
df -h
docker system prune -a
```

#### 紧急恢复

```bash
# 1. 快速重启
docker-compose restart

# 2. 回滚到上一版本
git checkout HEAD~1
docker-compose up -d --build

# 3. 数据库恢复
mysql -u root -p uav_exam_management < backup.sql
```

---

## 🎯 总结

本指南涵盖了UAV考点运营管理系统从开发到生产的完整部署流程：

1. **本地环境**: 快速搭建开发环境
2. **服务器环境**: 生产级别的部署配置
3. **GitHub协作**: 现代化的开发工作流
4. **CI/CD**: 自动化测试和部署
5. **监控运维**: 系统健康监控和维护

通过遵循本指南，您可以：
- 快速搭建开发环境进行功能开发
- 部署稳定的生产环境支持1200并发用户
- 建立高效的团队协作流程
- 实现自动化的持续集成和部署
- 确保系统的稳定性和安全性

**建议**: 从本地开发环境开始，逐步过渡到生产环境，并根据实际需求调整配置参数。

---

**文档版本**: v1.0  
**更新时间**: 2025-01-18  
**适用版本**: UAV考点管理系统 v1.1.0
