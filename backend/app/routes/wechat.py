"""
微信小程序专用API路由
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import qrcode
import io
import base64

from ..config.database import get_db
from ..services.auth_service import AuthService
from ..services.wechat_service import WeChatService
from ..services.schedule_service import ScheduleService
from ..models.user import User, UserRole
from ..schemas.wechat import (
    WeChatLoginRequest,
    WeChatLoginResponse,
    CandidateScheduleResponse,
    VenueStatusResponse,
    CheckInRequest,
    CheckInResponse
)

router = APIRouter(prefix="/wechat", tags=["微信小程序"])


@router.post("/login", response_model=WeChatLoginResponse, summary="微信小程序登录")
async def wechat_login(
    login_data: WeChatLoginRequest,
    db: Session = Depends(get_db)
):
    """微信小程序登录（身份证号登录）"""
    service = WeChatService(db)
    try:
        result = service.login_by_id_card(login_data.id_card, login_data.openid)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/candidate/schedule", response_model=List[CandidateScheduleResponse], summary="获取考生日程")
async def get_candidate_schedule(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前考生的日程安排"""
    if current_user.role != UserRole.CANDIDATE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有考生可以访问此接口"
        )
    
    service = ScheduleService(db)
    schedules = service.get_candidate_schedules(current_user.id)
    return schedules


@router.get("/candidate/qrcode", summary="获取考生二维码")
async def get_candidate_qrcode(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取考生的动态二维码"""
    if current_user.role != UserRole.CANDIDATE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有考生可以访问此接口"
        )
    
    service = WeChatService(db)
    qr_data = service.generate_candidate_qrcode(current_user.id)
    
    # 生成二维码图片
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 转换为base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return {
        "qr_code": f"data:image/png;base64,{img_str}",
        "qr_data": qr_data,
        "expires_at": datetime.now().isoformat()
    }


@router.get("/venues/status", response_model=List[VenueStatusResponse], summary="获取考场状态")
async def get_venues_status(
    db: Session = Depends(get_db)
):
    """获取所有考场的实时状态（公共接口）"""
    service = WeChatService(db)
    venues = service.get_venues_status()
    return venues


@router.post("/checkin", response_model=CheckInResponse, summary="扫码签到")
async def checkin_candidate(
    checkin_data: CheckInRequest,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """考务人员扫码签到"""
    if current_user.role not in [UserRole.ADMIN, UserRole.EXAMINER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有考务人员可以执行签到操作"
        )
    
    service = WeChatService(db)
    try:
        result = service.process_checkin(
            schedule_id=checkin_data.schedule_id,
            examiner_id=current_user.id,
            venue_id=checkin_data.venue_id
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/candidate/queue-position", summary="获取排队位置")
async def get_queue_position(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取考生在当前考场的排队位置"""
    if current_user.role != UserRole.CANDIDATE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有考生可以访问此接口"
        )
    
    service = ScheduleService(db)
    position = service.get_candidate_queue_position(current_user.id)
    return position


@router.get("/dashboard", summary="获取看板数据")
async def get_dashboard_data(
    db: Session = Depends(get_db)
):
    """获取小程序看板数据（公共接口）"""
    service = WeChatService(db)
    dashboard = service.get_dashboard_data()
    return dashboard
