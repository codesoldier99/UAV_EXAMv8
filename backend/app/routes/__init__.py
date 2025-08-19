"""
API路由模块
"""

from .auth import router as auth_router
from .institutions import router as institutions_router
from .venues import router as venues_router
from .exam_products import router as exam_products_router
from .candidates import router as candidates_router
from .wechat import router as wechat_router
from .schedules import router as schedules_router

__all__ = [
    "auth_router",
    "institutions_router",
    "venues_router",
    "exam_products_router",
    "candidates_router",
    "wechat_router",
    "schedules_router"
]