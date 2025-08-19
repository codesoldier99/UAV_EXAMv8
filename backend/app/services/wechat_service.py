"""
微信小程序服务
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json

from ..models.user import User, UserRole
from ..models.venue import Venue, VenueStatus
from ..models.exam import Schedule, ScheduleStatus, ExamProduct, ExamRegistration
from ..models.checkin import CheckIn, CheckInStatus, CheckInMethod
from ..utils.security import create_access_token
from ..config.settings import settings


class WeChatService:
    """微信服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def login_by_id_card(self, id_card: str, openid: str) -> Dict[str, Any]:
        """通过身份证号登录"""
        # 查找考生
        candidate = self.db.query(User).filter(
            and_(
                User.id_card == id_card,
                User.role == UserRole.CANDIDATE
            )
        ).first()
        
        if not candidate:
            raise ValueError("身份证号不存在或不是考生")
        
        if not candidate.is_active:
            raise ValueError("考生账户已被禁用")
        
        # 更新微信openid
        candidate.wechat_openid = openid
        candidate.last_login = datetime.utcnow()
        self.db.commit()
        
        # 生成访问令牌
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={
                "sub": candidate.username,
                "user_id": candidate.id,
                "role": candidate.role.value
            },
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.access_token_expire_minutes * 60,
            "user": {
                "id": candidate.id,
                "username": candidate.username,
                "real_name": candidate.real_name,
                "role": candidate.role.value
            }
        }
    
    def generate_candidate_qrcode(self, candidate_id: int) -> str:
        """生成考生的动态二维码数据"""
        # 获取考生的下一个待进行日程
        next_schedule = self.db.query(Schedule).filter(
            and_(
                Schedule.registration_id.in_(
                    self.db.query(ExamRegistration.id).filter(
                        ExamRegistration.user_id == candidate_id
                    )
                ),
                Schedule.status == ScheduleStatus.PENDING
            )
        ).order_by(Schedule.start_time).first()
        
        if not next_schedule:
            # 如果没有待进行的日程，返回默认数据
            qr_data = {
                "type": "candidate",
                "candidate_id": candidate_id,
                "schedule_id": None,
                "timestamp": datetime.now().isoformat()
            }
        else:
            qr_data = {
                "type": "candidate",
                "candidate_id": candidate_id,
                "schedule_id": next_schedule.id,
                "timestamp": datetime.now().isoformat()
            }
        
        return json.dumps(qr_data, ensure_ascii=False)
    
    def get_venues_status(self) -> List[Dict[str, Any]]:
        """获取所有考场的实时状态"""
        venues = self.db.query(Venue).filter(Venue.is_active == True).all()
        result = []
        
        for venue in venues:
            # 获取当前正在进行的日程
            current_schedule = self.db.query(Schedule).filter(
                and_(
                    Schedule.venue_id == venue.id,
                    Schedule.status == ScheduleStatus.IN_PROGRESS
                )
            ).first()
            
            # 获取等待中的日程数量
            waiting_count = self.db.query(Schedule).filter(
                and_(
                    Schedule.venue_id == venue.id,
                    Schedule.status == ScheduleStatus.PENDING
                )
            ).count()
            
            # 获取下一个开始时间
            next_schedule = self.db.query(Schedule).filter(
                and_(
                    Schedule.venue_id == venue.id,
                    Schedule.status == ScheduleStatus.PENDING
                )
            ).order_by(Schedule.start_time).first()
            
            venue_data = {
                "venue_id": venue.id,
                "venue_name": venue.name,
                "venue_type": venue.venue_type if hasattr(venue, 'venue_type') else "未知",
                "status": venue.status.value,
                "current_candidate": None,
                "waiting_count": waiting_count,
                "next_start_time": None,
                "capacity": venue.capacity
            }
            
            if current_schedule:
                # 获取当前考生的姓名
                candidate = self.db.query(User).filter(
                    User.id == current_schedule.registration.user_id
                ).first()
                if candidate:
                    venue_data["current_candidate"] = f"{candidate.real_name[0]}**"
            
            if next_schedule:
                venue_data["next_start_time"] = next_schedule.start_time.strftime("%H:%M")
            
            result.append(venue_data)
        
        return result
    
    def process_checkin(self, schedule_id: int, examiner_id: int, venue_id: int) -> Dict[str, Any]:
        """处理扫码签到"""
        # 获取日程信息
        schedule = self.db.query(Schedule).filter(Schedule.id == schedule_id).first()
        if not schedule:
            raise ValueError("日程不存在")
        
        if schedule.status != ScheduleStatus.PENDING:
            raise ValueError("该日程状态不允许签到")
        
        if schedule.venue_id != venue_id:
            raise ValueError("考场不匹配")
        
        # 获取考生信息
        candidate = self.db.query(User).filter(
            User.id == schedule.registration.user_id
        ).first()
        
        if not candidate:
            raise ValueError("考生信息不存在")
        
        # 创建签到记录
        checkin = CheckIn(
            user_id=candidate.id,
            venue_id=venue_id,
            exam_session_id=schedule.registration.exam_session_id,
            registration_id=schedule.registration.id,
            schedule_id=schedule_id,
            checkin_time=datetime.utcnow(),
            method=CheckInMethod.QR_CODE,
            status=CheckInStatus.SUCCESS
        )
        
        self.db.add(checkin)
        
        # 更新日程状态
        schedule.status = ScheduleStatus.IN_PROGRESS
        schedule.updated_at = datetime.utcnow()
        
        self.db.commit()
        
        return {
            "success": True,
            "message": f"{candidate.real_name} 签到成功",
            "candidate_name": candidate.real_name,
            "schedule_info": {
                "schedule_id": schedule.id,
                "venue_name": schedule.venue.name,
                "exam_product_name": schedule.exam_product.name,
                "start_time": schedule.start_time.strftime("%H:%M")
            },
            "checkin_time": checkin.checkin_time
        }
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """获取小程序看板数据"""
        # 获取考场状态
        venues_status = self.get_venues_status()
        
        # 统计信息
        total_venues = len(venues_status)
        active_venues = len([v for v in venues_status if v["status"] == "available"])
        total_waiting = sum(v["waiting_count"] for v in venues_status)
        
        return {
            "title": "UAV考点实时状态",
            "update_time": datetime.now().strftime("%H:%M"),
            "venues": venues_status,
            "summary": {
                "total_venues": total_venues,
                "active_venues": active_venues,
                "total_waiting": total_waiting
            }
        }
