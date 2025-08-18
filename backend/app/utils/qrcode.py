"""
二维码生成工具
"""

import qrcode
import io
import base64
from PIL import Image
from typing import Optional


def generate_qr_code(
    data: str,
    size: int = 10,
    border: int = 4,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    fill_color: str = "black",
    back_color: str = "white"
) -> str:
    """
    生成二维码图片的Base64编码字符串
    
    Args:
        data: 二维码包含的数据
        size: 二维码大小（1-40）
        border: 边框宽度
        error_correction: 错误纠正级别
        fill_color: 前景色
        back_color: 背景色
    
    Returns:
        Base64编码的PNG图片字符串
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_correction,
        box_size=size,
        border=border,
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    
    # 创建图片
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    
    # 转换为Base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"


def generate_venue_qr_code(venue_id: int, venue_name: str) -> str:
    """
    生成考场二维码
    
    Args:
        venue_id: 考场ID
        venue_name: 考场名称
    
    Returns:
        二维码的Base64字符串
    """
    qr_data = {
        "type": "venue",
        "venue_id": venue_id,
        "venue_name": venue_name,
        "timestamp": int(time.time())
    }
    
    import json
    data_str = json.dumps(qr_data, ensure_ascii=False)
    
    return generate_qr_code(data_str, size=8)


def generate_checkin_qr_code(
    exam_session_id: int,
    venue_id: int,
    exam_title: str
) -> str:
    """
    生成签到二维码
    
    Args:
        exam_session_id: 考试场次ID
        venue_id: 考场ID
        exam_title: 考试标题
    
    Returns:
        二维码的Base64字符串
    """
    import time
    import json
    
    qr_data = {
        "type": "checkin",
        "exam_session_id": exam_session_id,
        "venue_id": venue_id,
        "exam_title": exam_title,
        "timestamp": int(time.time())
    }
    
    data_str = json.dumps(qr_data, ensure_ascii=False)
    
    return generate_qr_code(data_str, size=10)


def parse_qr_data(qr_text: str) -> Optional[dict]:
    """
    解析二维码数据
    
    Args:
        qr_text: 二维码文本内容
    
    Returns:
        解析后的数据字典，解析失败返回None
    """
    try:
        import json
        return json.loads(qr_text)
    except (json.JSONDecodeError, TypeError):
        return None