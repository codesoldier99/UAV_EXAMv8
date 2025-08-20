"""
用户相关数据模型
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from ..config.database import Base


class UserRole(enum.Enum):
    """用户角色枚举"""
    SUPER_ADMIN = "super_admin"      # 超级管理员
    ADMIN = "admin"                  # 管理员
    OPERATOR = "operator"            # 操作员
    EXAMINER = "examiner"            # 监考员
    CANDIDATE = "candidate"          # 考生


class User(Base):
    """用户模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(20), unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # 基本信息
    real_name = Column(String(50))
    full_name = Column(String(50))  # 添加全名字段以兼容RBAC
    id_card = Column(String(20))
    avatar = Column(String(255))
    
    # 角色权限
    role = Column(Enum(UserRole), default=UserRole.CANDIDATE)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # 关联机构
    institution_id = Column(Integer, ForeignKey("institutions.id"))
    
    # 微信信息
    wechat_openid = Column(String(100), unique=True, index=True)
    wechat_unionid = Column(String(100), unique=True, index=True)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # 关系定义
    institution = relationship("Institution", back_populates="users")
    exam_registrations = relationship("ExamRegistration", back_populates="user")
    checkins = relationship("CheckIn", back_populates="user")
    
    # RBAC 关系
    roles = relationship("Role", secondary="user_roles", back_populates="users")
    
    def __repr__(self):
        return f"<User {self.username}>"
    
    def has_permission(self, permission_name: str) -> bool:
        """检查用户是否有指定权限"""
        for role in self.roles:
            for permission in role.permissions:
                if permission.name == permission_name:
                    return True
        return False
    
    def has_role(self, role_name: str) -> bool:
        """检查用户是否有指定角色"""
        return any(role.name == role_name for role in self.roles)