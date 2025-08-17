#!/bin/bash

# UAV考点运营管理系统部署脚本
# 适用于腾讯云Ubuntu 22.04 LTS Docker预装版

set -e

echo "========================================="
echo "UAV考点运营管理系统自动化部署脚本 v1.0"
echo "========================================="

# 配置变量
SERVER_IP=${1:-"your_server_ip"}
MYSQL_ROOT_PASSWORD="uav_root_2024!"
MYSQL_DB_PASSWORD="uav_db_2024!"
JWT_SECRET=$(openssl rand -base64 32 2>/dev/null || echo "fallback-secret-key-$(date +%s)")

if [ "$SERVER_IP" = "your_server_ip" ]; then
    echo "请提供服务器IP地址:"
    echo "使用方法: ./deploy.sh <服务器IP地址>"
    echo "例如: ./deploy.sh 123.456.789.10"
    exit 1
fi

echo "目标服务器IP: $SERVER_IP"

# 1. 更新系统和安装必要软件
echo "步骤1: 更新系统和安装必要软件..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl wget nginx

# 2. 配置防火墙
echo "步骤2: 配置防火墙..."
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 3306
sudo ufw allow 6379
sudo ufw allow 8000
sudo ufw allow 3000
sudo ufw --force enable

# 3. 创建项目目录
echo "步骤3: 创建项目目录..."
sudo mkdir -p /opt/uav-exam
sudo chown $USER:$USER /opt/uav-exam
cd /opt/uav-exam

# 4. 创建环境配置文件
echo "步骤4: 创建环境配置文件..."
cat > backend/.env << EOF
# 数据库配置
MYSQL_SERVER=localhost
MYSQL_PORT=3306
MYSQL_USER=uav_user
MYSQL_PASSWORD=$MYSQL_DB_PASSWORD
MYSQL_DB=uav_exam_management

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# 应用配置
SECRET_KEY=$JWT_SECRET
ACCESS_TOKEN_EXPIRE_MINUTES=11520

# 微信小程序配置（请根据实际情况修改）
WECHAT_APPID=your_wechat_appid
WECHAT_SECRET=your_wechat_secret

# CORS配置
BACKEND_CORS_ORIGINS=http://$SERVER_IP,https://$SERVER_IP,http://localhost:3000
EOF

# 5. 启动Docker服务
echo "步骤5: 启动Docker服务..."
docker --version
docker-compose --version || (curl -L "https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose)

docker-compose down -v || true
docker-compose build
docker-compose up -d

# 6. 等待服务启动
echo "步骤6: 等待服务启动..."
sleep 30

# 7. 检查服务状态
echo "步骤7: 检查服务状态..."
docker-compose ps

# 8. 设置开机自启动
echo "步骤8: 设置开机自启动..."
sudo systemctl enable docker
sudo systemctl enable nginx

echo ""
echo "========================================="
echo "部署完成！"
echo "========================================="
echo ""
echo "系统访问地址:"
echo "健康检查: http://$SERVER_IP:8000/health"
echo "API文档: http://$SERVER_IP:8000/api/v1/docs"
echo "前端界面: http://$SERVER_IP:3000"
echo ""
echo "重要提醒:"
echo "1. 请配置微信小程序APPID和SECRET"
echo "2. 如需HTTPS，请运行: sudo certbot --nginx"
echo "3. 系统已启动，可以开始使用"
echo "========================================="