# UAV考点运营与流程管理系统

## 🎯 项目简介

UAV考点运营与流程管理系统是一套专为无人机考试机构设计的综合管理平台，旨在解决考点现场管理混乱、信息不透明、考生焦虑以及运营效率低下等问题。

### ✨ 系统特点

- 🏛️ **后台管理**: 完整的用户、角色、权限(RBAC)管理体系
- 📋 **报名流程**: 支持批量导入和手动录入考生信息
- 📅 **日程编排**: 智能化考试日程安排，支持按机构集中管理
- 📱 **移动端支持**: 微信小程序提供考生服务和考务管理
- 🔍 **实时监控**: 考场动态看板，实时更新考试状态
- 🏗️ **高性能**: 支持1200人同时在线，响应时间<500ms

## 🔧 技术架构

### 后端技术栈
- **框架**: FastAPI + Python 3.11
- **数据库**: MySQL 8.0 + Redis
- **认证**: JWT + FastAPI-Users
- **部署**: Docker + Docker Compose

### 前端技术栈
- **PC管理后台**: Vue 3 + Element Plus
- **微信小程序**: 原生小程序框架
- **构建工具**: Vite

## 🚀 快速开始

### 方式1：快速启动（推荐）

```bash
# 克隆项目
git clone https://github.com/codesoldier99/UAV_EXAMv8.git
cd UAV_EXAMv8

# 一键启动
python quick_start.py
```

### 方式2：Docker部署

```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps
```

### 方式3：生产环境部署

```bash
# 在服务器上执行
chmod +x deploy.sh
./deploy.sh your_server_ip
```

## 📊 系统访问

启动成功后访问：

- **健康检查**: http://localhost:8000/health
- **API文档**: http://localhost:8000/api/v1/docs
- **前端界面**: http://localhost:3000（如果启动了前端）

### 测试API端点

```bash
# 健康检查
curl http://localhost:8000/health

# 用户登录
curl -X POST "http://localhost:8000/api/v1/auth/login" -d "username=admin&password=admin123"

# 获取机构列表  
curl http://localhost:8000/api/v1/institutions

# 考场状态（小程序公共看板）
curl http://localhost:8000/api/v1/public/venues-status
```

## 🏗️ 核心功能

### 用户角色管理
- **超级管理员**: 系统配置、用户管理
- **考务管理员**: 考试安排、现场监控
- **机构用户**: 考生报名、信息查询
- **考务人员**: 现场扫码签到
- **考生**: 查看日程、出示二维码

### 考生管理
- 批量Excel导入考生信息
- 手动单个考生录入
- 按机构隔离数据访问
- 考生状态实时追踪

### 排期管理
- 智能日程编排算法
- 按机构集中安排实操考试
- 考场资源优化配置
- 实时排队状态显示

### 移动端功能
- 考生动态二维码身份凭证
- 考务人员扫码签到
- 实时考场状态看板
- 个人日程查询

## 📱 微信小程序

小程序配置文件在 `miniprogram/` 目录：

- `app.json` - 小程序配置
- `app.js` - 小程序入口文件
- 支持考生登录、二维码显示、日程查看等功能

## 🐳 Docker支持

项目包含完整的Docker配置：

- `docker-compose.yml` - 服务编排配置
- `backend/Dockerfile` - 后端镜像构建
- `frontend/Dockerfile` - 前端镜像构建

服务包括：
- MySQL 8.0 数据库
- Redis 缓存
- FastAPI 后端
- Vue3 前端
- Nginx 反向代理

## 📦 项目结构

```
UAV_EXAMv8/
├── backend/                 # FastAPI后端
│   ├── app/                # 应用代码
│   ├── requirements.txt    # Python依赖
│   ├── Dockerfile          # Docker镜像
│   └── .env.example        # 环境配置示例
├── frontend/               # Vue3前端
│   ├── src/                # 源代码
│   ├── package.json        # 前端依赖
│   └── Dockerfile          # Docker镜像
├── miniprogram/            # 微信小程序
│   ├── pages/              # 小程序页面
│   ├── app.json            # 小程序配置
│   └── app.js              # 小程序入口
├── docker-compose.yml      # Docker编排
├── deploy.sh               # 部署脚本
├── quick_start.py          # 快速启动
└── README.md               # 项目文档
```

## ⚡ 性能特性

- **高并发**: 支持1200人同时在线
- **快速响应**: API响应时间<500ms
- **缓存优化**: Redis缓存热点数据
- **数据库优化**: 索引优化和连接池配置

## 🔒 安全特性

- JWT Token认证
- RBAC权限控制
- SQL注入防护
- XSS攻击防护
- CORS策略配置
- HTTPS通信加密

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/new-feature`)
3. 提交更改 (`git commit -m 'Add some feature'`)
4. 推送到分支 (`git push origin feature/new-feature`)
5. 创建 Pull Request

## 📝 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 技术支持

- 项目地址: https://github.com/codesoldier99/UAV_EXAMv8
- Issues: https://github.com/codesoldier99/UAV_EXAMv8/issues

## 🎉 更新日志

### v1.0.0 (2025-08-17)
- 🎉 初始版本发布
- ✅ 完整的用户权限管理系统
- ✅ 考生报名和排期管理
- ✅ 微信小程序支持
- ✅ 实时考场看板
- ✅ Docker容器化部署
- ✅ 自动化部署脚本
- ✅ 完整的API文档

---

**享受您的UAV考点管理系统！** 🚀
