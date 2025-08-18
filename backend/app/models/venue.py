"""
考场相关数据模型
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from ..config.database import Base


class VenueStatus(enum.Enum):
    """考场状态枚举"""
    AVAILABLE = "available"      # 可用
    OCCUPIED = "occupied"        # 占用中
    MAINTENANCE = "maintenance"  # 维护中
    DISABLED = "disabled"        # 已禁用


class Venue(Base):
    """考场模型"""
    __tablename__ = "venues"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 基本信息
    name = Column(String(100), nullable=False)
    code = Column(String(50), nullable=False, index=True)
    description = Column(Text)
    
    # 容量信息
    capacity = Column(Integer, nullable=False, default=20)  # 最大容纳人数
    current_count = Column(Integer, default=0)  # 当前人数
    
    # 地理位置
    building = Column(String(50))
    floor = Column(String(20))
    room_number = Column(String(20))
    
    # 设备信息
    equipment = Column(JSON)  # 考场设备清单
    facilities = Column(JSON)  # 设施配置
    
    # 状态
    status = Column(Enum(VenueStatus), default=VenueStatus.AVAILABLE)
    is_active = Column(Boolean, default=True)
    
    # 关联机构
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    institution = relationship("Institution", back_populates="venues")
    
    # 二维码信息
    qr_code = Column(String(255))  # 考场二维码
    
    # 时间戳
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 反向关系
    exam_sessions = relationship("ExamSession", back_populates="venue")
    checkins = relationship("CheckIn", back_populates="venue")
    
    def __repr__(self):
        return f"<Venue {self.name}>"