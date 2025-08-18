/**
 * 用户状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import router from '@/router'

export const useUserStore = defineStore('user', () => {
  // 状态
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || '')
  const permissions = ref([])

  // 计算属性
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value && ['admin', 'super_admin'].includes(user.value.role))
  const isSuperAdmin = computed(() => user.value && user.value.role === 'super_admin')

  // 操作方法
  const login = async (loginForm) => {
    try {
      const response = await authApi.login(loginForm)
      const { access_token, user: userInfo } = response.data
      
      // 保存认证信息
      token.value = access_token
      user.value = userInfo
      permissions.value = userInfo.permissions || []
      
      // 持久化存储
      localStorage.setItem('token', access_token)
      localStorage.setItem('user', JSON.stringify(userInfo))
      
      return response
    } catch (error) {
      throw error
    }
  }

  const logout = async () => {
    try {
      // 调用后端登出接口
      await authApi.logout()
    } catch (error) {
      console.warn('登出接口调用失败:', error)
    } finally {
      // 清除本地状态
      clearAuth()
      router.push('/login')
    }
  }

  const getCurrentUser = async () => {
    try {
      const response = await authApi.getCurrentUser()
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(response.data))
      return response.data
    } catch (error) {
      // 获取用户信息失败，清除认证状态
      clearAuth()
      router.push('/login')
      throw error
    }
  }

  const refreshToken = async () => {
    try {
      const response = await authApi.refreshToken()
      const { access_token } = response.data
      
      token.value = access_token
      localStorage.setItem('token', access_token)
      
      return access_token
    } catch (error) {
      clearAuth()
      router.push('/login')
      throw error
    }
  }

  const initializeAuth = async (savedToken) => {
    if (!savedToken) return false
    
    token.value = savedToken
    
    try {
      // 尝试获取用户信息验证token有效性
      await getCurrentUser()
      return true
    } catch (error) {
      clearAuth()
      return false
    }
  }

  const clearAuth = () => {
    user.value = null
    token.value = ''
    permissions.value = []
    
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  const hasPermission = (permission) => {
    return permissions.value.includes(permission)
  }

  const hasRole = (role) => {
    return user.value && user.value.role === role
  }

  const hasAnyRole = (roles) => {
    return user.value && roles.includes(user.value.role)
  }

  return {
    // 状态
    user,
    token,
    permissions,
    
    // 计算属性
    isAuthenticated,
    isAdmin,
    isSuperAdmin,
    
    // 方法
    login,
    logout,
    getCurrentUser,
    refreshToken,
    initializeAuth,
    clearAuth,
    hasPermission,
    hasRole,
    hasAnyRole
  }
})