"""
数据模式模块
"""

from .exam_product import ExamProductCreate, ExamProductUpdate, ExamProductResponse, ExamProductList
from .candidate import CandidateCreate, CandidateUpdate, CandidateResponse, CandidateList, BatchImportResult, CandidateStatistics
from .wechat import WeChatLoginRequest, WeChatLoginResponse, CandidateScheduleResponse, VenueStatusResponse, CheckInRequest, CheckInResponse, QueuePositionResponse

__all__ = [
    "ExamProductCreate", "ExamProductUpdate", "ExamProductResponse", "ExamProductList",
    "CandidateCreate", "CandidateUpdate", "CandidateResponse", "CandidateList", "BatchImportResult", "CandidateStatistics",
    "WeChatLoginRequest", "WeChatLoginResponse", "CandidateScheduleResponse", "VenueStatusResponse", "CheckInRequest", "CheckInResponse", "QueuePositionResponse"
]
