"""
日程数据模式
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date


class ScheduleBase(BaseModel):
    """日程基础模式"""
    registration_id: int = Field(..., description="报名ID")
    exam_product_id: int = Field(..., description="考试产品ID")
    venue_id: int = Field(..., description="考场ID")
    schedule_date: date = Field(..., description="安排日期")
    start_time: datetime = Field(..., description="开始时间")
    end_time: datetime = Field(..., description="结束时间")
    queue_position: Optional[int] = Field(0, description="排队位置")


class ScheduleCreate(ScheduleBase):
    """创建日程模式"""
    
    @validator('end_time')
    def validate_end_time(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('结束时间必须晚于开始时间')
        return v


class ScheduleUpdate(BaseModel):
    """更新日程模式"""
    registration_id: Optional[int] = Field(None, description="报名ID")
    exam_product_id: Optional[int] = Field(None, description="考试产品ID")
    venue_id: Optional[int] = Field(None, description="考场ID")
    schedule_date: Optional[date] = Field(None, description="安排日期")
    start_time: Optional[datetime] = Field(None, description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")
    queue_position: Optional[int] = Field(None, description="排队位置")
    status: Optional[str] = Field(None, description="状态")


class ScheduleResponse(ScheduleBase):
    """日程响应模式"""
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    
    # 关联信息
    candidate_name: Optional[str] = None
    candidate_id_card: Optional[str] = None
    exam_product_name: Optional[str] = None
    venue_name: Optional[str] = None
    institution_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class BatchScheduleCreate(BaseModel):
    """批量创建日程模式"""
    registration_ids: List[int] = Field(..., description="报名ID列表")
    exam_product_id: int = Field(..., description="考试产品ID")
    venue_id: int = Field(..., description="考场ID")
    start_time: datetime = Field(..., description="开始时间")
    duration_minutes: int = Field(15, description="单个考试时长（分钟）", ge=1, le=480)


class ScheduleList(BaseModel):
    """日程列表响应模式"""
    items: List[ScheduleResponse]
    total: int
    page: int
    size: int
    pages: int


class ScheduleStatistics(BaseModel):
    """日程统计信息模式"""
    total_schedules: int
    status_stats: List[Dict[str, Any]]
    venue_stats: List[Dict[str, Any]]
    institution_stats: Optional[List[Dict[str, Any]]] = None


class ScheduleConflictCheck(BaseModel):
    """日程冲突检查模式"""
    venue_id: int = Field(..., description="考场ID")
    start_time: datetime = Field(..., description="开始时间")
    end_time: datetime = Field(..., description="结束时间")
    exclude_schedule_id: Optional[int] = Field(None, description="排除的日程ID")


class ScheduleConflictResult(BaseModel):
    """日程冲突检查结果模式"""
    has_conflict: bool
    conflicting_schedules: List[ScheduleResponse]
    message: str
