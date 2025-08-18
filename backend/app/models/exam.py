"""
考试相关数据模型
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON, Enum, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from ..config.database import Base


class ExamStatus(enum.Enum):
    """考试状态枚举"""
    DRAFT = "draft"              # 草稿
    PUBLISHED = "published"      # 已发布
    REGISTRATION = "registration"  # 报名中
    SCHEDULED = "scheduled"      # 已排期
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"      # 已完成
    CANCELLED = "cancelled"      # 已取消


class RegistrationStatus(enum.Enum):
    """报名状态枚举"""
    PENDING = "pending"          # 待审核
    APPROVED = "approved"        # 已通过
    REJECTED = "rejected"        # 已拒绝
    CANCELLED = "cancelled"      # 已取消


class Exam(Base):
    """考试模型"""
    __tablename__ = "exams"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 基本信息
    title = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    subject = Column(String(100))  # 考试科目
    
    # 考试配置
    duration_minutes = Column(Integer, nullable=False)  # 考试时长（分钟）
    total_score = Column(Numeric(5, 2), default=100)  # 总分
    passing_score = Column(Numeric(5, 2), default=60)  # 及格分
    
    # 报名配置
    max_candidates = Column(Integer, default=1000)  # 最大报名人数
    registration_fee = Column(Numeric(10, 2), default=0)  # 报名费用
    
    # 时间配置
    registration_start = Column(DateTime)  # 报名开始时间
    registration_end = Column(DateTime)    # 报名截止时间
    exam_start = Column(DateTime)          # 考试开始时间
    exam_end = Column(DateTime)            # 考试结束时间
    
    # 状态
    status = Column(Enum(ExamStatus), default=ExamStatus.DRAFT)
    is_active = Column(Boolean, default=True)
    
    # 关联机构
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    institution = relationship("Institution", back_populates="exams")
    
    # 配置信息
    config = Column(JSON)  # 考试特殊配置
    
    # 时间戳
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 反向关系
    exam_sessions = relationship("ExamSession", back_populates="exam")
    registrations = relationship("ExamRegistration", back_populates="exam")
    
    def __repr__(self):
        return f"<Exam {self.title}>"


class ExamSession(Base):
    """考试场次模型"""
    __tablename__ = "exam_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 关联考试和考场
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    exam = relationship("Exam", back_populates="exam_sessions")
    
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    venue = relationship("Venue", back_populates="exam_sessions")
    
    # 场次信息
    session_name = Column(String(100))  # 场次名称
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    
    # 容量控制
    max_candidates = Column(Integer, nullable=False)
    current_count = Column(Integer, default=0)
    
    # 监考员配置
    examiners = Column(JSON)  # 监考员列表
    
    # 状态
    is_active = Column(Boolean, default=True)
    
    # 时间戳
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 反向关系
    registrations = relationship("ExamRegistration", back_populates="exam_session")
    checkins = relationship("CheckIn", back_populates="exam_session")
    
    def __repr__(self):
        return f"<ExamSession {self.session_name}>"


class ExamRegistration(Base):
    """考试报名模型"""
    __tablename__ = "exam_registrations"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 关联用户和考试
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="exam_registrations")
    
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    exam = relationship("Exam", back_populates="registrations")
    
    exam_session_id = Column(Integer, ForeignKey("exam_sessions.id"))
    exam_session = relationship("ExamSession", back_populates="registrations")
    
    # 报名信息
    registration_number = Column(String(50), unique=True, nullable=False)  # 报名号
    candidate_number = Column(String(50), unique=True, nullable=False)     # 准考证号
    
    # 状态
    status = Column(Enum(RegistrationStatus), default=RegistrationStatus.PENDING)
    
    # 额外信息
    notes = Column(Text)
    data = Column(JSON)  # 额外的报名数据
    
    # 时间戳
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 反向关系
    checkins = relationship("CheckIn", back_populates="registration")
    
    def __repr__(self):
        return f"<ExamRegistration {self.registration_number}>"