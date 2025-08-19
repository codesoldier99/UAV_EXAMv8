"""
日程管理服务
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, func, or_
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from ..models.user import User, UserRole
from ..models.exam import Schedule, ScheduleStatus, ExamRegistration, ExamProduct
from ..models.venue import Venue


class ScheduleService:
    """日程服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_candidate_schedules(self, candidate_id: int) -> List[Schedule]:
        """获取考生的所有日程安排"""
        schedules = self.db.query(Schedule).filter(
            Schedule.registration_id.in_(
                self.db.query(ExamRegistration.id).filter(
                    ExamRegistration.user_id == candidate_id
                )
            )
        ).order_by(Schedule.start_time).all()
        
        return schedules
    
    def get_candidate_queue_position(self, candidate_id: int) -> Optional[Dict[str, Any]]:
        """获取考生在当前考场的排队位置"""
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
            return None
        
        # 计算排队位置
        position = self.db.query(Schedule).filter(
            and_(
                Schedule.venue_id == next_schedule.venue_id,
                Schedule.status == ScheduleStatus.PENDING,
                Schedule.start_time <= next_schedule.start_time
            )
        ).count()
        
        # 获取该考场的总等待人数
        total_waiting = self.db.query(Schedule).filter(
            and_(
                Schedule.venue_id == next_schedule.venue_id,
                Schedule.status == ScheduleStatus.PENDING
            )
        ).count()
        
        # 估算等待时间（假设每个考试15分钟）
        estimated_wait_time = (position - 1) * 15 if position > 1 else 0
        
        return {
            "venue_name": next_schedule.venue.name,
            "position": position,
            "total_waiting": total_waiting,
            "estimated_wait_time": estimated_wait_time
        }
    
    def create_schedule(
        self,
        registration_id: int,
        exam_product_id: int,
        venue_id: int,
        start_time: datetime,
        end_time: datetime
    ) -> Schedule:
        """创建日程安排"""
        # 检查时间冲突
        conflict = self.db.query(Schedule).filter(
            and_(
                Schedule.venue_id == venue_id,
                Schedule.status.in_([ScheduleStatus.PENDING, ScheduleStatus.IN_PROGRESS]),
                or_(
                    and_(Schedule.start_time < end_time, Schedule.end_time > start_time)
                )
            )
        ).first()
        
        if conflict:
            raise ValueError("时间冲突，该时间段已被占用")
        
        # 创建日程
        schedule = Schedule(
            registration_id=registration_id,
            exam_product_id=exam_product_id,
            venue_id=venue_id,
            schedule_date=start_time.date(),
            start_time=start_time,
            end_time=end_time,
            status=ScheduleStatus.PENDING
        )
        
        self.db.add(schedule)
        self.db.commit()
        self.db.refresh(schedule)
        
        return schedule
    
    def batch_create_schedules(
        self,
        registration_ids: List[int],
        exam_product_id: int,
        venue_id: int,
        start_time: datetime,
        duration_minutes: int = 15
    ) -> List[Schedule]:
        """批量创建日程安排"""
        schedules = []
        current_time = start_time
        
        for registration_id in registration_ids:
            end_time = current_time + timedelta(minutes=duration_minutes)
            
            try:
                schedule = self.create_schedule(
                    registration_id=registration_id,
                    exam_product_id=exam_product_id,
                    venue_id=venue_id,
                    start_time=current_time,
                    end_time=end_time
                )
                schedules.append(schedule)
                current_time = end_time
            except ValueError as e:
                # 如果时间冲突，跳过这个时间段
                current_time = end_time
                continue
        
        return schedules
    
    def update_schedule_status(self, schedule_id: int, status: ScheduleStatus) -> Optional[Schedule]:
        """更新日程状态"""
        schedule = self.db.query(Schedule).filter(Schedule.id == schedule_id).first()
        if not schedule:
            return None
        
        schedule.status = status
        schedule.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(schedule)
        
        return schedule
    
    def get_venue_schedules(
        self,
        venue_id: int,
        date: Optional[datetime] = None,
        status: Optional[ScheduleStatus] = None
    ) -> List[Schedule]:
        """获取考场的日程安排"""
        query = self.db.query(Schedule).filter(Schedule.venue_id == venue_id)
        
        if date:
            query = query.filter(Schedule.schedule_date == date.date())
        
        if status:
            query = query.filter(Schedule.status == status)
        
        return query.order_by(Schedule.start_time).all()
    
    def get_schedules_by_date(self, date: datetime) -> List[Schedule]:
        """获取指定日期的所有日程"""
        return self.db.query(Schedule).filter(
            Schedule.schedule_date == date.date()
        ).order_by(Schedule.start_time).all()
    
    def get_schedules_by_institution(
        self,
        institution_id: int,
        date: Optional[datetime] = None
    ) -> List[Schedule]:
        """获取指定机构的日程安排"""
        query = self.db.query(Schedule).join(ExamRegistration).join(User).filter(
            User.institution_id == institution_id
        )
        
        if date:
            query = query.filter(Schedule.schedule_date == date.date())
        
        return query.order_by(Schedule.start_time).all()
    
    def get_schedule_statistics(self, date: Optional[datetime] = None) -> Dict[str, Any]:
        """获取日程统计信息"""
        query = self.db.query(Schedule)
        
        if date:
            query = query.filter(Schedule.schedule_date == date.date())
        
        total_schedules = query.count()
        
        # 按状态统计
        status_stats = self.db.query(
            Schedule.status,
            func.count(Schedule.id).label('count')
        )
        
        if date:
            status_stats = status_stats.filter(Schedule.schedule_date == date.date())
        
        status_stats = status_stats.group_by(Schedule.status).all()
        
        # 按考场统计
        venue_stats = self.db.query(
            Venue.name,
            func.count(Schedule.id).label('count')
        ).join(Schedule)
        
        if date:
            venue_stats = venue_stats.filter(Schedule.schedule_date == date.date())
        
        venue_stats = venue_stats.group_by(Venue.id, Venue.name).all()
        
        return {
            "total_schedules": total_schedules,
            "status_stats": [
                {"status": status.value, "count": count} for status, count in status_stats
            ],
            "venue_stats": [
                {"venue_name": name, "count": count} for name, count in venue_stats
            ]
        }
