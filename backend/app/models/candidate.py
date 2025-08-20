"""
考生数据模型
"""
import enum
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..config.database import Base


class CandidateStatus(enum.Enum):
    """考生状态枚举"""
    PENDING_SCHEDULE = "pending_schedule"      # 待安排
    SCHEDULED = "scheduled"                    # 已安排
    IN_THEORY = "in_theory"                   # 理论考试中
    IN_PRACTICAL = "in_practical"             # 实操考试中
    THEORY_COMPLETED = "theory_completed"      # 理论已完成
    PRACTICAL_COMPLETED = "practical_completed"  # 实操已完成
    ALL_COMPLETED = "all_completed"           # 全部完成


class Candidate(Base):
    """考生模型"""
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 基本信息
    name = Column(String(50), nullable=False, index=True)
    id_card = Column(String(18), nullable=False, unique=True, index=True)
    phone = Column(String(11), nullable=False, index=True)
    email = Column(String(100), index=True)
    
    # 微信信息
    wechat_openid = Column(String(100), unique=True, index=True)
    wechat_nickname = Column(String(100))
    
    # 关联信息
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False, index=True)
    exam_product_id = Column(Integer, ForeignKey("exam_products.id"), nullable=False, index=True)
    
    # 状态信息
    status = Column(Enum(CandidateStatus), default=CandidateStatus.PENDING_SCHEDULE, nullable=False, index=True)
    
    # 报名信息
    registration_date = Column(DateTime(timezone=True), server_default=func.now())
    registration_number = Column(String(50), unique=True, index=True)
    
    # 备注
    remarks = Column(Text)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    
    # 关系定义
    institution = relationship("Institution", back_populates="candidates")
    exam_product = relationship("ExamProduct", back_populates="candidates")
    creator = relationship("User", foreign_keys=[created_by])
    schedules = relationship("Schedule", secondary="schedule_candidates", back_populates="candidates")
    checkins = relationship("CheckIn", back_populates="candidate")
    
    def __repr__(self):
        return f"<Candidate(id={self.id}, name='{self.name}', id_card='{self.id_card}', status='{self.status}')>"