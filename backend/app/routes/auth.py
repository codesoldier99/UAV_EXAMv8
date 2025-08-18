"""
认证相关API路由
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ..config.database import get_db
from ..config.settings import settings
from ..services.auth_service import AuthService
from ..utils.security import verify_password, create_access_token
from ..models.user import User

router = APIRouter(prefix="/auth", tags=["认证"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.post("/token", summary="用户登录获取访问令牌")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """用户登录获取JWT访问令牌"""
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户账户已被禁用"
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id, "role": user.role.value},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes * 60,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "real_name": user.real_name
        }
    }


@router.post("/register", summary="用户注册")
async def register(
    username: str,
    password: str,
    email: str,
    real_name: str = None,
    phone: str = None,
    db: Session = Depends(get_db)
):
    """用户注册"""
    auth_service = AuthService(db)
    
    try:
        user = auth_service.create_user(
            username=username,
            password=password,
            email=email,
            real_name=real_name,
            phone=phone
        )
        return {
            "message": "注册成功",
            "user_id": user.id,
            "username": user.username
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/me", summary="获取当前用户信息")
async def get_current_user_info(
    current_user: User = Depends(AuthService.get_current_user)
):
    """获取当前登录用户的详细信息"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "phone": current_user.phone,
        "real_name": current_user.real_name,
        "role": current_user.role.value,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified,
        "institution_id": current_user.institution_id,
        "created_at": current_user.created_at,
        "last_login": current_user.last_login
    }


@router.post("/logout", summary="用户登出")
async def logout():
    """用户登出（实际上由于JWT无状态，主要在客户端删除token）"""
    return {"message": "登出成功"}


@router.post("/refresh", summary="刷新访问令牌")
async def refresh_token(
    current_user: User = Depends(AuthService.get_current_user)
):
    """刷新访问令牌"""
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": current_user.username, "user_id": current_user.id, "role": current_user.role.value},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes * 60
    }