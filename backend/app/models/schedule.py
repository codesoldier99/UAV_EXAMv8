"""
考试日程安排数据模型
"""
import enum
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Date, Time, Table, Numeric, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..config.database import Base


class ScheduleStatus(enum.Enum):
    """日程状态枚举"""
    PENDING = "pending"                # 待进行
    READY = "ready"                   # 准备就绪
    IN_PROGRESS = "in_progress"       # 进行中
    COMPLETED = "completed"           # 已完成
    CANCELLED = "cancelled"           # 已取消


# 日程考生关联表
schedule_candidates = Table(
    'schedule_candidates',
    Base.metadata,
    Column('schedule_id', Integer, ForeignKey('schedules.id'), primary_key=True),
    Column('candidate_id', Integer, ForeignKey('candidates.id'), primary_key=True),
    Column('assigned_at', DateTime(timezone=True), server_default=func.now())
)


class Schedule(Base):
    """考试日程安排模型"""
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 基本信息
    activity_name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    
    # 时间安排
    exam_date = Column(Date, nullable=False, index=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    # 关联信息
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False, index=True)
    exam_product_id = Column(Integer, ForeignKey("exam_products.id"), nullable=False, index=True)
    institution_id = Column(Integer, ForeignKey("institutions.id"), index=True)
    
    # 容量管理
    max_candidates = Column(Integer, default=1)  # 最大考生数
    candidate_count = Column(Integer, default=0)  # 当前考生数
    
    # 状态信息
    status = Column(Enum(ScheduleStatus), default=ScheduleStatus.PENDING, nullable=False, index=True)
    
    # 考试设置
    is_theory = Column(Boolean, default=False)     # 是否为理论考试
    is_practical = Column(Boolean, default=True)   # 是否为实操考试
    
    # 费用信息
    exam_fee = Column(Numeric(10, 2), default=0)
    
    # 备注
    remarks = Column(Text)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    
    # 关系定义
    venue = relationship("Venue", back_populates="schedules")
    exam_product = relationship("ExamProduct", back_populates="schedules")
    institution = relationship("Institution", back_populates="schedules")
    creator = relationship("User", foreign_keys=[created_by])
    candidates = relationship("Candidate", secondary=schedule_candidates, back_populates="schedules")
    checkins = relationship("CheckIn", back_populates="schedule")
    
    def __repr__(self):
        return f"<Schedule(id={self.id}, activity='{self.activity_name}', date='{self.exam_date}', time='{self.start_time}-{self.end_time}')>"
    
    @property
    def is_full(self):
        """检查是否已满员"""
        return self.candidate_count >= self.max_candidates
    
    @property
    def available_slots(self):
        """获取可用名额"""
        return max(0, self.max_candidates - self.candidate_count)