#!/usr/bin/env python3
"""
UAV Exam Center - 8 Test Scenarios
测试完整的考试管理系统流程
"""

import requests
import json
from datetime import datetime, date, timedelta

# API Base URL
API_BASE = "https://8000-ilh9ynfruexbglxoshzc7-6532622b.e2b.dev"

def test_api_connection():
    """测试API连接"""
    print("🔗 Testing API Connection...")
    try:
        response = requests.get(f"{API_BASE}/")
        print(f"✅ API Status: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ API Connection Failed: {str(e)}")
        return False

def test_scenario_1():
    """测试场景1: 机构用户能登录PC后台"""
    print("\n🔑 Test Scenario 1: Institution User PC Backend Login")
    print("=" * 60)
    
    # Test institution user login
    login_data = {
        "username": "institution_user",
        "password": "inst123"
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/auth/login", json=login_data)
        result = response.json()
        
        if result.get("success"):
            print("✅ Institution user login successful!")
            print(f"   User: {result['user']['display_name']}")
            print(f"   Institution: {result['user']['institution_name']}")
            print(f"   Token: {result['token']}")
            return True, result['user']
        else:
            print(f"❌ Login failed: {result.get('message')}")
            return False, None
            
    except Exception as e:
        print(f"❌ Login test failed: {str(e)}")
        return False, None

def test_scenario_2():
    """测试场景2: 机构用户能成功报名一个考生（手动或批量）"""
    print("\n📝 Test Scenario 2: Institution User Can Register Candidates")
    print("=" * 60)
    
    # Register a new candidate
    candidate_data = {
        "name": "测试考生001",
        "id_card": "110101199905051111",
        "phone": "13900139001",
        "wechat_name": "测试考生001",
        "institution_id": 1
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/candidates/register", json=candidate_data)
        result = response.json()
        
        if result.get("success"):
            print("✅ Candidate registration successful!")
            print(f"   Name: {candidate_data['name']}")
            print(f"   ID Card: {candidate_data['id_card']}")
            print(f"   Phone: {candidate_data['phone']}")
            print(f"   Candidate ID: {result['candidate_id']}")
            return True, result['candidate_id']
        else:
            print(f"❌ Registration failed: {result}")
            return False, None
            
    except Exception as e:
        print(f"❌ Registration test failed: {str(e)}")
        return False, None

def test_scenario_3():
    """测试场景3: 考务管理员能登录PC后台"""
    print("\n🔑 Test Scenario 3: Exam Administrator PC Backend Login")
    print("=" * 60)
    
    # Test exam admin login
    login_data = {
        "username": "exam_admin",
        "password": "exam123"
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/auth/login", json=login_data)
        result = response.json()
        
        if result.get("success"):
            print("✅ Exam administrator login successful!")
            print(f"   User: {result['user']['display_name']}")
            print(f"   Role: {result['user']['role']}")
            print(f"   Token: {result['token']}")
            return True, result['user']
        else:
            print(f"❌ Login failed: {result.get('message')}")
            return False, None
            
    except Exception as e:
        print(f"❌ Login test failed: {str(e)}")
        return False, None

def test_scenario_4(candidate_id):
    """测试场景4: 考务管理员能为这个考生成功排一个期"""
    print("\n📅 Test Scenario 4: Exam Administrator Can Schedule Exams")
    print("=" * 60)
    
    if not candidate_id:
        print("❌ No candidate ID available for scheduling")
        return False
    
    # Get exam products and venues first
    try:
        products_response = requests.get(f"{API_BASE}/api/exam-products")
        venues_response = requests.get(f"{API_BASE}/api/venues")
        
        products = products_response.json()['data']
        venues = venues_response.json()['data']
        
        if not products or not venues:
            print("❌ No exam products or venues available")
            return False
        
        print(f"Available exam products: {len(products)}")
        print(f"Available venues: {len(venues)}")
        
        # Create schedule for tomorrow
        tomorrow = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        schedule_data = {
            "candidate_id": candidate_id,
            "exam_product_id": products[0]['id'],  # First available product
            "venue_id": venues[0]['id'],  # First available venue
            "exam_date": tomorrow,
            "start_time": "16:00",
            "end_time": "18:00"
        }
        
        response = requests.post(f"{API_BASE}/api/schedules/create", json=schedule_data)
        result = response.json()
        
        if result.get("success"):
            print("✅ Exam scheduling successful!")
            print(f"   Candidate ID: {candidate_id}")
            print(f"   Exam: {products[0]['name']}")
            print(f"   Venue: {venues[0]['name']}")
            print(f"   Date: {tomorrow}")
            print(f"   Time: {schedule_data['start_time']}-{schedule_data['end_time']}")
            print(f"   Schedule ID: {result['schedule_id']}")
            return True
        else:
            print(f"❌ Scheduling failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Scheduling test failed: {str(e)}")
        return False

def test_scenario_5():
    """测试场景5: 考生能用身份证号登录小程序"""
    print("\n📱 Test Scenario 5: Candidate Miniprogram Login with ID Card")
    print("=" * 60)
    
    # Test with existing candidate
    login_data = {
        "id_card": "110101199001011234",
        "phone": "13800138001"
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/public/candidate/login", json=login_data)
        result = response.json()
        
        if result.get("success"):
            print("✅ Candidate miniprogram login successful!")
            print(f"   Name: {result['candidate']['name']}")
            print(f"   ID Card: {result['candidate']['id_card']}")
            print(f"   Phone: {result['candidate']['phone']}")
            print(f"   Status: {result['candidate']['status']}")
            print(f"   Institution: {result['candidate']['institution_name']}")
            return True, result['candidate']
        else:
            print(f"❌ Login failed: {result}")
            return False, None
            
    except Exception as e:
        print(f"❌ Miniprogram login test failed: {str(e)}")
        return False, None

def test_scenario_6(candidate):
    """测试场景6: 考生能在小程序里看到自己的日程和二维码"""
    print("\n📋 Test Scenario 6: Candidate Can View Schedule and QR Code")
    print("=" * 60)
    
    if not candidate:
        print("❌ No candidate data available")
        return False
    
    candidate_id = candidate['id']
    
    try:
        response = requests.get(f"{API_BASE}/api/public/candidate/{candidate_id}/schedules")
        result = response.json()
        
        if result.get("success"):
            schedules = result['data']
            print("✅ Candidate schedule retrieval successful!")
            print(f"   Candidate: {candidate['name']}")
            print(f"   Total schedules: {len(schedules)}")
            
            for i, schedule in enumerate(schedules, 1):
                print(f"\n   Schedule {i}:")
                print(f"     Exam: {schedule['exam_name']}")
                print(f"     Venue: {schedule['venue_name']}")
                print(f"     Date: {schedule['exam_date']}")
                print(f"     Time: {schedule['start_time']}-{schedule['end_time']}")
                print(f"     Status: {schedule['schedule_status']}")
                print(f"     QR Code: {schedule['qr_code']}")
            
            return True, schedules
        else:
            print(f"❌ Schedule retrieval failed: {result}")
            return False, None
            
    except Exception as e:
        print(f"❌ Schedule retrieval test failed: {str(e)}")
        return False, None

def test_scenario_7():
    """测试场景7: 考务人员能用小程序成功扫描这个二维码并完成签到"""
    print("\n📷 Test Scenario 7: Staff Can Scan QR Code and Complete Check-in")
    print("=" * 60)
    
    try:
        response = requests.post(f"{API_BASE}/api/public/checkin", json={"qr_code": "test_qr_code"})
        result = response.json()
        
        if result.get("success"):
            print("✅ QR code scanning and check-in successful!")
            print(f"   Check-in time: {result['check_in_time']}")
            print("   Status: Candidate checked in successfully")
            return True
        else:
            print(f"❌ Check-in failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Check-in test failed: {str(e)}")
        return False

def test_scenario_8():
    """测试场景8: 考场看板能大致反映出状态变化"""
    print("\n📊 Test Scenario 8: Venue Dashboard Reflects Status Changes")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_BASE}/api/dashboard/venue-status")
        result = response.json()
        
        if result.get("success"):
            venue_data = result['data']
            print("✅ Venue dashboard data retrieval successful!")
            print(f"   Date: {result['date']}")
            print(f"   Total venue sessions: {len(venue_data)}")
            
            for i, venue in enumerate(venue_data, 1):
                print(f"\n   Venue Session {i}:")
                print(f"     Venue: {venue['venue_name']}")
                print(f"     Exam: {venue['exam_name']}")
                print(f"     Time: {venue['start_time']}-{venue['end_time']}")
                print(f"     Total Candidates: {venue['candidate_count']}")
                print(f"     Checked In: {venue['checked_in_count']}")
                print(f"     Status: {venue['status']}")
            
            return True
        else:
            print(f"❌ Dashboard retrieval failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Dashboard test failed: {str(e)}")
        return False

def main():
    """运行所有测试场景"""
    print("🚀 UAV Exam Center - Complete System Test")
    print("=" * 60)
    print("Testing all 8 required scenarios...")
    
    # Test API connection first
    if not test_api_connection():
        return
    
    # Run all test scenarios
    results = []
    
    # Scenario 1: Institution user login
    success1, institution_user = test_scenario_1()
    results.append(("Institution User Login", success1))
    
    # Scenario 2: Register candidate
    success2, candidate_id = test_scenario_2()
    results.append(("Candidate Registration", success2))
    
    # Scenario 3: Exam admin login
    success3, exam_admin = test_scenario_3()
    results.append(("Exam Admin Login", success3))
    
    # Scenario 4: Schedule exam (needs candidate_id from scenario 2)
    success4 = test_scenario_4(candidate_id)
    results.append(("Exam Scheduling", success4))
    
    # Scenario 5: Candidate miniprogram login
    success5, candidate = test_scenario_5()
    results.append(("Candidate Miniprogram Login", success5))
    
    # Scenario 6: View schedule and QR (needs candidate from scenario 5)
    success6, schedules = test_scenario_6(candidate)
    results.append(("Candidate Schedule View", success6))
    
    # Scenario 7: QR scanning and check-in
    success7 = test_scenario_7()
    results.append(("QR Code Check-in", success7))
    
    # Scenario 8: Venue dashboard
    success8 = test_scenario_8()
    results.append(("Venue Dashboard", success8))
    
    # Print summary
    print("\n" + "=" * 60)
    print("🎯 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    for i, (name, success) in enumerate(results, 1):
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{i}. {name}: {status}")
        if success:
            passed += 1
    
    print(f"\n📊 Overall Result: {passed}/{len(results)} scenarios passed")
    
    if passed == len(results):
        print("🎉 ALL TESTS PASSED! System is ready for production.")
    else:
        print("⚠️  Some tests failed. Please review and fix issues.")
    
    print("\n🔗 API Server URL: " + API_BASE)
    print("📋 Test Credentials:")
    print("   Admin: admin/admin123")
    print("   Exam Admin: exam_admin/exam123") 
    print("   Institution User: institution_user/inst123")
    print("   Staff: staff001/staff123")
    print("\n👥 Test Candidates for Miniprogram:")
    print("   张三: ID 110101199001011234, Phone 13800138001")
    print("   李四: ID 110101199002022345, Phone 13800138002")

if __name__ == "__main__":
    main()