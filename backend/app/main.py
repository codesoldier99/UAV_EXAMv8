"""
FastAPI主应用程序
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# 创建FastAPI应用实例
app = FastAPI(
    title="UAV考点运营管理系统",
    version="1.0.0",
    description="UAV考点运营管理系统API",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 信任主机中间件
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["*"]  # 在生产环境中应该设置具体的域名
)

# 健康检查端点
@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "healthy", "message": "UAV考点运营管理系统运行正常"}

@app.get("/")
def read_root():
    """根路径"""
    return {"message": "欢迎使用UAV考点运营管理系统", "docs": "/api/v1/docs"}

# 用户登录端点（简化版）
@app.post("/api/v1/auth/login")
def login():
    """用户登录"""
    return {
        "access_token": "demo_token_12345",
        "token_type": "bearer",
        "user": {
            "id": 1,
            "username": "admin",
            "email": "admin@example.com",
            "real_name": "系统管理员",
            "permissions": ["user.read", "institution.read", "candidate.read"]
        }
    }

# 获取当前用户信息
@app.get("/api/v1/auth/me")  
def get_current_user():
    """获取当前用户信息"""
    return {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "real_name": "系统管理员",
        "permissions": ["user.read", "institution.read", "candidate.read"]
    }

# 机构管理API
@app.get("/api/v1/institutions")
def get_institutions():
    """获取机构列表"""
    return [
        {"id": 1, "name": "测试培训机构1", "contact_person": "张三", "phone": "13800138001"},
        {"id": 2, "name": "测试培训机构2", "contact_person": "李四", "phone": "13800138002"}
    ]

# 考场状态API（小程序公共看板）
@app.get("/api/v1/public/venues-status")
def get_venues_status():
    """获取考场实时状态"""
    return [
        {
            "venue_id": 1,
            "venue_name": "多旋翼A号实操场",
            "venue_type": "实操",
            "status": "进行中",
            "current_candidate_name": "李*",
            "waiting_count": 12,
            "next_start_time": "14:30"
        },
        {
            "venue_id": 2,
            "venue_name": "理论一号教室", 
            "venue_type": "理论",
            "status": "空闲",
            "current_candidate_name": None,
            "waiting_count": 0,
            "next_start_time": "15:00"
        }
    ]