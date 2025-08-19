#!/usr/bin/env python3
"""
API测试脚本
"""

import requests
import json
from datetime import datetime

# API基础URL
BASE_URL = "http://localhost:8000/api/v1"

def test_health_check():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    response = requests.get(f"{BASE_URL.replace('/api/v1', '')}/health")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

def test_system_info():
    """测试系统信息"""
    print("🔍 测试系统信息...")
    response = requests.get(f"{BASE_URL.replace('/api/v1', '')}/api/v1/system/info")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

def test_venues_status():
    """测试考场状态"""
    print("🔍 测试考场状态...")
    response = requests.get(f"{BASE_URL.replace('/api/v1', '')}/api/v1/public/venues/status")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

def test_wechat_dashboard():
    """测试微信看板"""
    print("🔍 测试微信看板...")
    response = requests.get(f"{BASE_URL.replace('/api/v1', '')}/api/v1/wechat/venues/dashboard")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

def test_exam_products():
    """测试考试产品API"""
    print("🔍 测试考试产品API...")
    response = requests.get(f"{BASE_URL}/exam-products/")
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"考试产品列表: {response.json()}")
    else:
        print(f"错误: {response.text}")
    print()

def test_candidates():
    """测试考生API"""
    print("🔍 测试考生API...")
    response = requests.get(f"{BASE_URL}/candidates/")
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"考生列表: {response.json()}")
    else:
        print(f"错误: {response.text}")
    print()

def test_wechat_venues():
    """测试微信考场状态"""
    print("🔍 测试微信考场状态...")
    response = requests.get(f"{BASE_URL}/wechat/venues/status")
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"考场状态: {response.json()}")
    else:
        print(f"错误: {response.text}")
    print()

def test_wechat_dashboard_api():
    """测试微信看板API"""
    print("🔍 测试微信看板API...")
    response = requests.get(f"{BASE_URL}/wechat/dashboard")
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"看板数据: {response.json()}")
    else:
        print(f"错误: {response.text}")
    print()

def main():
    """主测试函数"""
    print("🚀 开始API测试...")
    print("=" * 50)
    
    try:
        test_health_check()
        test_system_info()
        test_venues_status()
        test_wechat_dashboard()
        test_exam_products()
        test_candidates()
        test_wechat_venues()
        test_wechat_dashboard_api()
        
        print("✅ 所有测试完成!")
        
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败，请确保服务器正在运行")
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")

if __name__ == "__main__":
    main()
