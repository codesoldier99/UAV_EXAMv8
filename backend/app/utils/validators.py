"""
数据验证工具函数
"""

import re
from typing import Optional


def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """验证手机号格式（中国大陆）"""
    if not phone:
        return False
    
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))


def validate_id_card(id_card: str) -> bool:
    """验证身份证号格式（中国大陆）"""
    if not id_card:
        return False
    
    # 18位身份证号验证
    if len(id_card) != 18:
        return False
    
    pattern = r'^\d{17}[\dXx]$'
    return bool(re.match(pattern, id_card))


def validate_password_strength(password: str) -> dict:
    """验证密码强度"""
    result = {
        "valid": False,
        "score": 0,
        "messages": []
    }
    
    if len(password) < 8:
        result["messages"].append("密码长度至少8位")
        return result
    
    score = 0
    
    # 检查长度
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    
    # 检查字符类型
    if re.search(r'[a-z]', password):
        score += 1
    if re.search(r'[A-Z]', password):
        score += 1
    if re.search(r'\d', password):
        score += 1
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    
    result["score"] = score
    
    if score < 3:
        result["messages"].append("密码强度较弱，建议包含大小写字母、数字和特殊字符")
    elif score < 5:
        result["messages"].append("密码强度中等")
    else:
        result["messages"].append("密码强度较强")
        result["valid"] = True
    
    return result


def sanitize_input(text: str) -> str:
    """清理输入文本"""
    if not text:
        return ""
    
    # 移除HTML标签
    text = re.sub(r'<[^>]+>', '', text)
    
    # 移除多余空格
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text