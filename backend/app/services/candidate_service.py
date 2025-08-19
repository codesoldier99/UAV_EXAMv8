"""
考生报名管理服务
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional, Dict, Any
from datetime import datetime
import pandas as pd
import re

from ..models.user import User, UserRole
from ..models.exam import ExamProduct, ExamRegistration, RegistrationStatus
from ..models.institution import Institution
from ..schemas.candidate import CandidateCreate, CandidateUpdate, BatchImportResult
from ..utils.security import get_password_hash


class CandidateService:
    """考生服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_candidates(
        self,
        skip: int = 0,
        limit: int = 100,
        institution_id: Optional[int] = None,
        exam_product_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[User]:
        """获取考生列表"""
        query = self.db.query(User).filter(User.role == UserRole.CANDIDATE)
        
        # 应用过滤条件
        if institution_id:
            query = query.filter(User.institution_id == institution_id)
        
        if exam_product_id:
            # 通过报名记录过滤
            query = query.join(ExamRegistration).filter(
                ExamRegistration.exam_product_id == exam_product_id
            )
        
        if status:
            # 通过报名状态过滤
            query = query.join(ExamRegistration).filter(
                ExamRegistration.status == RegistrationStatus(status)
            )
        
        # 按创建时间倒序排列
        query = query.order_by(User.created_at.desc())
        
        return query.offset(skip).limit(limit).all()
    
    def get_candidate_by_id(self, candidate_id: int) -> Optional[User]:
        """根据ID获取考生"""
        return self.db.query(User).filter(
            and_(
                User.id == candidate_id,
                User.role == UserRole.CANDIDATE
            )
        ).first()
    
    def get_candidate_by_id_card(self, id_card: str) -> Optional[User]:
        """根据身份证号获取考生"""
        return self.db.query(User).filter(
            and_(
                User.id_card == id_card,
                User.role == UserRole.CANDIDATE
            )
        ).first()
    
    def create_candidate(self, candidate_data: CandidateCreate) -> User:
        """创建新的考生"""
        # 验证身份证号格式
        if not self._validate_id_card(candidate_data.id_card):
            raise ValueError("身份证号格式不正确")
        
        # 检查身份证号是否已存在
        if self.get_candidate_by_id_card(candidate_data.id_card):
            raise ValueError(f"身份证号 '{candidate_data.id_card}' 已存在")
        
        # 检查机构是否存在
        institution = self.db.query(Institution).filter(
            Institution.id == candidate_data.institution_id
        ).first()
        if not institution:
            raise ValueError("指定的机构不存在")
        
        # 检查考试产品是否存在
        exam_product = self.db.query(ExamProduct).filter(
            ExamProduct.id == candidate_data.exam_product_id
        ).first()
        if not exam_product:
            raise ValueError("指定的考试产品不存在")
        
        # 生成用户名（使用身份证号后6位）
        username = f"candidate_{candidate_data.id_card[-6:]}"
        counter = 1
        while self.db.query(User).filter(User.username == username).first():
            username = f"candidate_{candidate_data.id_card[-6:]}_{counter}"
            counter += 1
        
        # 创建考生用户
        candidate = User(
            username=username,
            password_hash=get_password_hash(candidate_data.id_card[-6:]),  # 默认密码为身份证后6位
            real_name=candidate_data.real_name,
            id_card=candidate_data.id_card,
            phone=candidate_data.phone,
            email=candidate_data.email,
            role=UserRole.CANDIDATE,
            institution_id=candidate_data.institution_id
        )
        
        self.db.add(candidate)
        self.db.commit()
        self.db.refresh(candidate)
        
        # 创建报名记录
        registration = ExamRegistration(
            user_id=candidate.id,
            exam_product_id=candidate_data.exam_product_id,
            registration_number=self._generate_registration_number(),
            candidate_number=self._generate_candidate_number(),
            status=RegistrationStatus.APPROVED  # 默认已通过
        )
        
        self.db.add(registration)
        self.db.commit()
        
        return candidate
    
    def update_candidate(self, candidate_id: int, candidate_data: CandidateUpdate) -> Optional[User]:
        """更新考生信息"""
        candidate = self.get_candidate_by_id(candidate_id)
        if not candidate:
            return None
        
        # 验证身份证号格式
        if candidate_data.id_card and not self._validate_id_card(candidate_data.id_card):
            raise ValueError("身份证号格式不正确")
        
        # 检查身份证号是否已被其他考生使用
        if candidate_data.id_card and candidate_data.id_card != candidate.id_card:
            existing_candidate = self.get_candidate_by_id_card(candidate_data.id_card)
            if existing_candidate:
                raise ValueError(f"身份证号 '{candidate_data.id_card}' 已存在")
        
        # 更新字段
        update_data = candidate_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(candidate, field, value)
        
        candidate.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(candidate)
        
        return candidate
    
    def delete_candidate(self, candidate_id: int) -> bool:
        """删除考生"""
        candidate = self.get_candidate_by_id(candidate_id)
        if not candidate:
            return False
        
        # 检查是否有关联的报名记录
        registrations = self.db.query(ExamRegistration).filter(
            ExamRegistration.user_id == candidate_id
        ).all()
        
        if registrations:
            raise ValueError("该考生存在报名记录，无法删除")
        
        self.db.delete(candidate)
        self.db.commit()
        
        return True
    
    def batch_import_candidates(self, df: pd.DataFrame, institution_id: Optional[int] = None) -> BatchImportResult:
        """批量导入考生"""
        success_count = 0
        failed_count = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                # 验证数据
                if pd.isna(row['姓名']) or pd.isna(row['身份证号']) or pd.isna(row['考试产品名称']):
                    raise ValueError("姓名、身份证号、考试产品名称为必填项")
                
                # 查找考试产品
                exam_product = self.db.query(ExamProduct).filter(
                    ExamProduct.name == row['考试产品名称']
                ).first()
                if not exam_product:
                    raise ValueError(f"考试产品 '{row['考试产品名称']}' 不存在")
                
                # 创建考生数据
                candidate_data = CandidateCreate(
                    real_name=str(row['姓名']),
                    id_card=str(row['身份证号']),
                    exam_product_id=exam_product.id,
                    institution_id=institution_id,
                    phone=str(row.get('手机号（可选）', '')) if not pd.isna(row.get('手机号（可选）', '')) else None,
                    email=str(row.get('邮箱（可选）', '')) if not pd.isna(row.get('邮箱（可选）', '')) else None
                )
                
                # 创建考生
                self.create_candidate(candidate_data)
                success_count += 1
                
            except Exception as e:
                failed_count += 1
                errors.append({
                    "row": index + 1,
                    "error": str(e)
                })
        
        return BatchImportResult(
            total=len(df),
            success_count=success_count,
            failed_count=failed_count,
            errors=errors
        )
    
    def get_candidate_statistics(self, institution_id: Optional[int] = None) -> Dict[str, Any]:
        """获取考生统计信息"""
        query = self.db.query(User).filter(User.role == UserRole.CANDIDATE)
        
        if institution_id:
            query = query.filter(User.institution_id == institution_id)
        
        total_candidates = query.count()
        
        # 按机构统计
        institution_stats = self.db.query(
            Institution.name,
            func.count(User.id).label('count')
        ).join(User).filter(
            User.role == UserRole.CANDIDATE
        ).group_by(Institution.id, Institution.name).all()
        
        # 按考试产品统计
        product_stats = self.db.query(
            ExamProduct.name,
            func.count(ExamRegistration.id).label('count')
        ).join(ExamRegistration).group_by(ExamProduct.id, ExamProduct.name).all()
        
        # 按状态统计
        status_stats = self.db.query(
            ExamRegistration.status,
            func.count(ExamRegistration.id).label('count')
        ).group_by(ExamRegistration.status).all()
        
        return {
            "total_candidates": total_candidates,
            "institution_stats": [
                {"name": name, "count": count} for name, count in institution_stats
            ],
            "product_stats": [
                {"name": name, "count": count} for name, count in product_stats
            ],
            "status_stats": [
                {"status": status.value, "count": count} for status, count in status_stats
            ]
        }
    
    def _validate_id_card(self, id_card: str) -> bool:
        """验证身份证号格式"""
        # 简单的身份证号格式验证
        pattern = r'^\d{17}[\dXx]$'
        return bool(re.match(pattern, id_card))
    
    def _generate_registration_number(self) -> str:
        """生成报名号"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"REG{timestamp}"
    
    def _generate_candidate_number(self) -> str:
        """生成准考证号"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"CAN{timestamp}"
