"""
初始化RBAC权限系统数据
"""
from sqlalchemy.orm import Session
from ..models.rbac import Role, Permission
from ..models.user import User
import hashlib


def init_permissions(db: Session):
    """初始化权限数据"""
    permissions_data = [
        # 用户管理权限
        {"name": "user:create", "display_name": "创建用户", "resource": "user", "action": "create", "description": "创建系统用户"},
        {"name": "user:read", "display_name": "查看用户", "resource": "user", "action": "read", "description": "查看用户信息"},
        {"name": "user:update", "display_name": "更新用户", "resource": "user", "action": "update", "description": "更新用户信息"},
        {"name": "user:delete", "display_name": "删除用户", "resource": "user", "action": "delete", "description": "删除系统用户"},
        
        # 机构管理权限
        {"name": "institution:create", "display_name": "创建机构", "resource": "institution", "action": "create", "description": "创建考试机构"},
        {"name": "institution:read", "display_name": "查看机构", "resource": "institution", "action": "read", "description": "查看机构信息"},
        {"name": "institution:update", "display_name": "更新机构", "resource": "institution", "action": "update", "description": "更新机构信息"},
        {"name": "institution:delete", "display_name": "删除机构", "resource": "institution", "action": "delete", "description": "删除考试机构"},
        
        # 考生管理权限
        {"name": "candidate:create", "display_name": "创建考生", "resource": "candidate", "action": "create", "description": "创建考生信息"},
        {"name": "candidate:read", "display_name": "查看考生", "resource": "candidate", "action": "read", "description": "查看考生信息"},
        {"name": "candidate:update", "display_name": "更新考生", "resource": "candidate", "action": "update", "description": "更新考生信息"},
        {"name": "candidate:delete", "display_name": "删除考生", "resource": "candidate", "action": "delete", "description": "删除考生信息"},
        {"name": "candidate:import", "display_name": "批量导入考生", "resource": "candidate", "action": "import", "description": "批量导入考生数据"},
        
        # 考试产品权限
        {"name": "exam_product:create", "display_name": "创建考试产品", "resource": "exam_product", "action": "create", "description": "创建考试产品"},
        {"name": "exam_product:read", "display_name": "查看考试产品", "resource": "exam_product", "action": "read", "description": "查看考试产品"},
        {"name": "exam_product:update", "display_name": "更新考试产品", "resource": "exam_product", "action": "update", "description": "更新考试产品"},
        {"name": "exam_product:delete", "display_name": "删除考试产品", "resource": "exam_product", "action": "delete", "description": "删除考试产品"},
        
        # 场地管理权限
        {"name": "venue:create", "display_name": "创建场地", "resource": "venue", "action": "create", "description": "创建考试场地"},
        {"name": "venue:read", "display_name": "查看场地", "resource": "venue", "action": "read", "description": "查看场地信息"},
        {"name": "venue:update", "display_name": "更新场地", "resource": "venue", "action": "update", "description": "更新场地信息"},
        {"name": "venue:delete", "display_name": "删除场地", "resource": "venue", "action": "delete", "description": "删除考试场地"},
        
        # 日程管理权限
        {"name": "schedule:create", "display_name": "创建日程", "resource": "schedule", "action": "create", "description": "创建考试日程"},
        {"name": "schedule:read", "display_name": "查看日程", "resource": "schedule", "action": "read", "description": "查看考试日程"},
        {"name": "schedule:update", "display_name": "更新日程", "resource": "schedule", "action": "update", "description": "更新考试日程"},
        {"name": "schedule:delete", "display_name": "删除日程", "resource": "schedule", "action": "delete", "description": "删除考试日程"},
        
        # 签到管理权限
        {"name": "checkin:create", "display_name": "执行签到", "resource": "checkin", "action": "create", "description": "执行考生签到"},
        {"name": "checkin:read", "display_name": "查看签到", "resource": "checkin", "action": "read", "description": "查看签到记录"},
        
        # 系统管理权限
        {"name": "system:config", "display_name": "系统配置", "resource": "system", "action": "config", "description": "系统配置管理"},
        {"name": "system:monitor", "display_name": "系统监控", "resource": "system", "action": "monitor", "description": "系统监控查看"},
    ]
    
    for perm_data in permissions_data:
        existing = db.query(Permission).filter(Permission.name == perm_data["name"]).first()
        if not existing:
            permission = Permission(**perm_data)
            db.add(permission)
    
    db.commit()


