"""
考场管理API路由
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..config.database import get_db
from ..services.auth_service import AuthService
from ..services.venue_service import VenueService
from ..models.user import User, UserRole
from ..schemas.venue import (
    VenueCreate,
    VenueUpdate,
    VenueResponse,
    VenueList
)

router = APIRouter(prefix="/venues", tags=["考场管理"])


@router.get("/", response_model=List[VenueResponse], summary="获取考场列表")
async def get_venues(
    skip: int = 0,
    limit: int = 100,
    institution_id: Optional[int] = None,
    status: Optional[str] = None,
    venue_type: Optional[str] = None,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取考场列表"""
    service = VenueService(db)
    
    # 机构用户只能查看本机构的考场
    if current_user.role == UserRole.OPERATOR:
        institution_id = current_user.institution_id
    
    venues = service.get_venues(
        skip=skip,
        limit=limit,
        institution_id=institution_id,
        status=status,
        venue_type=venue_type
    )
    return venues


@router.get("/{venue_id}", response_model=VenueResponse, summary="获取考场详情")
async def get_venue(
    venue_id: int,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取考场详情"""
    service = VenueService(db)
    venue = service.get_venue_by_id(venue_id)
    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="考场不存在"
        )
    
    # 检查权限：机构用户只能查看本机构的考场
    if current_user.role == UserRole.OPERATOR and venue.institution_id != current_user.institution_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问该考场信息"
        )
    
    return venue


@router.post("/", response_model=VenueResponse, summary="创建考场")
async def create_venue(
    venue_data: VenueCreate,
    current_user: User = Depends(AuthService.require_admin),
    db: Session = Depends(get_db)
):
    """创建新考场"""
    service = VenueService(db)
    try:
        venue = service.create_venue(venue_data)
        return venue
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{venue_id}", response_model=VenueResponse, summary="更新考场信息")
async def update_venue(
    venue_id: int,
    venue_data: VenueUpdate,
    current_user: User = Depends(AuthService.require_admin),
    db: Session = Depends(get_db)
):
    """更新考场信息"""
    service = VenueService(db)
    try:
        venue = service.update_venue(venue_id, venue_data)
        if not venue:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="考场不存在"
            )
        return venue
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{venue_id}", summary="删除考场")
async def delete_venue(
    venue_id: int,
    current_user: User = Depends(AuthService.require_admin),
    db: Session = Depends(get_db)
):
    """删除考场"""
    service = VenueService(db)
    try:
        success = service.delete_venue(venue_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="考场不存在"
            )
        return {"message": "考场删除成功"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{venue_id}/toggle-status", summary="切换考场状态")
async def toggle_venue_status(
    venue_id: int,
    current_user: User = Depends(AuthService.require_admin),
    db: Session = Depends(get_db)
):
    """切换考场的可用/维护状态"""
    service = VenueService(db)
    try:
        venue = service.toggle_venue_status(venue_id)
        if not venue:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="考场不存在"
            )
        return {
            "message": f"考场状态已切换为{venue.status.value}",
            "venue": venue
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{venue_id}/schedules", summary="获取考场日程")
async def get_venue_schedules(
    venue_id: int,
    date: Optional[str] = None,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取考场的日程安排"""
    service = VenueService(db)
    
    # 解析日期
    schedule_date = None
    if date:
        try:
            schedule_date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="日期格式错误，请使用YYYY-MM-DD格式"
            )
    
    schedules = service.get_venue_schedules(venue_id, schedule_date)
    return schedules


@router.get("/{venue_id}/current-status", summary="获取考场当前状态")
async def get_venue_current_status(
    venue_id: int,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取考场当前状态信息"""
    service = VenueService(db)
    status_info = service.get_venue_current_status(venue_id)
    return status_info
