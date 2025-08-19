#!/usr/bin/env python3
"""
初始化测试数据脚本
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.config.database import engine, SessionLocal
from backend.app.models import *
from backend.app.services.auth_service import AuthService
from backend.app.services.exam_product_service import ExamProductService
from backend.app.services.institution_service import InstitutionService
from backend.app.services.candidate_service import CandidateService
from backend.app.utils.security import get_password_hash
from datetime import datetime, timedelta

def create_test_data():
    """创建测试数据"""
    db = SessionLocal()
    
    try:
        print("🚀 开始创建测试数据...")
        
        # 1. 创建超级管理员
        print("📝 创建超级管理员...")
        admin_user = User(
            username="admin",
            password_hash=get_password_hash("admin123"),
            email="admin@example.com",
            real_name="系统管理员",
            role=UserRole.SUPER_ADMIN,
            is_active=True,
            is_verified=True
        )
        db.add(admin_user)
        db.commit()
        print("✅ 超级管理员创建成功")
        
        # 2. 创建机构
        print("📝 创建测试机构...")
        institution = Institution(
            name="测试培训机构",
            code="TEST001",
            contact_person="张老师",
            contact_phone="13800138000",
            contact_email="test@example.com",
            address="北京市朝阳区测试路123号",
            is_active=True
        )
        db.add(institution)
        db.commit()
        print("✅ 测试机构创建成功")
        
        # 3. 创建机构用户
        print("📝 创建机构用户...")
        institution_user = User(
            username="institution_user",
            password_hash=get_password_hash("123456"),
            email="institution@example.com",
            real_name="机构管理员",
            role=UserRole.OPERATOR,
            institution_id=institution.id,
            is_active=True,
            is_verified=True
        )
        db.add(institution_user)
        db.commit()
        print("✅ 机构用户创建成功")
        
        # 4. 创建考试产品
        print("📝 创建考试产品...")
        exam_products = [
            {
                "name": "多旋翼视距内驾驶员",
                "code": "MULTIROTOR_VLOS",
                "description": "多旋翼无人机视距内驾驶员考试",
                "duration_minutes": 15,
                "exam_type": "实操"
            },
            {
                "name": "固定翼视距内驾驶员",
                "code": "FIXEDWING_VLOS",
                "description": "固定翼无人机视距内驾驶员考试",
                "duration_minutes": 20,
                "exam_type": "实操"
            },
            {
                "name": "无人机理论考试",
                "code": "THEORY_EXAM",
                "description": "无人机驾驶员理论考试",
                "duration_minutes": 60,
                "exam_type": "理论"
            }
        ]
        
        for product_data in exam_products:
            product = ExamProduct(**product_data)
            db.add(product)
        db.commit()
        print("✅ 考试产品创建成功")
        
        # 5. 创建考场
        print("📝 创建考场...")
        venues = [
            {
                "name": "多旋翼A号实操场",
                "code": "MULTIROTOR_A",
                "description": "多旋翼无人机实操考试场地A",
                "capacity": 20,
                "building": "实操楼",
                "floor": "1层",
                "room_number": "A101",
                "status": VenueStatus.AVAILABLE,
                "institution_id": institution.id
            },
            {
                "name": "理论一号教室",
                "code": "THEORY_01",
                "description": "理论考试教室",
                "capacity": 50,
                "building": "教学楼",
                "floor": "2层",
                "room_number": "201",
                "status": VenueStatus.AVAILABLE,
                "institution_id": institution.id
            },
            {
                "name": "固定翼实操区",
                "code": "FIXEDWING_AREA",
                "description": "固定翼无人机实操考试区域",
                "capacity": 15,
                "building": "实操楼",
                "floor": "1层",
                "room_number": "B101",
                "status": VenueStatus.AVAILABLE,
                "institution_id": institution.id
            }
        ]
        
        for venue_data in venues:
            venue = Venue(**venue_data)
            db.add(venue)
        db.commit()
        print("✅ 考场创建成功")
        
        # 6. 创建测试考生
        print("📝 创建测试考生...")
        candidates_data = [
            {
                "real_name": "张三",
                "id_card": "110101199001011234",
                "phone": "13800138001",
                "email": "zhangsan@example.com"
            },
            {
                "real_name": "李四",
                "id_card": "110101199002022345",
                "phone": "13800138002",
                "email": "lisi@example.com"
            },
            {
                "real_name": "王五",
                "id_card": "110101199003033456",
                "phone": "13800138003",
                "email": "wangwu@example.com"
            }
        ]
        
        # 获取第一个考试产品
        exam_product = db.query(ExamProduct).first()
        
        for candidate_data in candidates_data:
            # 生成用户名
            username = f"candidate_{candidate_data['id_card'][-6:]}"
            
            # 创建考生用户
            candidate = User(
                username=username,
                password_hash=get_password_hash(candidate_data['id_card'][-6:]),
                real_name=candidate_data['real_name'],
                id_card=candidate_data['id_card'],
                phone=candidate_data['phone'],
                email=candidate_data['email'],
                role=UserRole.CANDIDATE,
                institution_id=institution.id,
                is_active=True
            )
            db.add(candidate)
            db.commit()
            db.refresh(candidate)
            
            # 创建报名记录
            registration = ExamRegistration(
                user_id=candidate.id,
                exam_product_id=exam_product.id,
                registration_number=f"REG{datetime.now().strftime('%Y%m%d%H%M%S')}{candidate.id}",
                candidate_number=f"CAN{datetime.now().strftime('%Y%m%d%H%M%S')}{candidate.id}",
                status=RegistrationStatus.APPROVED
            )
            db.add(registration)
        
        db.commit()
        print("✅ 测试考生创建成功")
        
        print("\n🎉 测试数据创建完成!")
        print("\n📋 测试账号信息:")
        print("超级管理员: admin / admin123")
        print("机构用户: institution_user / 123456")
        print("考生登录: 使用身份证号后6位作为密码")
        print("\n🔗 API文档: http://localhost:8000/api/v1/docs")
        
    except Exception as e:
        print(f"❌ 创建测试数据失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()
