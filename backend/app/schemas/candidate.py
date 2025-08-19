"""
考生数据模式
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime


class CandidateBase(BaseModel):
    """考生基础模式"""
    real_name: str = Field(..., description="考生姓名", max_length=50)
    id_card: str = Field(..., description="身份证号", max_length=20)
    exam_product_id: int = Field(..., description="考试产品ID")
    institution_id: int = Field(..., description="机构ID")
    phone: Optional[str] = Field(None, description="手机号", max_length=20)
    email: Optional[EmailStr] = Field(None, description="邮箱")


class CandidateCreate(CandidateBase):
    """创建考生模式"""
    pass


class CandidateUpdate(BaseModel):
    """更新考生模式"""
    real_name: Optional[str] = Field(None, description="考生姓名", max_length=50)
    id_card: Optional[str] = Field(None, description="身份证号", max_length=20)
    exam_product_id: Optional[int] = Field(None, description="考试产品ID")
    institution_id: Optional[int] = Field(None, description="机构ID")
    phone: Optional[str] = Field(None, description="手机号", max_length=20)
    email: Optional[EmailStr] = Field(None, description="邮箱")


class CandidateResponse(CandidateBase):
    """考生响应模式"""
    id: int
    username: str
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True


class CandidateList(BaseModel):
    """考生列表响应模式"""
    items: List[CandidateResponse]
    total: int
    page: int
    size: int
    pages: int


class BatchImportResult(BaseModel):
    """批量导入结果模式"""
    total: int = Field(..., description="总记录数")
    success_count: int = Field(..., description="成功导入数")
    failed_count: int = Field(..., description="失败数")
    errors: List[Dict[str, Any]] = Field(..., description="错误详情")


class CandidateStatistics(BaseModel):
    """考生统计信息模式"""
    total_candidates: int
    institution_stats: List[Dict[str, Any]]
    product_stats: List[Dict[str, Any]]
    status_stats: List[Dict[str, Any]]
