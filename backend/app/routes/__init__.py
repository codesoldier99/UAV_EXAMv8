"""
API路由模块
"""

from .auth import router as auth_router
from .users import router as users_router
from .institutions import router as institutions_router
from .venues import router as venues_router
from .exams import router as exams_router
from .checkins import router as checkins_router
from .admin import router as admin_router

__all__ = [
    "auth_router",
    "users_router", 
    "institutions_router",
    "venues_router",
    "exams_router",
    "checkins_router",
    "admin_router"
]