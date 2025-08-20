#!/usr/bin/env python3
"""
UAV Exam Center Management System - SQLite Initialization
Initialize the complete system with SQLite for testing purposes
"""

import os
import sys
from datetime import datetime, date, time, timedelta
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import hashlib

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Import all models and services
from backend.app.models.base import Base
from backend.app.models.user import User, UserRole, UserStatus
from backend.app.models.rbac import Role, Permission, role_permissions, user_roles
from backend.app.models.institution import Institution, InstitutionType, InstitutionStatus
from backend.app.models.candidate import Candidate, CandidateStatus
from backend.app.models.exam_product import ExamProduct, ExamProductStatus, ExamType
from backend.app.models.schedule import Schedule, ScheduleStatus, schedule_candidates
from backend.app.models.venue import Venue, VenueType, VenueStatus

def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def main():
    print("🚀 Starting UAV Exam Center Management System Initialization...")
    
    # Create SQLite database
    DATABASE_URL = "sqlite:///./uav_exam_center.db"
    engine = create_engine(DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(bind=engine)
    
    # Create all tables
    print("\n📊 Creating database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
    
    # Initialize session
    db = SessionLocal()
    
    try:
        # 1. Initialize RBAC System
        print("\n🔒 Initializing RBAC System...")
        
        # Create permissions
        permissions_data = [
            ("user_create", "Create users"),
            ("user_read", "Read users"),
            ("user_update", "Update users"),
            ("user_delete", "Delete users"),
            ("candidate_create", "Create candidates"),
            ("candidate_read", "Read candidates"),
            ("candidate_update", "Update candidates"),
            ("candidate_delete", "Delete candidates"),
            ("schedule_create", "Create schedules"),
            ("schedule_read", "Read schedules"),
            ("schedule_update", "Update schedules"),
            ("schedule_delete", "Delete schedules"),
            ("exam_create", "Create exams"),
            ("exam_read", "Read exams"),
            ("exam_update", "Update exams"),
            ("exam_delete", "Delete exams"),
            ("venue_create", "Create venues"),
            ("venue_read", "Read venues"),
            ("venue_update", "Update venues"),
            ("venue_delete", "Delete venues"),
            ("institution_create", "Create institutions"),
            ("institution_read", "Read institutions"),
            ("institution_update", "Update institutions"),
            ("institution_delete", "Delete institutions"),
        ]
        
        permissions = []
        for code, description in permissions_data:
            permission = Permission(code=code, description=description)
            permissions.append(permission)
            db.add(permission)
        
        db.commit()
        print(f"✅ Created {len(permissions)} permissions")
        
        # Create roles
        roles_data = [
            ("super_admin", "Super Administrator", list(range(len(permissions)))),
            ("exam_admin", "Exam Administrator", [0,1,2,4,5,6,8,9,10,12,13,14,16,17,18]),
            ("institution_user", "Institution User", [4,5,6]),
            ("staff", "Staff Member", [5,9,13]),
            ("candidate", "Candidate", [5,9]),
        ]
        
        roles = []
        for name, description, perm_indices in roles_data:
            role = Role(name=name, description=description)
            # Add permissions to role
            for idx in perm_indices:
                if idx < len(permissions):
                    role.permissions.append(permissions[idx])
            roles.append(role)
            db.add(role)
        
        db.commit()
        print(f"✅ Created {len(roles)} roles with permissions")
        
        # 2. Create Test Institutions
        print("\n🏢 Creating Test Institutions...")
        
        institutions_data = [
            ("北京航空培训学院", "Beijing Aviation Training College", InstitutionType.TRAINING, 
             "北京市朝阳区", "010-12345678", "contact@bjatc.edu.cn"),
            ("上海无人机培训中心", "Shanghai UAV Training Center", InstitutionType.TRAINING,
             "上海市浦东新区", "021-87654321", "info@shuav.com.cn"),
        ]
        
        institutions = []
        for name, name_en, inst_type, address, phone, email in institutions_data:
            institution = Institution(
                name=name,
                name_en=name_en,
                type=inst_type,
                status=InstitutionStatus.ACTIVE,
                address=address,
                phone=phone,
                email=email,
                created_at=datetime.now()
            )
            institutions.append(institution)
            db.add(institution)
        
        db.commit()
        print(f"✅ Created {len(institutions)} test institutions")
        
        # 3. Create Test Users
        print("\n👥 Creating Test Users...")
        
        users_data = [
            ("admin", "admin123", "超级管理员", "admin@uav.com", "super_admin"),
            ("exam_admin", "exam123", "考务管理员", "exam@uav.com", "exam_admin"),
            ("institution_user", "inst123", "机构用户", "inst@bjatc.edu.cn", "institution_user"),
            ("staff001", "staff123", "考务人员", "staff001@uav.com", "staff"),
        ]
        
        users = []
        for username, password, display_name, email, role_name in users_data:
            # Find role
            role = db.query(Role).filter(Role.name == role_name).first()
            
            user = User(
                username=username,
                password_hash=hash_password(password),
                email=email,
                display_name=display_name,
                role=UserRole.ADMIN if role_name == "super_admin" else UserRole.USER,
                status=UserStatus.ACTIVE,
                created_at=datetime.now()
            )
            
            # Add role to user
            if role:
                user.roles.append(role)
            
            # Assign institution for institution user
            if role_name == "institution_user" and institutions:
                user.institution_id = institutions[0].id
            
            users.append(user)
            db.add(user)
        
        db.commit()
        print(f"✅ Created {len(users)} test users")
        
        # 4. Create Test Exam Products
        print("\n📋 Creating Test Exam Products...")
        
        exam_products_data = [
            ("无人机驾驶员理论考试", "UAV Pilot Theory Exam", ExamType.THEORY, 120, 80.0),
            ("无人机驾驶员实操考试", "UAV Pilot Practical Exam", ExamType.PRACTICAL, 60, 80.0),
            ("植保无人机操作员考试", "Agricultural UAV Operator Exam", ExamType.THEORY, 90, 75.0),
        ]
        
        exam_products = []
        for name, name_en, exam_type, duration, pass_score in exam_products_data:
            exam_product = ExamProduct(
                name=name,
                name_en=name_en,
                type=exam_type,
                duration_minutes=duration,
                pass_score=pass_score,
                status=ExamProductStatus.ACTIVE,
                created_at=datetime.now()
            )
            exam_products.append(exam_product)
            db.add(exam_product)
        
        db.commit()
        print(f"✅ Created {len(exam_products)} exam products")
        
        # 5. Create Test Venues
        print("\n🏛️ Creating Test Venues...")
        
        venues_data = [
            ("理论考试室A", VenueType.THEORY, 30, "北京考点理论考试室A"),
            ("理论考试室B", VenueType.THEORY, 25, "北京考点理论考试室B"),
            ("实操考试场地", VenueType.PRACTICAL, 10, "北京考点实操考试场地"),
            ("上海理论考试室", VenueType.THEORY, 40, "上海考点理论考试室"),
        ]
        
        venues = []
        for name, venue_type, capacity, description in venues_data:
            venue = Venue(
                name=name,
                type=venue_type,
                capacity=capacity,
                description=description,
                status=VenueStatus.ACTIVE,
                created_at=datetime.now()
            )
            venues.append(venue)
            db.add(venue)
        
        db.commit()
        print(f"✅ Created {len(venues)} test venues")
        
        # 6. Create Test Candidates
        print("\n🎓 Creating Test Candidates...")
        
        candidates_data = [
            ("张三", "110101199001011234", "13800138001", "张三", institutions[0].id),
            ("李四", "110101199002022345", "13800138002", "李四", institutions[0].id),
            ("王五", "310101199003033456", "13800138003", "王五", institutions[1].id),
            ("赵六", "110101199004044567", "13800138004", "赵六", institutions[0].id),
        ]
        
        candidates = []
        for name, id_card, phone, wechat_name, institution_id in candidates_data:
            candidate = Candidate(
                name=name,
                id_card=id_card,
                phone=phone,
                wechat_name=wechat_name,
                institution_id=institution_id,
                status=CandidateStatus.PENDING_SCHEDULE,
                created_at=datetime.now()
            )
            candidates.append(candidate)
            db.add(candidate)
        
        db.commit()
        print(f"✅ Created {len(candidates)} test candidates")
        
        # 7. Create Test Schedules
        print("\n📅 Creating Test Schedules...")
        
        # Create schedules for tomorrow
        tomorrow = date.today() + timedelta(days=1)
        
        schedules_data = [
            (exam_products[0].id, venues[0].id, tomorrow, time(9, 0), time(11, 0)),  # Theory A
            (exam_products[1].id, venues[2].id, tomorrow, time(14, 0), time(15, 0)),  # Practical
            (exam_products[0].id, venues[1].id, tomorrow, time(9, 0), time(11, 0)),  # Theory B
        ]
        
        schedules = []
        for exam_product_id, venue_id, exam_date, start_time, end_time in schedules_data:
            schedule = Schedule(
                exam_product_id=exam_product_id,
                venue_id=venue_id,
                exam_date=exam_date,
                start_time=start_time,
                end_time=end_time,
                status=ScheduleStatus.SCHEDULED,
                created_at=datetime.now()
            )
            schedules.append(schedule)
            db.add(schedule)
        
        db.commit()
        print(f"✅ Created {len(schedules)} test schedules")
        
        # 8. Assign Candidates to Schedules
        print("\n🔗 Assigning Candidates to Schedules...")
        
        # Assign candidates to schedules
        assignments = [
            (candidates[0], schedules[0]),  # 张三 -> Theory A
            (candidates[1], schedules[1]),  # 李四 -> Practical
            (candidates[2], schedules[2]),  # 王五 -> Theory B
            (candidates[3], schedules[0]),  # 赵六 -> Theory A
        ]
        
        for candidate, schedule in assignments:
            candidate.schedules.append(schedule)
            candidate.status = CandidateStatus.SCHEDULED
        
        db.commit()
        print(f"✅ Assigned {len(assignments)} candidate-schedule relationships")
        
        print("\n🎉 System initialization completed successfully!")
        print("\n📋 Test Accounts Created:")
        print("=" * 50)
        print("🔑 Login Credentials:")
        print("  Super Admin:     admin / admin123")
        print("  Exam Admin:      exam_admin / exam123")
        print("  Institution User: institution_user / inst123")
        print("  Staff:           staff001 / staff123")
        print("\n👥 Test Candidates (for miniprogram login):")
        print("  张三: ID Card 110101199001011234, Phone 13800138001")
        print("  李四: ID Card 110101199002022345, Phone 13800138002")
        print("  王五: ID Card 310101199003033456, Phone 13800138003")
        print("  赵六: ID Card 110101199004044567, Phone 13800138004")
        print("\n📅 Exam Schedule: Tomorrow (" + str(tomorrow) + ")")
        print("  09:00-11:00 Theory Exam (Room A & B)")
        print("  14:00-15:00 Practical Exam")
        print("\n🎯 Ready for 8 Test Scenarios!")
        
    except Exception as e:
        print(f"❌ Error during initialization: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)