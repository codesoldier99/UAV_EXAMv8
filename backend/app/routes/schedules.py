"""
日程管理API路由
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date

from ..config.database import get_db
from ..services.auth_service import AuthService
from ..services.schedule_service import ScheduleService
from ..models.user import User, UserRole
from ..schemas.schedule import (
    ScheduleCreate,
    ScheduleUpdate,
    ScheduleResponse,
    BatchScheduleCreate,
    ScheduleStatistics
)

router = APIRouter(prefix="/schedules", tags=["日程管理"])


@router.get("/", response_model=List[ScheduleResponse], summary="获取日程列表")
async def get_schedules(
    skip: int = 0,
    limit: int = 100,
    venue_id: Optional[int] = None,
    date: Optional[str] = None,
    status: Optional[str] = None,
    institution_id: Optional[int] = None,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取日程列表"""
    service = ScheduleService(db)
    
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
    
    # 机构用户只能查看本机构的日程
    if current_user.role == UserRole.OPERATOR:
        institution_id = current_user.institution_id
    
    schedules = service.get_schedules(
        skip=skip,
        limit=limit,
        venue_id=venue_id,
        date=schedule_date,
        status=status,
        institution_id=institution_id
    )
    return schedules


@router.get("/{schedule_id}", response_model=ScheduleResponse, summary="获取日程详情")
async def get_schedule(
    schedule_id: int,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取日程详情"""
    service = ScheduleService(db)
    schedule = service.get_schedule_by_id(schedule_id)
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="日程不存在"
        )
    
    # 检查权限：机构用户只能查看本机构的日程
    if (current_user.role == UserRole.OPERATOR and 
        schedule.registration.user.institution_id != current_user.institution_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问该日程信息"
        )
    
    return schedule


@router.post("/", response_model=ScheduleResponse, summary="创建日程")
async def create_schedule(
    schedule_data: ScheduleCreate,
    current_user: User = Depends(AuthService.require_admin),
    db: Session = Depends(get_db)
):
    """创建新日程"""
    service = ScheduleService(db)
    try:
        schedule = service.create_schedule(
            registration_id=schedule_data.registration_id,
            exam_product_id=schedule_data.exam_product_id,
            venue_id=schedule_data.venue_id,
            start_time=schedule_data.start_time,
            end_time=schedule_data.end_time
        )
        return schedule
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/batch", summary="批量创建日程")
async def batch_create_schedules(
    batch_data: BatchScheduleCreate,
    current_user: User = Depends(AuthService.require_admin),
    db: Session = Depends(get_db)
):
    """批量创建日程安排"""
    service = ScheduleService(db)
    try:
        schedules = service.batch_create_schedules(
            registration_ids=batch_data.registration_ids,
            exam_product_id=batch_data.exam_product_id,
            venue_id=batch_data.venue_id,
            start_time=batch_data.start_time,
            duration_minutes=batch_data.duration_minutes
        )
        return {
            "message": f"成功创建 {len(schedules)} 个日程",
            "schedules": schedules
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{schedule_id}", response_model=ScheduleResponse, summary="更新日程")
async def update_schedule(
    schedule_id: int,
    schedule_data: ScheduleUpdate,
    current_user: User = Depends(AuthService.require_admin),
    db: Session = Depends(get_db)
):
    """更新日程信息"""
    service = ScheduleService(db)
    try:
        schedule = service.update_schedule(schedule_id, schedule_data)
        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="日程不存在"
            )
        return schedule
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{schedule_id}", summary="删除日程")
async def delete_schedule(
    schedule_id: int,
    current_user: User = Depends(AuthService.require_admin),
    db: Session = Depends(get_db)
):
    """删除日程"""
    service = ScheduleService(db)
    try:
        success = service.delete_schedule(schedule_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="日程不存在"
            )
        return {"message": "日程删除成功"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{schedule_id}/start", summary="开始日程")
async def start_schedule(
    schedule_id: int,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """开始执行日程"""
    service = ScheduleService(db)
    try:
        schedule = service.start_schedule(schedule_id)
        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="日程不存在"
            )
        return {
            "message": "日程已开始",
            "schedule": schedule
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{schedule_id}/complete", summary="完成日程")
async def complete_schedule(
    schedule_id: int,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """完成日程"""
    service = ScheduleService(db)
    try:
        schedule = service.complete_schedule(schedule_id)
        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="日程不存在"
            )
        return {
            "message": "日程已完成",
            "schedule": schedule
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/statistics/overview", response_model=ScheduleStatistics, summary="获取日程统计")
async def get_schedule_statistics(
    date: Optional[str] = None,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取日程统计信息"""
    service = ScheduleService(db)
    
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
    
    stats = service.get_schedule_statistics(schedule_date)
    return stats


@router.get("/venue/{venue_id}/today", summary="获取考场今日日程")
async def get_venue_today_schedules(
    venue_id: int,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取指定考场今日的日程安排"""
    service = ScheduleService(db)
    today = datetime.now()
    schedules = service.get_venue_schedules(venue_id, today)
    return schedules
