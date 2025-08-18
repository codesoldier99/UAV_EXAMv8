<template>
  <div class="dashboard">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>控制台</h1>
      <p>欢迎使用UAV考点运营管理系统，{{ userStore.user?.real_name || '用户' }}！</p>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6" v-for="stat in stats" :key="stat.key">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" :style="{ backgroundColor: stat.color }">
              <el-icon><component :is="stat.icon" /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stat.value }}</div>
              <div class="stat-label">{{ stat.label }}</div>
              <div class="stat-change" :class="stat.trend">
                <el-icon><ArrowUp v-if="stat.trend === 'up'" /><ArrowDown v-else /></el-icon>
                {{ stat.change }}
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 主要内容区域 -->
    <el-row :gutter="20" class="content-row">
      <!-- 考场状态监控 -->
      <el-col :span="16">
        <el-card title="考场实时状态" shadow="hover" class="monitor-card">
          <template #header>
            <div class="card-header">
              <span>考场实时状态</span>
              <el-button type="primary" size="small" @click="refreshVenuesStatus">
                <el-icon><Refresh /></el-icon>
                刷新
              </el-button>
            </div>
          </template>

          <div class="venues-monitor">
            <div 
              v-for="venue in venuesStatus" 
              :key="venue.venue_id"
              class="venue-item"
              :class="venue.status"
            >
              <div class="venue-header">
                <h4>{{ venue.venue_name }}</h4>
                <el-tag 
                  :type="getStatusType(venue.status)"
                  size="small"
                >
                  {{ venue.status }}
                </el-tag>
              </div>
              
              <div class="venue-details">
                <div class="detail-item">
                  <span class="label">类型:</span>
                  <span class="value">{{ venue.venue_type }}</span>
                </div>
                
                <div class="detail-item" v-if="venue.current_candidate">
                  <span class="label">当前考生:</span>
                  <span class="value">{{ venue.current_candidate }}</span>
                </div>
                
                <div class="detail-item" v-if="venue.waiting_count > 0">
                  <span class="label">等待人数:</span>
                  <span class="value">{{ venue.waiting_count }}人</span>
                </div>
                
                <div class="detail-item" v-if="venue.next_start_time">
                  <span class="label">下场时间:</span>
                  <span class="value">{{ venue.next_start_time }}</span>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 快速操作 -->
      <el-col :span="8">
        <el-card title="快速操作" shadow="hover" class="quick-actions-card">
          <div class="quick-actions">
            <el-button 
              type="primary" 
              icon="Plus" 
              @click="$router.push('/institution')"
              class="action-btn"
            >
              机构管理
            </el-button>
            
            <el-button 
              type="success" 
              icon="School" 
              @click="$router.push('/venue')"
              class="action-btn"
            >
              考场管理
            </el-button>
            
            <el-button 
              type="warning" 
              icon="EditPen" 
              @click="$router.push('/exam')"
              class="action-btn"
            >
              考试管理
            </el-button>
            
            <el-button 
              type="info" 
              icon="User" 
              @click="$router.push('/candidate')"
              class="action-btn"
            >
              考生管理
            </el-button>
            
            <el-button 
              type="primary" 
              icon="Checked" 
              @click="$router.push('/checkin')"
              class="action-btn"
            >
              签到管理
            </el-button>
          </div>
        </el-card>

        <!-- 最新动态 -->
        <el-card title="最新动态" shadow="hover" class="activities-card" style="margin-top: 20px;">
          <div class="activities">
            <div v-for="activity in activities" :key="activity.id" class="activity-item">
              <div class="activity-time">{{ activity.time }}</div>
              <div class="activity-content">
                <div class="activity-title">{{ activity.title }}</div>
                <div class="activity-desc">{{ activity.description }}</div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useUserStore } from '@/store/user'
import { ElMessage } from 'element-plus'
import { 
  OfficeBuilding, User, School, Checked, 
  ArrowUp, ArrowDown, Refresh 
} from '@element-plus/icons-vue'
import api from '@/api'

const userStore = useUserStore()

// 统计数据
const stats = reactive([
  {
    key: 'institutions',
    label: '注册机构',
    value: '126',
    change: '+12.5%',
    trend: 'up',
    color: '#409EFF',
    icon: 'OfficeBuilding'
  },
  {
    key: 'venues',
    label: '考场总数',
    value: '48',
    change: '+3.2%',
    trend: 'up',
    color: '#67C23A',
    icon: 'School'
  },
  {
    key: 'candidates',
    label: '注册考生',
    value: '2,340',
    change: '+18.7%',
    trend: 'up',
    color: '#E6A23C',
    icon: 'User'
  },
  {
    key: 'checkins',
    label: '今日签到',
    value: '156',
    change: '+5.3%',
    trend: 'up',
    color: '#F56C6C',
    icon: 'Checked'
  }
])

// 考场状态数据
const venuesStatus = ref([])

// 最新动态数据
const activities = reactive([
  {
    id: 1,
    time: '10分钟前',
    title: '考生张三签到成功',
    description: '多旋翼A号实操场'
  },
  {
    id: 2,
    time: '25分钟前',
    title: '新机构注册审核通过',
    description: '航空培训学校'
  },
  {
    id: 3,
    time: '1小时前',
    title: '考试场次安排完成',
    description: '无人机驾驶员理论考试'
  },
  {
    id: 4,
    time: '2小时前',
    title: '考场设备检修完成',
    description: '固定翼实操区'
  }
])

// 获取状态类型
const getStatusType = (status) => {
  const statusMap = {
    '进行中': 'danger',
    '空闲': 'success',
    '维护中': 'warning',
    '已禁用': 'info'
  }
  return statusMap[status] || 'info'
}

// 刷新考场状态
const refreshVenuesStatus = async () => {
  try {
    const response = await api.get('/public/venues/status')
    venuesStatus.value = response.data.venues
    ElMessage.success('状态更新成功')
  } catch (error) {
    console.error('获取考场状态失败:', error)
    ElMessage.error('获取考场状态失败')
  }
}

// 组件挂载时初始化数据
onMounted(() => {
  refreshVenuesStatus()
})
</script>

<style scoped>
.dashboard {
  padding: 0;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
}

.page-header p {
  color: #909399;
  font-size: 14px;
}

.stats-row {
  margin-bottom: 24px;
}

.stat-card {
  border: none;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: 600;
  color: #303133;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  color: #909399;
  font-size: 14px;
  margin-bottom: 4px;
}

.stat-change {
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.stat-change.up {
  color: #67C23A;
}

.stat-change.down {
  color: #F56C6C;
}

.content-row {
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.venues-monitor {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.venue-item {
  padding: 16px;
  border: 1px solid #EBEEF5;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.venue-item:hover {
  border-color: #409EFF;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.venue-item.进行中 {
  border-left: 4px solid #F56C6C;
}

.venue-item.空闲 {
  border-left: 4px solid #67C23A;
}

.venue-item.维护中 {
  border-left: 4px solid #E6A23C;
}

.venue-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.venue-header h4 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.venue-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
}

.detail-item .label {
  color: #909399;
}

.detail-item .value {
  color: #303133;
  font-weight: 500;
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.action-btn {
  width: 100%;
  height: 48px;
  font-size: 16px;
}

.activities {
  max-height: 300px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #F0F0F0;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-time {
  font-size: 12px;
  color: #C0C4CC;
  white-space: nowrap;
  min-width: 60px;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-size: 14px;
  color: #303133;
  font-weight: 500;
  margin-bottom: 4px;
}

.activity-desc {
  font-size: 12px;
  color: #909399;
}
</style>