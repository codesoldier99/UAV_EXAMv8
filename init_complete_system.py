#!/usr/bin/env python3
"""
完整系统初始化脚本
包含所有模型、RBAC权限系统、测试数据
"""
import sys
import os
from datetime import datetime, timedelta, date, time

# 添加backend到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.config.database import engine, SessionLocal, Base
from backend.app.models import *
from backend.app.core.init_rbac import init_rbac_system
from backend.app.utils.security import get_password_hash
import hashlib


def create_all_tables():
    """创建所有数据库表"""
    print("🗄️ 创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表创建完成")


def create_test_institutions(db):
    """创建测试机构"""
    print("🏢 创建测试机构...")
    
    institutions_data = [
        {
            "name": "北京航空培训学院",
            "code": "BJAT001",
            "type": "学校",
            "contact_person": "张教授",
            "contact_phone": "13800138001",
            "contact_email": "zhang@bjat.edu.cn",
            "province": "北京市",
            "city": "北京市",
            "district": "朝阳区",
            "address": "北京市朝阳区航空路123号",
            "license_number": "教民111010123456781",
            "business_license": "91110000123456789X",
            "is_active": True,
            "is_approved": True
        },
        {
            "name": "上海无人机培训中心",
            "code": "SHUAV001",
            "type": "培训机构",
            "contact_person": "李老师",
            "contact_phone": "13800138002",
            "contact_email": "li@shuav.com",
            "province": "上海市",
            "city": "上海市",
            "district": "浦东新区",
            "address": "上海市浦东新区张江路456号",
            "license_number": "教民131010123456782",
            "business_license": "91310000123456789Y",
            "is_active": True,
            "is_approved": True
        }
    ]
    
    created_institutions = []
    for inst_data in institutions_data:
        existing = db.query(Institution).filter(Institution.code == inst_data["code"]).first()
        if not existing:
            institution = Institution(**inst_data)
            db.add(institution)
            db.commit()
            db.refresh(institution)
            created_institutions.append(institution)
        else:
            created_institutions.append(existing)
    
    print(f"✅ 创建了 {len(created_institutions)} 个测试机构")
    return created_institutions


def create_test_exam_products(db):
    """创建测试考试产品"""
    print("📚 创建考试产品...")
    
    products_data = [
        {
            "name": "多旋翼视距内驾驶员",
            "code": "MULTIROTOR_VLOS",
            "description": "多旋翼无人机视距内驾驶员考试，包含理论和实操两部分",
            "theory_duration": 60,
            "practical_duration": 15,
            "theory_score": 70,
            "practical_score": 70,
            "fee": 1200.00,
            "is_active": True
        },
        {
            "name": "固定翼视距内驾驶员",
            "code": "FIXEDWING_VLOS",
            "description": "固定翼无人机视距内驾驶员考试",
            "theory_duration": 60,
            "practical_duration": 20,
            "theory_score": 70,
            "practical_score": 70,
            "fee": 1500.00,
            "is_active": True
        },
        {
            "name": "多旋翼超视距驾驶员",
            "code": "MULTIROTOR_BVLOS",
            "description": "多旋翼无人机超视距驾驶员考试",
            "theory_duration": 90,
            "practical_duration": 25,
            "theory_score": 80,
            "practical_score": 80,
            "fee": 2000.00,
            "is_active": True
        }
    ]
    
    created_products = []
    for product_data in products_data:
        existing = db.query(ExamProduct).filter(ExamProduct.code == product_data["code"]).first()
        if not existing:
            product = ExamProduct(**product_data)
            db.add(product)
            db.commit()
            db.refresh(product)
            created_products.append(product)
        else:
            created_products.append(existing)
    
    print(f"✅ 创建了 {len(created_products)} 个考试产品")
    return created_products


def create_test_venues(db, institutions):
    """创建测试考场"""
    print("🏛️ 创建考场...")
    
    venues_data = [
        {
            "name": "理论一号教室",
            "venue_type": "theory",
            "description": "理论考试专用教室，配备标准化考试设备",
            "location": "教学楼2楼201室",
            "capacity": 50,
            "status": "available",
            "equipment": "投影设备、监控系统、空调、标准化桌椅",
            "institution_id": institutions[0].id
        },
        {
            "name": "理论二号教室",
            "venue_type": "theory",
            "description": "理论考试备用教室",
            "location": "教学楼2楼202室",
            "capacity": 30,
            "status": "available",
            "equipment": "投影设备、监控系统、空调",
            "institution_id": institutions[0].id
        },
        {
            "name": "多旋翼A号实操场",
            "venue_type": "practical",
            "description": "多旋翼无人机实操考试场地",
            "location": "实操楼1楼A区",
            "capacity": 20,
            "status": "available",
            "equipment": "GPS定位系统、安全防护网、监控设备、气象站",
            "institution_id": institutions[0].id
        },
        {
            "name": "多旋翼B号实操场",
            "venue_type": "practical",
            "description": "多旋翼无人机实操考试场地（备用）",
            "location": "实操楼1楼B区",
            "capacity": 15,
            "status": "available",
            "equipment": "GPS定位系统、安全防护网、监控设备",
            "institution_id": institutions[0].id
        },
        {
            "name": "固定翼实操场",
            "venue_type": "practical",
            "description": "固定翼无人机实操考试场地",
            "location": "室外实操区",
            "capacity": 10,
            "status": "available",
            "equipment": "跑道设施、GPS定位系统、监控设备、气象站",
            "institution_id": institutions[0].id
        }
    ]
    
    created_venues = []
    for venue_data in venues_data:
        existing = db.query(Venue).filter(
            Venue.name == venue_data["name"],
            Venue.institution_id == venue_data["institution_id"]
        ).first()
        if not existing:
            venue = Venue(**venue_data)
            db.add(venue)
            db.commit()
            db.refresh(venue)
            created_venues.append(venue)
        else:
            created_venues.append(existing)
    
    print(f"✅ 创建了 {len(created_venues)} 个考场")
    return created_venues


