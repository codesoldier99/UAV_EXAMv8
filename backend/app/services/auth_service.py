"""
认证服务
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime

from ..config.database import get_db
from ..config.settings import settings
from ..models.user import User, UserRole
from ..utils.security import verify_password, get_password_hash

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class AuthService:
    """认证服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def authenticate_user(self, username: str, password: str) -> User:
        """验证用户凭据"""
        user = self.db.query(User).filter(
            (User.username == username) | 
            (User.email == username) | 
            (User.phone == username)
        ).first()
        
        if not user or not verify_password(password, user.password_hash):
            return None
        
        # 更新最后登录时间
        user.last_login = datetime.utcnow()
        self.db.commit()
        
        return user
    
    def create_user(
        self, 
        username: str, 
        password: str, 
        email: str = None,
        real_name: str = None,
        phone: str = None,
        role: UserRole = UserRole.CANDIDATE
    ) -> User:
        """创建新用户"""
        # 检查用户名是否已存在
        if self.db.query(User).filter(User.username == username).first():
            raise ValueError("用户名已存在")
        
        # 检查邮箱是否已存在
        if email and self.db.query(User).filter(User.email == email).first():
            raise ValueError("邮箱已被注册")
        
        # 检查手机号是否已存在
        if phone and self.db.query(User).filter(User.phone == phone).first():
            raise ValueError("手机号已被注册")
        
        # 创建用户
        user = User(
            username=username,
            password_hash=get_password_hash(password),
            email=email,
            real_name=real_name,
            phone=phone,
            role=role
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def get_user_by_id(self, user_id: int) -> User:
        """根据ID获取用户"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_username(self, username: str) -> User:
        """根据用户名获取用户"""
        return self.db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
    ) -> User:
        """获取当前登录用户"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            user_id: int = payload.get("user_id")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        service = AuthService(db)
        user = service.get_user_by_id(user_id)
        if user is None:
            raise credentials_exception
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="用户账户已被禁用"
            )
        
        return user
    
    @staticmethod
    def require_role(required_role: UserRole):
        """要求特定角色的装饰器生成器"""
        def role_checker(current_user: User = Depends(AuthService.get_current_user)):
            if current_user.role != required_role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"需要 {required_role.value} 权限"
                )
            return current_user
        return role_checker
    
    @staticmethod
    def require_admin(current_user: User = Depends(get_current_user)):
        """要求管理员权限"""
        if current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="需要管理员权限"
            )
        return current_user
    
    @staticmethod
    def require_super_admin(current_user: User = Depends(get_current_user)):
        """要求超级管理员权限"""
        if current_user.role != UserRole.SUPER_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="需要超级管理员权限"
            )
        return current_user