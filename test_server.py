#!/usr/bin/env python3
"""
Simple FastAPI Test Server for UAV Exam System
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import hashlib
from datetime import datetime, date
from typing import List, Optional
import json

app = FastAPI(title="UAV Exam Center API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
def get_db():
    conn = sqlite3.connect("/home/user/webapp/uav_exam_center.db")
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Request/Response Models
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    user: Optional[dict] = None
    token: Optional[str] = None

class CandidateLoginRequest(BaseModel):
    id_card: str
    phone: str

class CandidateRegisterRequest(BaseModel):
    name: str
    id_card: str
    phone: str
    wechat_name: Optional[str] = None
    institution_id: int

class ScheduleCreateRequest(BaseModel):
    candidate_id: int
    exam_product_id: int
    venue_id: int
    exam_date: str
    start_time: str
    end_time: str

# API Endpoints

@app.get("/")
async def root():
    return {"message": "UAV Exam Center API", "version": "1.0.0", "status": "running"}

@app.post("/api/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """PC后台用户登录"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Query user
        cursor.execute('''
            SELECT u.*, i.name as institution_name 
            FROM users u 
            LEFT JOIN institutions i ON u.institution_id = i.id 
            WHERE u.username = ? AND u.status = 'ACTIVE'
        ''', (request.username,))
        
        user_row = cursor.fetchone()
        
        if not user_row:
            return LoginResponse(success=False, message="用户不存在或已被禁用")
        
        user = dict(user_row)
        
        # Verify password
        if user['password_hash'] != hash_password(request.password):
            return LoginResponse(success=False, message="用户名或密码错误")
        
        # Remove sensitive data
        user.pop('password_hash', None)
        
        return LoginResponse(
            success=True,
            message="登录成功",
            user=user,
            token=f"test_token_{user['id']}"  # Simple test token
        )
        
    except Exception as e:
        return LoginResponse(success=False, message=f"登录失败: {str(e)}")
    finally:
        conn.close()

@app.post("/api/public/candidate/login")
async def candidate_login(request: CandidateLoginRequest):
    """考生小程序登录"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT c.*, i.name as institution_name 
            FROM candidates c 
            JOIN institutions i ON c.institution_id = i.id 
            WHERE c.id_card = ? AND c.phone = ?
        ''', (request.id_card, request.phone))
        
        candidate_row = cursor.fetchone()
        
        if not candidate_row:
            raise HTTPException(status_code=401, detail="身份证号或手机号错误")
        
        candidate = dict(candidate_row)
        
        return {
            "success": True,
            "message": "登录成功",
            "candidate": candidate
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.post("/api/candidates/register")
async def register_candidate(request: CandidateRegisterRequest):
    """机构用户报名考生"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Check if candidate already exists
        cursor.execute("SELECT id FROM candidates WHERE id_card = ?", (request.id_card,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="该身份证号已存在")
        
        # Insert candidate
        cursor.execute('''
            INSERT INTO candidates (name, id_card, phone, wechat_name, institution_id, status, qr_code)
            VALUES (?, ?, ?, ?, ?, 'PENDING_SCHEDULE', ?)
        ''', (request.name, request.id_card, request.phone, request.wechat_name, 
              request.institution_id, f"CANDIDATE_{request.id_card}"))
        
        candidate_id = cursor.lastrowid
        conn.commit()
        
        return {
            "success": True,
            "message": "考生报名成功",
            "candidate_id": candidate_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.get("/api/candidates")
async def get_candidates():
    """获取考生列表"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT c.*, i.name as institution_name 
            FROM candidates c 
            JOIN institutions i ON c.institution_id = i.id 
            ORDER BY c.created_at DESC
        ''')
        
        candidates = [dict(row) for row in cursor.fetchall()]
        
        return {
            "success": True,
            "data": candidates
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.post("/api/schedules/create")
async def create_schedule(request: ScheduleCreateRequest):
    """考务管理员排期"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Create schedule
        cursor.execute('''
            INSERT INTO schedules (exam_product_id, venue_id, exam_date, start_time, end_time, status)
            VALUES (?, ?, ?, ?, ?, 'SCHEDULED')
        ''', (request.exam_product_id, request.venue_id, request.exam_date, 
              request.start_time, request.end_time))
        
        schedule_id = cursor.lastrowid
        
        # Assign candidate to schedule
        cursor.execute('''
            INSERT INTO candidate_schedules (candidate_id, schedule_id, status)
            VALUES (?, ?, 'SCHEDULED')
        ''', (request.candidate_id, schedule_id))
        
        # Update candidate status
        cursor.execute('''
            UPDATE candidates SET status = 'SCHEDULED' WHERE id = ?
        ''', (request.candidate_id,))
        
        conn.commit()
        
        return {
            "success": True,
            "message": "排期成功",
            "schedule_id": schedule_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.get("/api/public/candidate/{candidate_id}/schedules")
async def get_candidate_schedules(candidate_id: int):
    """获取考生排期信息"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT s.*, ep.name as exam_name, v.name as venue_name,
                   cs.status as schedule_status, cs.check_in_time,
                   c.qr_code
            FROM candidate_schedules cs
            JOIN schedules s ON cs.schedule_id = s.id
            JOIN exam_products ep ON s.exam_product_id = ep.id
            JOIN venues v ON s.venue_id = v.id
            JOIN candidates c ON cs.candidate_id = c.id
            WHERE cs.candidate_id = ?
            ORDER BY s.exam_date, s.start_time
        ''', (candidate_id,))
        
        schedules = [dict(row) for row in cursor.fetchall()]
        
        return {
            "success": True,
            "data": schedules
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.post("/api/public/checkin")
async def check_in_candidate():
    """考务人员扫码签到"""
    # This is a simplified check-in endpoint
    return {
        "success": True,
        "message": "签到成功",
        "check_in_time": datetime.now().isoformat()
    }

@app.get("/api/dashboard/venue-status")
async def get_venue_status():
    """考场看板状态"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Get today's schedules with candidate counts
        today = date.today().strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT v.name as venue_name, s.*, ep.name as exam_name,
                   COUNT(cs.candidate_id) as candidate_count,
                   SUM(CASE WHEN cs.check_in_time IS NOT NULL THEN 1 ELSE 0 END) as checked_in_count
            FROM schedules s
            JOIN venues v ON s.venue_id = v.id
            JOIN exam_products ep ON s.exam_product_id = ep.id
            LEFT JOIN candidate_schedules cs ON s.id = cs.schedule_id
            WHERE s.exam_date = ?
            GROUP BY s.id, v.name, ep.name
            ORDER BY s.start_time
        ''', (today,))
        
        venue_status = [dict(row) for row in cursor.fetchall()]
        
        return {
            "success": True,
            "data": venue_status,
            "date": today
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.get("/api/exam-products")
async def get_exam_products():
    """获取考试科目"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM exam_products WHERE status = 'ACTIVE'")
        products = [dict(row) for row in cursor.fetchall()]
        
        return {"success": True, "data": products}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.get("/api/venues")
async def get_venues():
    """获取考场列表"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM venues WHERE status = 'ACTIVE'")
        venues = [dict(row) for row in cursor.fetchall()]
        
        return {"success": True, "data": venues}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)