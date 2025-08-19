"""
考试产品数据模式
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ExamProductBase(BaseModel):
    """考试产品基础模式"""
    name: str = Field(..., description="考试产品名称", max_length=200)
    code: str = Field(..., description="考试产品代码", max_length=50)
    description: Optional[str] = Field(None, description="考试产品描述")
    duration_minutes: int = Field(..., description="考试时长（分钟）", gt=0)
    exam_type: str = Field(..., description="考试类型（理论/实操）", max_length=50)
    is_active: Optional[bool] = Field(True, description="是否启用")


class ExamProductCreate(ExamProductBase):
    """创建考试产品模式"""
    pass


class ExamProductUpdate(BaseModel):
    """更新考试产品模式"""
    name: Optional[str] = Field(None, description="考试产品名称", max_length=200)
    code: Optional[str] = Field(None, description="考试产品代码", max_length=50)
    description: Optional[str] = Field(None, description="考试产品描述")
    duration_minutes: Optional[int] = Field(None, description="考试时长（分钟）", gt=0)
    exam_type: Optional[str] = Field(None, description="考试类型（理论/实操）", max_length=50)
    is_active: Optional[bool] = Field(None, description="是否启用")


class ExamProductResponse(ExamProductBase):
    """考试产品响应模式"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ExamProductList(BaseModel):
    """考试产品列表响应模式"""
    items: List[ExamProductResponse]
    total: int
    page: int
    size: int
    pages: int