def create_test_users(db, institutions):
    """创建测试用户"""
    print("👥 创建测试用户...")
    
    users_data = [
        {
            "username": "exam_admin",
            "email": "exam_admin@example.com",
            "full_name": "考务管理员",
            "real_name": "考务管理员",
            "phone": "13800138100",
            "password": "exam123",
            "role_name": "exam_admin",
            "is_active": True,
            "is_verified": True
        },
        {
            "username": "institution_user",
            "email": "institution@example.com",
            "full_name": "机构管理员",
            "real_name": "机构管理员",
            "phone": "13800138101",
            "password": "inst123",
            "role_name": "institution_user",
            "institution_id": institutions[0].id,
            "is_active": True,
            "is_verified": True
        },
        {
            "username": "staff001",
            "email": "staff001@example.com",
            "full_name": "考务人员001",
            "real_name": "王工作员",
            "phone": "13800138102",
            "password": "staff123",
            "role_name": "staff",
            "institution_id": institutions[0].id,
            "is_active": True,
            "is_verified": True
        }
    ]
    
    created_users = []
    for user_data in users_data:
        existing = db.query(User).filter(User.username == user_data["username"]).first()
        if not existing:
            # 创建用户
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                full_name=user_data["full_name"],
                real_name=user_data["real_name"],
                phone=user_data.get("phone"),
                password_hash=hashlib.sha256(user_data["password"].encode()).hexdigest(),
                institution_id=user_data.get("institution_id"),
                is_active=user_data["is_active"],
                is_verified=user_data["is_verified"]
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
            # 分配角色
            role = db.query(Role).filter(Role.name == user_data["role_name"]).first()
            if role:
                user.roles.append(role)
                db.commit()
            
            created_users.append(user)
        else:
            created_users.append(existing)
    
    print(f"✅ 创建了 {len(created_users)} 个测试用户")
    return created_users


def create_test_candidates(db, institutions, exam_products):
    """创建测试考生"""
    print("🎓 创建测试考生...")
    
    candidates_data = [
        {
            "name": "张三",
            "id_card": "110101199001011234",
            "phone": "13800138001",
            "email": "zhangsan@example.com",
            "institution_id": institutions[0].id,
            "exam_product_id": exam_products[0].id,
            "status": CandidateStatus.PENDING_SCHEDULE,
            "registration_number": "REG20250820001"
        },
        {
            "name": "李四",
            "id_card": "110101199002022345",
            "phone": "13800138002",
            "email": "lisi@example.com", 
            "institution_id": institutions[0].id,
            "exam_product_id": exam_products[0].id,
            "status": CandidateStatus.PENDING_SCHEDULE,
            "registration_number": "REG20250820002"
        },
        {
            "name": "王五",
            "id_card": "110101199003033456",
            "phone": "13800138003",
            "email": "wangwu@example.com",
            "institution_id": institutions[0].id,
            "exam_product_id": exam_products[1].id,
            "status": CandidateStatus.PENDING_SCHEDULE,
            "registration_number": "REG20250820003"
        },
        {
            "name": "赵六",
            "id_card": "110101199004044567",
            "phone": "13800138004",
            "email": "zhaoliu@example.com",
            "institution_id": institutions[0].id,
            "exam_product_id": exam_products[0].id,
            "status": CandidateStatus.SCHEDULED,
            "registration_number": "REG20250820004"
        },
        {
            "name": "孙七",
            "id_card": "110101199005055678",
            "phone": "13800138005",
            "email": "sunqi@example.com",
            "institution_id": institutions[0].id,
            "exam_product_id": exam_products[2].id,
            "status": CandidateStatus.PENDING_SCHEDULE,
            "registration_number": "REG20250820005"
        }
    ]
    
    created_candidates = []
    for candidate_data in candidates_data:
        existing = db.query(Candidate).filter(Candidate.id_card == candidate_data["id_card"]).first()
        if not existing:
            candidate = Candidate(**candidate_data)
            db.add(candidate)
            db.commit()
            db.refresh(candidate)
            created_candidates.append(candidate)
        else:
            created_candidates.append(existing)
    
    print(f"✅ 创建了 {len(created_candidates)} 个测试考生")
    return created_candidates


