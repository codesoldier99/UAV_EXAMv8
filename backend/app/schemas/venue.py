"""
考场数据模式
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class VenueBase(BaseModel):
    """考场基础模式"""
    name: str = Field(..., description="考场名称", max_length=100)
    code: str = Field(..., description="考场代码", max_length=50)
    description: Optional[str] = Field(None, description="考场描述")
    capacity: int = Field(..., description="最大容纳人数", ge=1)
    building: Optional[str] = Field(None, description="建筑物", max_length=50)
    floor: Optional[str] = Field(None, description="楼层", max_length=20)
    room_number: Optional[str] = Field(None, description="房间号", max_length=20)
    status: Optional[str] = Field("available", description="考场状态")
    institution_id: int = Field(..., description="机构ID")
    equipment: Optional[Dict[str, Any]] = Field(None, description="设备信息")
    facilities: Optional[Dict[str, Any]] = Field(None, description="设施配置")
    is_active: Optional[bool] = Field(True, description="是否启用")


class VenueCreate(VenueBase):
    """创建考场模式"""
    pass


class VenueUpdate(BaseModel):
    """更新考场模式"""
    name: Optional[str] = Field(None, description="考场名称", max_length=100)
    code: Optional[str] = Field(None, description="考场代码", max_length=50)
    description: Optional[str] = Field(None, description="考场描述")
    capacity: Optional[int] = Field(None, description="最大容纳人数", ge=1)
    building: Optional[str] = Field(None, description="建筑物", max_length=50)
    floor: Optional[str] = Field(None, description="楼层", max_length=20)
    room_number: Optional[str] = Field(None, description="房间号", max_length=20)
    status: Optional[str] = Field(None, description="考场状态")
    institution_id: Optional[int] = Field(None, description="机构ID")
    equipment: Optional[Dict[str, Any]] = Field(None, description="设备信息")
    facilities: Optional[Dict[str, Any]] = Field(None, description="设施配置")
    is_active: Optional[bool] = Field(None, description="是否启用")


class VenueResponse(VenueBase):
    """考场响应模式"""
    id: int
    current_count: int
    qr_code: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class VenueList(BaseModel):
    """考场列表响应模式"""
    items: List[VenueResponse]
    total: int
    page: int
    size: int
    pages: int


class VenueStatusInfo(BaseModel):
    """考场状态信息模式"""
    venue_id: int
    venue_name: str
    venue_type: str
    status: str
    capacity: int
    current_count: int
    waiting_count: int
    current_candidate: Optional[str]
    next_start_time: Optional[str]
    last_updated: str


class VenueStatistics(BaseModel):
    """考场统计信息模式"""
    total_venues: int
    status_stats: List[Dict[str, Any]]
    institution_stats: List[Dict[str, Any]]
