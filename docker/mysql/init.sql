-- UAV考点运营管理系统 - MySQL初始化脚本
-- 创建数据库和基础配置

-- 设置字符集
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS `uav_exam_management` 
DEFAULT CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE `uav_exam_management`;

-- 优化配置
SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO';

-- 创建初始超级管理员（密码: admin123）
-- 注意：这里的密码哈希是bcrypt加密的 "admin123"
INSERT IGNORE INTO `users` (
    `username`, 
    `password_hash`, 
    `email`, 
    `real_name`, 
    `role`, 
    `is_active`, 
    `is_verified`, 
    `created_at`, 
    `updated_at`
) VALUES (
    'admin', 
    '$2b$12$LQv3c1yqBw2WuuR.vlHvH.VTELJthsJcYt1J2Lkqv6cFoFvnf/mpu', 
    'admin@uav-exam.com', 
    '系统管理员', 
    'super_admin', 
    1, 
    1, 
    NOW(), 
    NOW()
);

-- 创建测试机构
INSERT IGNORE INTO `institutions` (
    `name`, 
    `code`, 
    `contact_person`, 
    `contact_phone`, 
    `contact_email`, 
    `address`, 
    `is_active`, 
    `created_at`, 
    `updated_at`
) VALUES (
    '北京无人机培训中心', 
    'BJ_UAV_001', 
    '张教练', 
    '13800138000', 
    'beijing@uav-training.com', 
    '北京市朝阳区航空路88号', 
    1, 
    NOW(), 
    NOW()
);

-- 创建考试产品
INSERT IGNORE INTO `exam_products` (
    `name`, 
    `code`, 
    `description`, 
    `duration_minutes`, 
    `exam_type`, 
    `is_active`, 
    `created_at`, 
    `updated_at`
) VALUES 
(
    '多旋翼视距内驾驶员', 
    'MULTIROTOR_VLOS', 
    '多旋翼无人机视距内驾驶员实操考试', 
    15, 
    '实操', 
    1, 
    NOW(), 
    NOW()
),
(
    '固定翼视距内驾驶员', 
    'FIXEDWING_VLOS', 
    '固定翼无人机视距内驾驶员实操考试', 
    20, 
    '实操', 
    1, 
    NOW(), 
    NOW()
),
(
    '无人机理论考试', 
    'THEORY_EXAM', 
    '无人机驾驶员理论知识考试', 
    60, 
    '理论', 
    1, 
    NOW(), 
    NOW()
);

-- 创建考场
INSERT IGNORE INTO `venues` (
    `name`, 
    `code`, 
    `description`, 
    `capacity`, 
    `building`, 
    `floor`, 
    `room_number`, 
    `status`, 
    `is_active`, 
    `institution_id`, 
    `created_at`, 
    `updated_at`
) VALUES 
(
    '多旋翼A号实操场', 
    'MULTIROTOR_A', 
    '多旋翼无人机实操考试场地A', 
    20, 
    '实操楼', 
    '1层', 
    'A101', 
    'available', 
    1, 
    1, 
    NOW(), 
    NOW()
),
(
    '理论一号教室', 
    'THEORY_01', 
    '理论考试专用教室', 
    50, 
    '教学楼', 
    '2层', 
    '201', 
    'available', 
    1, 
    1, 
    NOW(), 
    NOW()
),
(
    '固定翼实操区', 
    'FIXEDWING_AREA', 
    '固定翼无人机实操考试区域', 
    15, 
    '实操楼', 
    '1层', 
    'B101', 
    'available', 
    1, 
    1, 
    NOW(), 
    NOW()
);

-- 创建索引优化查询性能
CREATE INDEX IF NOT EXISTS `idx_users_username` ON `users` (`username`);
CREATE INDEX IF NOT EXISTS `idx_users_email` ON `users` (`email`);
CREATE INDEX IF NOT EXISTS `idx_users_role` ON `users` (`role`);
CREATE INDEX IF NOT EXISTS `idx_users_institution` ON `users` (`institution_id`);
CREATE INDEX IF NOT EXISTS `idx_users_wechat_openid` ON `users` (`wechat_openid`);

CREATE INDEX IF NOT EXISTS `idx_institutions_code` ON `institutions` (`code`);
CREATE INDEX IF NOT EXISTS `idx_institutions_active` ON `institutions` (`is_active`);

CREATE INDEX IF NOT EXISTS `idx_exam_products_code` ON `exam_products` (`code`);
CREATE INDEX IF NOT EXISTS `idx_exam_products_type` ON `exam_products` (`exam_type`);
CREATE INDEX IF NOT EXISTS `idx_exam_products_active` ON `exam_products` (`is_active`);

CREATE INDEX IF NOT EXISTS `idx_venues_code` ON `venues` (`code`);
CREATE INDEX IF NOT EXISTS `idx_venues_status` ON `venues` (`status`);
CREATE INDEX IF NOT EXISTS `idx_venues_institution` ON `venues` (`institution_id`);

CREATE INDEX IF NOT EXISTS `idx_exam_registrations_user` ON `exam_registrations` (`user_id`);
CREATE INDEX IF NOT EXISTS `idx_exam_registrations_product` ON `exam_registrations` (`exam_product_id`);
CREATE INDEX IF NOT EXISTS `idx_exam_registrations_status` ON `exam_registrations` (`status`);
CREATE INDEX IF NOT EXISTS `idx_exam_registrations_number` ON `exam_registrations` (`registration_number`);

CREATE INDEX IF NOT EXISTS `idx_schedules_registration` ON `schedules` (`registration_id`);
CREATE INDEX IF NOT EXISTS `idx_schedules_venue` ON `schedules` (`venue_id`);
CREATE INDEX IF NOT EXISTS `idx_schedules_date` ON `schedules` (`schedule_date`);
CREATE INDEX IF NOT EXISTS `idx_schedules_status` ON `schedules` (`status`);
CREATE INDEX IF NOT EXISTS `idx_schedules_time` ON `schedules` (`start_time`, `end_time`);

CREATE INDEX IF NOT EXISTS `idx_checkins_user` ON `checkins` (`user_id`);
CREATE INDEX IF NOT EXISTS `idx_checkins_venue` ON `checkins` (`venue_id`);
CREATE INDEX IF NOT EXISTS `idx_checkins_schedule` ON `checkins` (`schedule_id`);
CREATE INDEX IF NOT EXISTS `idx_checkins_time` ON `checkins` (`checkin_time`);

-- 恢复外键检查
SET FOREIGN_KEY_CHECKS = 1;

-- 输出初始化完成信息
SELECT '✅ UAV考点运营管理系统数据库初始化完成！' as message;
SELECT CONCAT('📊 数据库: ', DATABASE()) as database_info;
SELECT '🔑 默认管理员: admin / admin123' as admin_info;
