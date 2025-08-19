"""
签到相关数据模型
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from ..config.database import Base


class CheckInStatus(enum.Enum):
    """签到状态枚举"""
    SUCCESS = "success"          # 签到成功
    LATE = "late"               # 迟到签到
    FAILED = "failed"           # 签到失败
    INVALID = "invalid"         # 无效签到


class CheckInMethod(enum.Enum):
    """签到方式枚举"""
    QR_CODE = "qr_code"         # 二维码签到
    MANUAL = "manual"           # 手动签到
    NFC = "nfc"                # NFC签到
    BIOMETRIC = "biometric"     # 生物识别签到


class CheckIn(Base):
    """签到记录模型"""
    __tablename__ = "checkins"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 关联信息
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="checkins")
    
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    venue = relationship("Venue", back_populates="checkins")
    
    exam_session_id = Column(Integer, ForeignKey("exam_sessions.id"), nullable=False)
    exam_session = relationship("ExamSession", back_populates="checkins")
    
    registration_id = Column(Integer, ForeignKey("exam_registrations.id"), nullable=False)
    registration = relationship("ExamRegistration", back_populates="checkins")
    
    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=False)
    schedule = relationship("Schedule", back_populates="checkins")
    
    # 签到信息
    checkin_time = Column(DateTime, nullable=False, server_default=func.now())
    method = Column(Enum(CheckInMethod), default=CheckInMethod.QR_CODE)
    status = Column(Enum(CheckInStatus), default=CheckInStatus.SUCCESS)
    
    # 位置信息
    latitude = Column(String(20))   # 纬度
    longitude = Column(String(20))  # 经度
    location_address = Column(Text)  # 地址描述
    
    # 设备信息
    device_info = Column(JSON)  # 签到设备信息
    ip_address = Column(String(50))  # IP地址
    user_agent = Column(Text)   # 用户代理
    
    # 额外数据
    notes = Column(Text)        # 备注
    data = Column(JSON)         # 额外数据
    
    # 时间戳
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<CheckIn {self.user.username} - {self.checkin_time}>"