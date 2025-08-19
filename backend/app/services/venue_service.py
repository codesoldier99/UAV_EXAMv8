"""
考场管理服务
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..models.venue import Venue, VenueStatus
from ..models.exam import Schedule, ScheduleStatus
from ..models.institution import Institution
from ..schemas.venue import VenueCreate, VenueUpdate


class VenueService:
    """考场服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_venues(
        self,
        skip: int = 0,
        limit: int = 100,
        institution_id: Optional[int] = None,
        status: Optional[str] = None,
        venue_type: Optional[str] = None
    ) -> List[Venue]:
        """获取考场列表"""
        query = self.db.query(Venue)
        
        # 应用过滤条件
        if institution_id:
            query = query.filter(Venue.institution_id == institution_id)
        
        if status:
            query = query.filter(Venue.status == VenueStatus(status))
        
        if venue_type:
            # 这里假设venue_type存储在description或其他字段中
            query = query.filter(Venue.description.contains(venue_type))
        
        # 按创建时间倒序排列
        query = query.order_by(Venue.created_at.desc())
        
        return query.offset(skip).limit(limit).all()
    
    def get_venue_by_id(self, venue_id: int) -> Optional[Venue]:
        """根据ID获取考场"""
        return self.db.query(Venue).filter(Venue.id == venue_id).first()
    
    def get_venue_by_code(self, code: str) -> Optional[Venue]:
        """根据代码获取考场"""
        return self.db.query(Venue).filter(Venue.code == code).first()
    
    def create_venue(self, venue_data: VenueCreate) -> Venue:
        """创建新考场"""
        # 检查代码是否已存在
        if self.get_venue_by_code(venue_data.code):
            raise ValueError(f"考场代码 '{venue_data.code}' 已存在")
        
        # 检查机构是否存在
        institution = self.db.query(Institution).filter(
            Institution.id == venue_data.institution_id
        ).first()
        if not institution:
            raise ValueError("指定的机构不存在")
        
        # 创建考场
        venue = Venue(
            name=venue_data.name,
            code=venue_data.code,
            description=venue_data.description,
            capacity=venue_data.capacity,
            building=venue_data.building,
            floor=venue_data.floor,
            room_number=venue_data.room_number,
            status=VenueStatus(venue_data.status) if venue_data.status else VenueStatus.AVAILABLE,
            institution_id=venue_data.institution_id,
            equipment=venue_data.equipment,
            facilities=venue_data.facilities,
            is_active=venue_data.is_active if venue_data.is_active is not None else True
        )
        
        self.db.add(venue)
        self.db.commit()
        self.db.refresh(venue)
        
        return venue
    
    def update_venue(self, venue_id: int, venue_data: VenueUpdate) -> Optional[Venue]:
        """更新考场信息"""
        venue = self.get_venue_by_id(venue_id)
        if not venue:
            return None
        
        # 检查代码是否已被其他考场使用
        if venue_data.code and venue_data.code != venue.code:
            existing_venue = self.get_venue_by_code(venue_data.code)
            if existing_venue:
                raise ValueError(f"考场代码 '{venue_data.code}' 已存在")
        
        # 更新字段
        update_data = venue_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == 'status' and value:
                value = VenueStatus(value)
            setattr(venue, field, value)
        
        venue.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(venue)
        
        return venue
    
    def delete_venue(self, venue_id: int) -> bool:
        """删除考场"""
        venue = self.get_venue_by_id(venue_id)
        if not venue:
            return False
        
        # 检查是否有关联的日程安排
        schedules = self.db.query(Schedule).filter(
            Schedule.venue_id == venue_id
        ).all()
        
        if schedules:
            raise ValueError("该考场存在日程安排，无法删除")
        
        self.db.delete(venue)
        self.db.commit()
        
        return True
    
    def toggle_venue_status(self, venue_id: int) -> Optional[Venue]:
        """切换考场状态"""
        venue = self.get_venue_by_id(venue_id)
        if not venue:
            return None
        
        # 在可用和维护中之间切换
        if venue.status == VenueStatus.AVAILABLE:
            venue.status = VenueStatus.MAINTENANCE
        else:
            venue.status = VenueStatus.AVAILABLE
        
        venue.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(venue)
        
        return venue
    
    def get_venue_schedules(self, venue_id: int, date: Optional[datetime] = None) -> List[Schedule]:
        """获取考场的日程安排"""
        query = self.db.query(Schedule).filter(Schedule.venue_id == venue_id)
        
        if date:
            query = query.filter(Schedule.schedule_date == date.date())
        
        return query.order_by(Schedule.start_time).all()
    
    def get_venue_current_status(self, venue_id: int) -> Dict[str, Any]:
        """获取考场当前状态信息"""
        venue = self.get_venue_by_id(venue_id)
        if not venue:
            raise ValueError("考场不存在")
        
        # 获取当前正在进行的日程
        current_schedule = self.db.query(Schedule).filter(
            and_(
                Schedule.venue_id == venue_id,
                Schedule.status == ScheduleStatus.IN_PROGRESS
            )
        ).first()
        
        # 获取等待中的日程数量
        waiting_count = self.db.query(Schedule).filter(
            and_(
                Schedule.venue_id == venue_id,
                Schedule.status == ScheduleStatus.PENDING
            )
        ).count()
        
        # 获取下一个开始时间
        next_schedule = self.db.query(Schedule).filter(
            and_(
                Schedule.venue_id == venue_id,
                Schedule.status == ScheduleStatus.PENDING
            )
        ).order_by(Schedule.start_time).first()
        
        return {
            "venue_id": venue.id,
            "venue_name": venue.name,
            "venue_type": "实操" if "实操" in venue.name else "理论",
            "status": venue.status.value,
            "capacity": venue.capacity,
            "current_count": venue.current_count,
            "waiting_count": waiting_count,
            "current_candidate": None,
            "next_start_time": next_schedule.start_time.strftime("%H:%M") if next_schedule else None,
            "last_updated": datetime.now().isoformat()
        }
    
    def get_available_venues(self, institution_id: Optional[int] = None) -> List[Venue]:
        """获取可用的考场"""
        query = self.db.query(Venue).filter(
            and_(
                Venue.status == VenueStatus.AVAILABLE,
                Venue.is_active == True
            )
        )
        
        if institution_id:
            query = query.filter(Venue.institution_id == institution_id)
        
        return query.all()
    
    def search_venues(self, keyword: str, institution_id: Optional[int] = None) -> List[Venue]:
        """搜索考场"""
        query = self.db.query(Venue).filter(
            or_(
                Venue.name.contains(keyword),
                Venue.code.contains(keyword),
                Venue.description.contains(keyword),
                Venue.building.contains(keyword)
            )
        )
        
        if institution_id:
            query = query.filter(Venue.institution_id == institution_id)
        
        return query.all()
    
    def get_venue_statistics(self, institution_id: Optional[int] = None) -> Dict[str, Any]:
        """获取考场统计信息"""
        query = self.db.query(Venue)
        
        if institution_id:
            query = query.filter(Venue.institution_id == institution_id)
        
        total_venues = query.count()
        
        # 按状态统计
        status_stats = self.db.query(
            Venue.status,
            func.count(Venue.id).label('count')
        )
        
        if institution_id:
            status_stats = status_stats.filter(Venue.institution_id == institution_id)
        
        status_stats = status_stats.group_by(Venue.status).all()
        
        # 按机构统计
        institution_stats = self.db.query(
            Institution.name,
            func.count(Venue.id).label('count')
        ).join(Venue).group_by(Institution.id, Institution.name).all()
        
        return {
            "total_venues": total_venues,
            "status_stats": [
                {"status": status.value, "count": count} for status, count in status_stats
            ],
            "institution_stats": [
                {"name": name, "count": count} for name, count in institution_stats
            ]
        }
