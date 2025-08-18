"""
机构服务
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from ..models.institution import Institution
from ..models.venue import Venue
from ..models.user import User


class InstitutionService:
    """机构服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_institutions(
        self, 
        skip: int = 0, 
        limit: int = 20,
        search: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[Institution]:
        """获取机构列表"""
        query = self.db.query(Institution)
        
        if search:
            query = query.filter(
                Institution.name.contains(search) |
                Institution.code.contains(search)
            )
        
        if is_active is not None:
            query = query.filter(Institution.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()
    
    def count_institutions(
        self,
        search: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> int:
        """统计机构数量"""
        query = self.db.query(Institution)
        
        if search:
            query = query.filter(
                Institution.name.contains(search) |
                Institution.code.contains(search)
            )
        
        if is_active is not None:
            query = query.filter(Institution.is_active == is_active)
        
        return query.count()
    
    def get_institution(self, institution_id: int) -> Institution:
        """获取机构详情"""
        return self.db.query(Institution).filter(Institution.id == institution_id).first()
    
    def get_institution_by_code(self, code: str) -> Institution:
        """根据代码获取机构"""
        return self.db.query(Institution).filter(Institution.code == code).first()
    
    def create_institution(
        self,
        name: str,
        code: str,
        type: str = "培训机构",
        contact_person: str = None,
        contact_phone: str = None,
        contact_email: str = None,
        address: str = None
    ) -> Institution:
        """创建机构"""
        # 检查代码是否已存在
        if self.get_institution_by_code(code):
            raise ValueError("机构代码已存在")
        
        institution = Institution(
            name=name,
            code=code,
            type=type,
            contact_person=contact_person,
            contact_phone=contact_phone,
            contact_email=contact_email,
            address=address
        )
        
        self.db.add(institution)
        self.db.commit()
        self.db.refresh(institution)
        
        return institution
    
    def update_institution(
        self,
        institution_id: int,
        **updates
    ) -> Institution:
        """更新机构信息"""
        institution = self.get_institution(institution_id)
        if not institution:
            return None
        
        # 更新字段
        for field, value in updates.items():
            if value is not None and hasattr(institution, field):
                setattr(institution, field, value)
        
        self.db.commit()
        self.db.refresh(institution)
        
        return institution
    
    def delete_institution(self, institution_id: int) -> bool:
        """删除机构"""
        institution = self.get_institution(institution_id)
        if not institution:
            return False
        
        # 检查是否有关联数据
        venue_count = self.db.query(Venue).filter(Venue.institution_id == institution_id).count()
        user_count = self.db.query(User).filter(User.institution_id == institution_id).count()
        
        if venue_count > 0 or user_count > 0:
            # 软删除：设置为非激活状态
            institution.is_active = False
            self.db.commit()
        else:
            # 硬删除
            self.db.delete(institution)
            self.db.commit()
        
        return True
    
    def get_institution_venues(
        self,
        institution_id: int,
        skip: int = 0,
        limit: int = 20
    ) -> List[Venue]:
        """获取机构的考场列表"""
        return self.db.query(Venue)\
            .filter(Venue.institution_id == institution_id)\
            .offset(skip).limit(limit).all()
    
    def get_institution_stats(self, institution_id: int) -> dict:
        """获取机构统计信息"""
        # 考场统计
        venue_total = self.db.query(Venue)\
            .filter(Venue.institution_id == institution_id).count()
        
        venue_active = self.db.query(Venue)\
            .filter(Venue.institution_id == institution_id, Venue.is_active == True).count()
        
        # 用户统计
        user_total = self.db.query(User)\
            .filter(User.institution_id == institution_id).count()
        
        user_active = self.db.query(User)\
            .filter(User.institution_id == institution_id, User.is_active == True).count()
        
        return {
            "venue_total": venue_total,
            "venue_active": venue_active,
            "user_total": user_total,
            "user_active": user_active
        }