"""
考生管理API路由
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..config.database import get_db
from ..services.auth_service import AuthService
from ..models.user import User, UserRole

router = APIRouter(prefix="/candidates", tags=["考生管理"])


@router.get("/", summary="获取考生列表")
async def get_candidates(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取考生列表"""
    # 根据用户角色过滤数据
    query = db.query(User).filter(User.role == UserRole.CANDIDATE)
    
    if current_user.role == UserRole.OPERATOR:
        # 机构用户只能查看本机构的考生
        query = query.filter(User.institution_id == current_user.institution_id)
    
    candidates = query.offset(skip).limit(limit).all()
    
    return {
        "candidates": [
            {
                "id": candidate.id,
                "username": candidate.username,
                "real_name": candidate.real_name,
                "id_card": candidate.id_card,
                "phone": candidate.phone,
                "email": candidate.email,
                "institution_id": candidate.institution_id,
                "is_active": candidate.is_active,
                "created_at": candidate.created_at
            }
            for candidate in candidates
        ],
        "total": query.count()
    }


@router.get("/{candidate_id}", summary="获取考生详情")
async def get_candidate(
    candidate_id: int,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取考生详情"""
    candidate = db.query(User).filter(
        User.id == candidate_id,
        User.role == UserRole.CANDIDATE
    ).first()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="考生不存在"
        )
    
    # 检查权限
    if current_user.role == UserRole.OPERATOR and candidate.institution_id != current_user.institution_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问该考生信息"
        )
    
    return {
        "id": candidate.id,
        "username": candidate.username,
        "real_name": candidate.real_name,
        "id_card": candidate.id_card,
        "phone": candidate.phone,
        "email": candidate.email,
        "institution_id": candidate.institution_id,
        "is_active": candidate.is_active,
        "created_at": candidate.created_at
    }