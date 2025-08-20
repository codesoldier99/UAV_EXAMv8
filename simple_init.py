#!/usr/bin/env python3
"""
Simple UAV Exam Center System Initialization for Testing
Uses SQLite and direct table creation
"""

import sqlite3
from datetime import datetime, date, timedelta
import hashlib
import os

def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def main():
    print("🚀 Starting Simple UAV Exam System Initialization...")
    
    # Remove existing database
    db_path = "/home/user/webapp/uav_exam_center.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Create SQLite connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Create tables
        print("\n📊 Creating database tables...")
        
        # Institutions table
        cursor.execute('''
            CREATE TABLE institutions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                name_en TEXT,
                type TEXT DEFAULT 'TRAINING',
                status TEXT DEFAULT 'ACTIVE',
                address TEXT,
                phone TEXT,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Users table
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT,
                display_name TEXT,
                role TEXT DEFAULT 'USER',
                status TEXT DEFAULT 'ACTIVE',
                institution_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (institution_id) REFERENCES institutions (id)
            )
        ''')
        
        # Candidates table
        cursor.execute('''
            CREATE TABLE candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                id_card TEXT UNIQUE NOT NULL,
                phone TEXT NOT NULL,
                wechat_name TEXT,
                institution_id INTEGER NOT NULL,
                status TEXT DEFAULT 'PENDING_SCHEDULE',
                qr_code TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (institution_id) REFERENCES institutions (id)
            )
        ''')
        
        # Exam products table
        cursor.execute('''
            CREATE TABLE exam_products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                name_en TEXT,
                type TEXT NOT NULL,
                duration_minutes INTEGER DEFAULT 120,
                pass_score REAL DEFAULT 80.0,
                status TEXT DEFAULT 'ACTIVE',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Venues table
        cursor.execute('''
            CREATE TABLE venues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                capacity INTEGER DEFAULT 30,
                description TEXT,
                status TEXT DEFAULT 'ACTIVE',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Schedules table
        cursor.execute('''
            CREATE TABLE schedules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exam_product_id INTEGER NOT NULL,
                venue_id INTEGER NOT NULL,
                exam_date DATE NOT NULL,
                start_time TIME NOT NULL,
                end_time TIME NOT NULL,
                status TEXT DEFAULT 'SCHEDULED',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (exam_product_id) REFERENCES exam_products (id),
                FOREIGN KEY (venue_id) REFERENCES venues (id)
            )
        ''')
        
        # Candidate schedules (many-to-many)
        cursor.execute('''
            CREATE TABLE candidate_schedules (
                candidate_id INTEGER NOT NULL,
                schedule_id INTEGER NOT NULL,
                status TEXT DEFAULT 'SCHEDULED',
                check_in_time TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (candidate_id, schedule_id),
                FOREIGN KEY (candidate_id) REFERENCES candidates (id),
                FOREIGN KEY (schedule_id) REFERENCES schedules (id)
            )
        ''')
        
        print("✅ Database tables created successfully!")
        
        # Insert test data
        print("\n🏢 Creating test institutions...")
        institutions = [
            ("北京航空培训学院", "Beijing Aviation Training College", "TRAINING", "ACTIVE", 
             "北京市朝阳区", "010-12345678", "contact@bjatc.edu.cn"),
            ("上海无人机培训中心", "Shanghai UAV Training Center", "TRAINING", "ACTIVE",
             "上海市浦东新区", "021-87654321", "info@shuav.com.cn"),
        ]
        
        cursor.executemany('''
            INSERT INTO institutions (name, name_en, type, status, address, phone, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', institutions)
        
        print("👥 Creating test users...")
        users = [
            ("admin", hash_password("admin123"), "admin@uav.com", "超级管理员", "ADMIN", "ACTIVE", None),
            ("exam_admin", hash_password("exam123"), "exam@uav.com", "考务管理员", "ADMIN", "ACTIVE", None),
            ("institution_user", hash_password("inst123"), "inst@bjatc.edu.cn", "机构用户", "USER", "ACTIVE", 1),
            ("staff001", hash_password("staff123"), "staff001@uav.com", "考务人员", "USER", "ACTIVE", None),
        ]
        
        cursor.executemany('''
            INSERT INTO users (username, password_hash, email, display_name, role, status, institution_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', users)
        
        print("📋 Creating exam products...")
        exam_products = [
            ("无人机驾驶员理论考试", "UAV Pilot Theory Exam", "THEORY", 120, 80.0, "ACTIVE"),
            ("无人机驾驶员实操考试", "UAV Pilot Practical Exam", "PRACTICAL", 60, 80.0, "ACTIVE"),
            ("植保无人机操作员考试", "Agricultural UAV Operator Exam", "THEORY", 90, 75.0, "ACTIVE"),
        ]
        
        cursor.executemany('''
            INSERT INTO exam_products (name, name_en, type, duration_minutes, pass_score, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', exam_products)
        
        print("🏛️ Creating test venues...")
        venues = [
            ("理论考试室A", "THEORY", 30, "北京考点理论考试室A", "ACTIVE"),
            ("理论考试室B", "THEORY", 25, "北京考点理论考试室B", "ACTIVE"),
            ("实操考试场地", "PRACTICAL", 10, "北京考点实操考试场地", "ACTIVE"),
            ("上海理论考试室", "THEORY", 40, "上海考点理论考试室", "ACTIVE"),
        ]
        
        cursor.executemany('''
            INSERT INTO venues (name, type, capacity, description, status)
            VALUES (?, ?, ?, ?, ?)
        ''', venues)
        
        print("🎓 Creating test candidates...")
        candidates = [
            ("张三", "110101199001011234", "13800138001", "张三", 1, "PENDING_SCHEDULE"),
            ("李四", "110101199002022345", "13800138002", "李四", 1, "PENDING_SCHEDULE"),
            ("王五", "310101199003033456", "13800138003", "王五", 2, "PENDING_SCHEDULE"),
            ("赵六", "110101199004044567", "13800138004", "赵六", 1, "PENDING_SCHEDULE"),
        ]
        
        cursor.executemany('''
            INSERT INTO candidates (name, id_card, phone, wechat_name, institution_id, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', candidates)
        
        print("📅 Creating test schedules...")
        tomorrow = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        schedules = [
            (1, 1, tomorrow, "09:00", "11:00", "SCHEDULED"),  # Theory A
            (2, 3, tomorrow, "14:00", "15:00", "SCHEDULED"),  # Practical
            (1, 2, tomorrow, "09:00", "11:00", "SCHEDULED"),  # Theory B
        ]
        
        cursor.executemany('''
            INSERT INTO schedules (exam_product_id, venue_id, exam_date, start_time, end_time, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', schedules)
        
        print("🔗 Assigning candidates to schedules...")
        candidate_schedules = [
            (1, 1, "SCHEDULED"),  # 张三 -> Theory A
            (2, 2, "SCHEDULED"),  # 李四 -> Practical
            (3, 3, "SCHEDULED"),  # 王五 -> Theory B
            (4, 1, "SCHEDULED"),  # 赵六 -> Theory A
        ]
        
        cursor.executemany('''
            INSERT INTO candidate_schedules (candidate_id, schedule_id, status)
            VALUES (?, ?, ?)
        ''', candidate_schedules)
        
        # Update candidate status to SCHEDULED
        cursor.execute("UPDATE candidates SET status = 'SCHEDULED' WHERE id IN (1,2,3,4)")
        
        # Generate QR codes for candidates
        for i in range(1, 5):
            qr_code = f"CANDIDATE_{i}_{tomorrow.replace('-', '')}"
            cursor.execute("UPDATE candidates SET qr_code = ? WHERE id = ?", (qr_code, i))
        
        conn.commit()
        print("✅ Test data inserted successfully!")
        
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
        print(f"\n📅 Exam Schedule: Tomorrow ({tomorrow})")
        print("  09:00-11:00 Theory Exam (Room A & B)")
        print("  14:00-15:00 Practical Exam")
        print("\n🎯 Ready for 8 Test Scenarios!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during initialization: {str(e)}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)