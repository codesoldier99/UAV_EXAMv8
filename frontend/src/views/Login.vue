<template>
  <div class="login-container">
    <div class="login-form">
      <div class="login-header">
        <h1>UAV考点运营管理系统</h1>
        <p>无人机考试管理平台</p>
      </div>

      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        size="large"
        label-position="top"
        @submit.prevent="handleLogin"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名/邮箱/手机号"
            :prefix-icon="User"
            clearable
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            :prefix-icon="Lock"
            show-password
            clearable
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-form-item>
          <div class="login-options">
            <el-checkbox v-model="rememberMe">记住我</el-checkbox>
            <el-link type="primary" :underline="false">忘记密码？</el-link>
          </div>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            @click="handleLogin"
            style="width: 100%"
          >
            {{ loading ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>
      </el-form>

      <div class="login-footer">
        <p>还没有账号？<el-link type="primary">立即注册</el-link></p>
      </div>
    </div>

    <!-- 系统特性展示 -->
    <div class="features-panel">
      <h2>系统特性</h2>
      <div class="feature-list">
        <div class="feature-item">
          <el-icon><Shield /></el-icon>
          <div>
            <h3>安全认证</h3>
            <p>JWT身份认证与RBAC权限管理</p>
          </div>
        </div>
        
        <div class="feature-item">
          <el-icon><OfficeBuilding /></el-icon>
          <div>
            <h3>机构管理</h3>
            <p>多机构考点运营管理</p>
          </div>
        </div>
        
        <div class="feature-item">
          <el-icon><User /></el-icon>
          <div>
            <h3>考生管理</h3>
            <p>考生报名与智能排期</p>
          </div>
        </div>
        
        <div class="feature-item">
          <el-icon><Phone /></el-icon>
          <div>
            <h3>移动支持</h3>
            <p>微信小程序扫码签到</p>
          </div>
        </div>
        
        <div class="feature-item">
          <el-icon><Monitor /></el-icon>
          <div>
            <h3>实时监控</h3>
            <p>考场状态实时监控</p>
          </div>
        </div>
        
        <div class="feature-item">
          <el-icon><Connection /></el-icon>
          <div>
            <h3>高并发</h3>
            <p>支持1200人并发访问</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { ElMessage } from 'element-plus'
import { 
  User, Lock, Shield, OfficeBuilding, 
  Phone, Monitor, Connection 
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

// 表单引用
const loginFormRef = ref()

// 表单数据
const loginForm = reactive({
  username: 'admin',
  password: 'admin123'
})

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 50, message: '用户名长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 50, message: '密码长度在 6 到 50 个字符', trigger: 'blur' }
  ]
}

// 其他状态
const loading = ref(false)
const rememberMe = ref(false)

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    // 表单验证
    await loginFormRef.value.validate()
    
    loading.value = true
    
    // 调用登录接口
    await userStore.login(loginForm)
    
    ElMessage.success('登录成功')
    
    // 跳转到首页
    const redirect = router.currentRoute.value.query.redirect || '/dashboard'
    router.replace(redirect)
    
  } catch (error) {
    console.error('登录失败:', error)
    ElMessage.error(error.response?.data?.detail || '登录失败，请检查用户名和密码')
  } finally {
    loading.value = false
  }
}

// 组件挂载
onMounted(() => {
  // 如果用户已登录，直接跳转到首页
  if (userStore.isAuthenticated) {
    router.replace('/dashboard')
  }
  
  // 如果选择了记住我，从本地存储恢复用户名
  const savedUsername = localStorage.getItem('rememberedUsername')
  if (savedUsername) {
    loginForm.username = savedUsername
    rememberMe.value = true
  }
})
</script>

<style scoped>
.login-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-form {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 40px;
  max-width: 500px;
  margin: 0 auto;
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
  color: white;
}

.login-header h1 {
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 8px;
}

.login-header p {
  font-size: 16px;
  opacity: 0.9;
}

.el-form {
  width: 100%;
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.login-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.login-footer {
  margin-top: 24px;
  text-align: center;
  color: white;
}

.features-panel {
  flex: 1;
  padding: 80px 60px;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  max-width: 600px;
}

.features-panel h2 {
  font-size: 36px;
  font-weight: 600;
  margin-bottom: 40px;
  text-align: center;
}

.feature-list {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 16px;
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 12px;
  backdrop-filter: blur(10px);
  transition: transform 0.3s ease;
}

.feature-item:hover {
  transform: translateY(-4px);
}

.feature-item .el-icon {
  font-size: 32px;
  color: #ffd700;
  flex-shrink: 0;
}

.feature-item h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 4px;
}

.feature-item p {
  font-size: 14px;
  opacity: 0.9;
  margin: 0;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .features-panel {
    display: none;
  }
  
  .login-form {
    max-width: none;
  }
}

@media (max-width: 768px) {
  .login-form {
    padding: 20px;
  }
  
  .el-form {
    padding: 30px 20px;
  }
  
  .login-header h1 {
    font-size: 24px;
  }
}
</style>