def init_roles(db: Session):
    """初始化角色数据"""
    roles_data = [
        {
            "name": "super_admin",
            "display_name": "超级管理员",
            "description": "系统超级管理员，拥有所有权限"
        },
        {
            "name": "exam_admin",
            "display_name": "考务管理员", 
            "description": "考务管理员，负责考试安排和监控"
        },
        {
            "name": "institution_user",
            "display_name": "机构用户",
            "description": "机构用户，负责考生报名和管理"
        },
        {
            "name": "staff",
            "display_name": "考务人员",
            "description": "考务人员，负责现场签到和监考"
        },
        {
            "name": "candidate",
            "display_name": "考生",
            "description": "考生用户，查看个人信息和考试安排"
        }
    ]
    
    for role_data in roles_data:
        existing = db.query(Role).filter(Role.name == role_data["name"]).first()
        if not existing:
            role = Role(**role_data)
            db.add(role)
    
    db.commit()


def assign_role_permissions(db: Session):
    """分配角色权限"""
    # 获取所有权限
    all_permissions = db.query(Permission).all()
    
    # 超级管理员：所有权限
    super_admin_role = db.query(Role).filter(Role.name == "super_admin").first()
    if super_admin_role:
        super_admin_role.permissions = all_permissions
    
    # 考务管理员：除用户管理外的所有权限
    exam_admin_role = db.query(Role).filter(Role.name == "exam_admin").first()
    if exam_admin_role:
        exam_admin_permissions = [p for p in all_permissions if not p.resource == "user" or p.action == "read"]
        exam_admin_role.permissions = exam_admin_permissions
    
    # 机构用户：考生管理、查看其他资源
    institution_role = db.query(Role).filter(Role.name == "institution_user").first()
    if institution_role:
        institution_permissions = []
        for p in all_permissions:
            if p.resource == "candidate":  # 考生管理权限
                institution_permissions.append(p)
            elif p.action == "read":  # 其他资源的读权限
                institution_permissions.append(p)
        institution_role.permissions = institution_permissions
    
    # 考务人员：签到权限和基本查看权限
    staff_role = db.query(Role).filter(Role.name == "staff").first()
    if staff_role:
        staff_permissions = []
        for p in all_permissions:
            if p.resource == "checkin":  # 签到权限
                staff_permissions.append(p)
            elif p.action == "read" and p.resource in ["candidate", "schedule", "venue"]:
                staff_permissions.append(p)
        staff_role.permissions = staff_permissions
    
    # 考生：只读个人相关信息
    candidate_role = db.query(Role).filter(Role.name == "candidate").first()
    if candidate_role:
        candidate_permissions = []
        for p in all_permissions:
            if p.action == "read" and p.resource in ["candidate", "schedule", "venue", "exam_product"]:
                candidate_permissions.append(p)
        candidate_role.permissions = candidate_permissions
    
    db.commit()


def create_default_admin(db: Session):
    """创建默认管理员用户"""
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        # 创建管理员用户
        admin_user = User(
            username="admin",
            email="admin@example.com",
            full_name="系统管理员",
            real_name="系统管理员",
            password_hash=hashlib.sha256("admin123".encode()).hexdigest(),
            is_active=True,
            is_verified=True
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        # 分配超级管理员角色
        super_admin_role = db.query(Role).filter(Role.name == "super_admin").first()
        if super_admin_role:
            admin_user.roles.append(super_admin_role)
            db.commit()


def init_rbac_system(db: Session):
    """初始化完整的RBAC系统"""
    print("🔐 初始化RBAC权限系统...")
    
    # 1. 初始化权限
    print("📝 创建权限数据...")
    init_permissions(db)
    
    # 2. 初始化角色
    print("👥 创建角色数据...")
    init_roles(db)
    
    # 3. 分配角色权限
    print("🔗 分配角色权限...")
    assign_role_permissions(db)
    
    # 4. 创建默认管理员
    print("👤 创建默认管理员...")
    create_default_admin(db)
    
    print("✅ RBAC权限系统初始化完成")