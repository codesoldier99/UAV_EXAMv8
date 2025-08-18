"""
机构管理API路由
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..config.database import get_db
from ..services.auth_service import AuthService
from ..services.institution_service import InstitutionService
from ..models.user import User, UserRole

router = APIRouter(prefix="/institutions", tags=["机构管理"])


@router.get("/", summary="获取机构列表")
async def get_institutions(
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """获取机构列表"""
    service = InstitutionService(db)
    institutions = service.get_institutions(
        skip=skip,
        limit=limit,
        search=search,
        is_active=is_active
    )
    total = service.count_institutions(search=search, is_active=is_active)
    
    return {
        "items": institutions,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.get("/{institution_id}", summary="获取机构详情")
async def get_institution(
    institution_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """获取指定机构的详细信息"""
    service = InstitutionService(db)
    institution = service.get_institution(institution_id)
    
    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="机构不存在"
        )
    
    return institution


@router.post("/", summary="创建机构")
async def create_institution(
    name: str,
    code: str,
    type: str = "培训机构",
    contact_person: str = None,
    contact_phone: str = None,
    contact_email: str = None,
    address: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.require_admin)
):
    """创建新机构（需要管理员权限）"""
    service = InstitutionService(db)
    
    try:
        institution = service.create_institution(
            name=name,
            code=code,
            type=type,
            contact_person=contact_person,
            contact_phone=contact_phone,
            contact_email=contact_email,
            address=address
        )
        return institution
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{institution_id}", summary="更新机构信息")
async def update_institution(
    institution_id: int,
    name: str = None,
    type: str = None,
    contact_person: str = None,
    contact_phone: str = None,
    contact_email: str = None,
    address: str = None,
    is_active: bool = None,
    is_approved: bool = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.require_admin)
):
    """更新机构信息（需要管理员权限）"""
    service = InstitutionService(db)
    
    institution = service.update_institution(
        institution_id=institution_id,
        name=name,
        type=type,
        contact_person=contact_person,
        contact_phone=contact_phone,
        contact_email=contact_email,
        address=address,
        is_active=is_active,
        is_approved=is_approved
    )
    
    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="机构不存在"
        )
    
    return institution


@router.delete("/{institution_id}", summary="删除机构")
async def delete_institution(
    institution_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.require_super_admin)
):
    """删除机构（需要超级管理员权限）"""
    service = InstitutionService(db)
    
    success = service.delete_institution(institution_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="机构不存在"
        )
    
    return {"message": "机构删除成功"}


@router.get("/{institution_id}/venues", summary="获取机构考场列表")
async def get_institution_venues(
    institution_id: int,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """获取指定机构的考场列表"""
    service = InstitutionService(db)
    venues = service.get_institution_venues(
        institution_id=institution_id,
        skip=skip,
        limit=limit
    )
    
    return {
        "items": venues,
        "skip": skip,
        "limit": limit
    }


@router.get("/{institution_id}/stats", summary="获取机构统计信息")
async def get_institution_stats(
    institution_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """获取机构的统计信息"""
    service = InstitutionService(db)
    stats = service.get_institution_stats(institution_id)
    
    return stats