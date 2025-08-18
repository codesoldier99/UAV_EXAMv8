"""
机构相关数据模型
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..config.database import Base


class Institution(Base):
    """考试机构模型"""
    __tablename__ = "institutions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 基本信息
    name = Column(String(100), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    type = Column(String(50))  # 机构类型：学校、培训机构、企业等
    
    # 联系信息
    contact_person = Column(String(50))
    contact_phone = Column(String(20))
    contact_email = Column(String(100))
    
    # 地址信息
    province = Column(String(50))
    city = Column(String(50))
    district = Column(String(50))
    address = Column(Text)
    
    # 认证信息
    license_number = Column(String(100))  # 办学许可证号
    business_license = Column(String(100))  # 营业执照号
    
    # 状态
    is_active = Column(Boolean, default=True)
    is_approved = Column(Boolean, default=False)
    
    # 配置信息
    config = Column(JSON)  # 机构特殊配置
    
    # 时间戳
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 反向关系
    users = relationship("User", back_populates="institution")
    venues = relationship("Venue", back_populates="institution")
    exams = relationship("Exam", back_populates="institution")
    
    def __repr__(self):
        return f"<Institution {self.name}>"