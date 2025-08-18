"""
分页工具函数
"""

from typing import List, TypeVar, Generic
from math import ceil

T = TypeVar('T')


class PaginationResult(Generic[T]):
    """分页结果类"""
    
    def __init__(
        self,
        items: List[T],
        total: int,
        page: int,
        size: int
    ):
        self.items = items
        self.total = total
        self.page = page
        self.size = size
        self.pages = ceil(total / size) if size > 0 else 0
        self.has_prev = page > 1
        self.has_next = page < self.pages
        self.prev_num = page - 1 if self.has_prev else None
        self.next_num = page + 1 if self.has_next else None
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            "items": self.items,
            "pagination": {
                "total": self.total,
                "page": self.page,
                "size": self.size,
                "pages": self.pages,
                "has_prev": self.has_prev,
                "has_next": self.has_next,
                "prev_num": self.prev_num,
                "next_num": self.next_num
            }
        }


def paginate(
    query,
    page: int = 1,
    per_page: int = 20,
    max_per_page: int = 100
) -> PaginationResult:
    """
    对查询结果进行分页
    
    Args:
        query: SQLAlchemy查询对象
        page: 页码（从1开始）
        per_page: 每页数量
        max_per_page: 最大每页数量
    
    Returns:
        分页结果对象
    """
    if page < 1:
        page = 1
    
    if per_page < 1:
        per_page = 20
    elif per_page > max_per_page:
        per_page = max_per_page
    
    total = query.count()
    
    # 计算偏移量
    offset = (page - 1) * per_page
    
    # 获取当前页数据
    items = query.offset(offset).limit(per_page).all()
    
    return PaginationResult(
        items=items,
        total=total,
        page=page,
        size=per_page
    )


def calculate_skip_limit(page: int = 1, size: int = 20) -> tuple:
    """
    计算跳过数量和限制数量
    
    Args:
        page: 页码（从1开始）
        size: 每页数量
    
    Returns:
        (skip, limit) 元组
    """
    if page < 1:
        page = 1
    
    if size < 1:
        size = 20
    
    skip = (page - 1) * size
    return skip, size