"""
考试产品管理服务
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime

from ..models.exam import ExamProduct
from ..schemas.exam_product import ExamProductCreate, ExamProductUpdate


class ExamProductService:
    """考试产品服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_exam_products(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        exam_type: Optional[str] = None
    ) -> List[ExamProduct]:
        """获取考试产品列表"""
        query = self.db.query(ExamProduct)
        
        # 应用过滤条件
        if is_active is not None:
            query = query.filter(ExamProduct.is_active == is_active)
        
        if exam_type:
            query = query.filter(ExamProduct.exam_type == exam_type)
        
        # 按创建时间倒序排列
        query = query.order_by(ExamProduct.created_at.desc())
        
        return query.offset(skip).limit(limit).all()
    
    def get_exam_product_by_id(self, product_id: int) -> Optional[ExamProduct]:
        """根据ID获取考试产品"""
        return self.db.query(ExamProduct).filter(ExamProduct.id == product_id).first()
    
    def get_exam_product_by_code(self, code: str) -> Optional[ExamProduct]:
        """根据代码获取考试产品"""
        return self.db.query(ExamProduct).filter(ExamProduct.code == code).first()
    
    def get_exam_product_by_name(self, name: str) -> Optional[ExamProduct]:
        """根据名称获取考试产品"""
        return self.db.query(ExamProduct).filter(ExamProduct.name == name).first()
    
    def create_exam_product(self, product_data: ExamProductCreate) -> ExamProduct:
        """创建新的考试产品"""
        # 检查代码是否已存在
        if self.get_exam_product_by_code(product_data.code):
            raise ValueError(f"考试产品代码 '{product_data.code}' 已存在")
        
        # 检查名称是否已存在
        if self.get_exam_product_by_name(product_data.name):
            raise ValueError(f"考试产品名称 '{product_data.name}' 已存在")
        
        # 创建考试产品
        product = ExamProduct(
            name=product_data.name,
            code=product_data.code,
            description=product_data.description,
            duration_minutes=product_data.duration_minutes,
            exam_type=product_data.exam_type,
            is_active=product_data.is_active if product_data.is_active is not None else True
        )
        
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        
        return product
    
    def update_exam_product(self, product_id: int, product_data: ExamProductUpdate) -> Optional[ExamProduct]:
        """更新考试产品信息"""
        product = self.get_exam_product_by_id(product_id)
        if not product:
            return None
        
        # 检查代码是否已被其他产品使用
        if product_data.code and product_data.code != product.code:
            existing_product = self.get_exam_product_by_code(product_data.code)
            if existing_product:
                raise ValueError(f"考试产品代码 '{product_data.code}' 已存在")
        
        # 检查名称是否已被其他产品使用
        if product_data.name and product_data.name != product.name:
            existing_product = self.get_exam_product_by_name(product_data.name)
            if existing_product:
                raise ValueError(f"考试产品名称 '{product_data.name}' 已存在")
        
        # 更新字段
        update_data = product_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        
        product.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(product)
        
        return product
    
    def delete_exam_product(self, product_id: int) -> bool:
        """删除考试产品"""
        product = self.get_exam_product_by_id(product_id)
        if not product:
            return False
        
        # 检查是否有关联的报名记录
        if product.exam_registrations:
            raise ValueError("该考试产品存在关联的报名记录，无法删除")
        
        # 检查是否有关联的日程安排
        if product.schedules:
            raise ValueError("该考试产品存在关联的日程安排，无法删除")
        
        self.db.delete(product)
        self.db.commit()
        
        return True
    
    def toggle_exam_product_status(self, product_id: int) -> Optional[ExamProduct]:
        """切换考试产品的启用/禁用状态"""
        product = self.get_exam_product_by_id(product_id)
        if not product:
            return None
        
        product.is_active = not product.is_active
        product.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(product)
        
        return product
    
    def get_active_exam_products(self) -> List[ExamProduct]:
        """获取所有启用的考试产品"""
        return self.db.query(ExamProduct).filter(ExamProduct.is_active == True).all()
    
    def get_exam_products_by_type(self, exam_type: str) -> List[ExamProduct]:
        """根据考试类型获取考试产品"""
        return self.db.query(ExamProduct).filter(
            and_(
                ExamProduct.exam_type == exam_type,
                ExamProduct.is_active == True
            )
        ).all()
    
    def search_exam_products(self, keyword: str) -> List[ExamProduct]:
        """搜索考试产品"""
        return self.db.query(ExamProduct).filter(
            or_(
                ExamProduct.name.contains(keyword),
                ExamProduct.code.contains(keyword),
                ExamProduct.description.contains(keyword)
            )
        ).all()
