"""
考试产品管理API路由
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..config.database import get_db
from ..services.auth_service import AuthService
from ..services.exam_product_service import ExamProductService
from ..models.user import User, UserRole
from ..schemas.exam_product import (
    ExamProductCreate,
    ExamProductUpdate,
    ExamProductResponse,
    ExamProductList
)

router = APIRouter(prefix="/exam-products", tags=["考试产品管理"])


@router.get("/", response_model=List[ExamProductResponse], summary="获取考试产品列表")
async def get_exam_products(
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None,
    exam_type: Optional[str] = None,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取考试产品列表"""
    service = ExamProductService(db)
    products = service.get_exam_products(
        skip=skip,
        limit=limit,
        is_active=is_active,
        exam_type=exam_type
    )
    return products


@router.get("/{product_id}", response_model=ExamProductResponse, summary="获取考试产品详情")
async def get_exam_product(
    product_id: int,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取考试产品详情"""
    service = ExamProductService(db)
    product = service.get_exam_product_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="考试产品不存在"
        )
    return product


@router.post("/", response_model=ExamProductResponse, summary="创建考试产品")
async def create_exam_product(
    product_data: ExamProductCreate,
    current_user: User = Depends(AuthService.require_admin),
    db: Session = Depends(get_db)
):
    """创建新的考试产品"""
    service = ExamProductService(db)
    try:
        product = service.create_exam_product(product_data)
        return product
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{product_id}", response_model=ExamProductResponse, summary="更新考试产品")
async def update_exam_product(
    product_id: int,
    product_data: ExamProductUpdate,
    current_user: User = Depends(AuthService.require_admin),
    db: Session = Depends(get_db)
):
    """更新考试产品信息"""
    service = ExamProductService(db)
    try:
        product = service.update_exam_product(product_id, product_data)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="考试产品不存在"
            )
        return product
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{product_id}", summary="删除考试产品")
async def delete_exam_product(
    product_id: int,
    current_user: User = Depends(AuthService.require_admin),
    db: Session = Depends(get_db)
):
    """删除考试产品"""
    service = ExamProductService(db)
    success = service.delete_exam_product(product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="考试产品不存在"
        )
    return {"message": "考试产品删除成功"}


@router.post("/{product_id}/toggle-status", summary="切换考试产品状态")
async def toggle_exam_product_status(
    product_id: int,
    current_user: User = Depends(AuthService.require_admin),
    db: Session = Depends(get_db)
):
    """切换考试产品的启用/禁用状态"""
    service = ExamProductService(db)
    try:
        product = service.toggle_exam_product_status(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="考试产品不存在"
            )
        return {
            "message": f"考试产品状态已切换为{'启用' if product.is_active else '禁用'}",
            "product": product
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