def create_test_schedules(db, venues, exam_products, candidates):
    """创建测试考试安排"""
    print("📅 创建考试安排...")
    
    # 获取明天的日期
    tomorrow = date.today() + timedelta(days=1)
    
    schedules_data = [
        {
            "activity_name": "多旋翼理论考试-上午场",
            "description": "多旋翼无人机理论考试",
            "exam_date": tomorrow,
            "start_time": time(9, 0),
            "end_time": time(10, 30),
            "venue_id": venues[0].id,  # 理论一号教室
            "exam_product_id": exam_products[0].id,
            "institution_id": venues[0].institution_id,
            "max_candidates": 30,
            "candidate_count": 2,
            "status": ScheduleStatus.READY,
            "is_theory": True,
            "is_practical": False,
            "exam_fee": 600.00
        },
        {
            "activity_name": "多旋翼实操考试-上午场",
            "description": "多旋翼无人机实操考试",
            "exam_date": tomorrow,
            "start_time": time(14, 0),
            "end_time": time(17, 0),
            "venue_id": venues[2].id,  # 多旋翼A号实操场
            "exam_product_id": exam_products[0].id,
            "institution_id": venues[2].institution_id,
            "max_candidates": 15,
            "candidate_count": 1,
            "status": ScheduleStatus.READY,
            "is_theory": False,
            "is_practical": True,
            "exam_fee": 600.00
        },
        {
            "activity_name": "固定翼理论考试",
            "description": "固定翼无人机理论考试",
            "exam_date": tomorrow,
            "start_time": time(10, 30),
            "end_time": time(12, 0),
            "venue_id": venues[1].id,  # 理论二号教室
            "exam_product_id": exam_products[1].id,
            "institution_id": venues[1].institution_id,
            "max_candidates": 20,
            "candidate_count": 1,
            "status": ScheduleStatus.PENDING,
            "is_theory": True,
            "is_practical": False,
            "exam_fee": 750.00
        }
    ]
    
    created_schedules = []
    for schedule_data in schedules_data:
        schedule = Schedule(**schedule_data)
        db.add(schedule)
        db.commit()
        db.refresh(schedule)
        created_schedules.append(schedule)
    
    # 分配考生到考试安排
    if len(candidates) >= 4:
        # 第一个考试安排分配两个考生
        created_schedules[0].candidates.extend([candidates[0], candidates[3]])
        # 第二个考试安排分配一个考生
        created_schedules[1].candidates.append(candidates[3])
        # 第三个考试安排分配一个考生
        created_schedules[2].candidates.append(candidates[2])
        
        # 更新考生状态
        candidates[0].status = CandidateStatus.SCHEDULED
        candidates[3].status = CandidateStatus.SCHEDULED
        candidates[2].status = CandidateStatus.SCHEDULED
        
        db.commit()
    
    print(f"✅ 创建了 {len(created_schedules)} 个考试安排")
    return created_schedules


def main():
    """主函数"""
    print("🚀 开始初始化完整的UAV考点运营管理系统...")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # 1. 创建数据库表
        create_all_tables()
        
        # 2. 初始化RBAC权限系统
        init_rbac_system(db)
        
        # 3. 创建测试数据
        institutions = create_test_institutions(db)
        exam_products = create_test_exam_products(db)
        venues = create_test_venues(db, institutions)
        users = create_test_users(db, institutions)
        candidates = create_test_candidates(db, institutions, exam_products)
        schedules = create_test_schedules(db, venues, exam_products, candidates)
        
        print("\n" + "=" * 60)
        print("🎉 系统初始化完成!")
        print("\n📋 测试账号信息:")
        print("超级管理员: admin / admin123")
        print("考务管理员: exam_admin / exam123")
        print("机构用户: institution_user / inst123")
        print("考务人员: staff001 / staff123")
        print("\n🎓 测试考生登录信息:")
        print("张三: 身份证 110101199001011234, 电话 13800138001")
        print("李四: 身份证 110101199002022345, 电话 13800138002")
        print("王五: 身份证 110101199003033456, 电话 13800138003")
        print("赵六: 身份证 110101199004044567, 电话 13800138004")
        print("孙七: 身份证 110101199005055678, 电话 13800138005")
        print("\n🔗 系统访问地址:")
        print("API文档: http://localhost:8000/api/v1/docs")
        print("健康检查: http://localhost:8000/health")
        print("前端界面: http://localhost:3000")
        print("\n✅ 系统已准备就绪，可以开始测试！")
        
    except Exception as e:
        print(f"❌ 系统初始化失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()