"""
微信小程序数据模式
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class WeChatLoginRequest(BaseModel):
    """微信登录请求"""
    id_card: str = Field(..., description="身份证号")
    openid: str = Field(..., description="微信openid")


class WeChatLoginResponse(BaseModel):
    """微信登录响应"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict


class CandidateScheduleResponse(BaseModel):
    """考生日程响应"""
    id: int
    schedule_date: datetime
    start_time: datetime
    end_time: datetime
    status: str
    queue_position: int
    venue_name: str
    venue_type: str
    exam_product_name: str
    exam_type: str
    
    class Config:
        from_attributes = True


class VenueStatusResponse(BaseModel):
    """考场状态响应"""
    venue_id: int
    venue_name: str
    venue_type: str
    status: str
    current_candidate: Optional[str]
    waiting_count: int
    next_start_time: Optional[str]
    capacity: int
    
    class Config:
        from_attributes = True


class CheckInRequest(BaseModel):
    """签到请求"""
    schedule_id: int = Field(..., description="日程ID")
    venue_id: int = Field(..., description="考场ID")


class CheckInResponse(BaseModel):
    """签到响应"""
    success: bool
    message: str
    candidate_name: Optional[str]
    schedule_info: Optional[dict]
    checkin_time: datetime


class QueuePositionResponse(BaseModel):
    """排队位置响应"""
    venue_name: str
    position: int
    total_waiting: int
    estimated_wait_time: Optional[int]  # 预计等待时间（分钟）
