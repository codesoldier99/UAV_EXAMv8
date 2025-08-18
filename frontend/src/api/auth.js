/**
 * 认证相关API
 */
import api from './index'

export const authApi = {
  // 用户登录
  login: (data) => {
    const formData = new FormData()
    formData.append('username', data.username)
    formData.append('password', data.password)
    
    return api.post('/auth/token', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 用户注册
  register: (data) => {
    return api.post('/auth/register', data)
  },

  // 获取当前用户信息
  getCurrentUser: () => {
    return api.get('/auth/me')
  },

  // 刷新令牌
  refreshToken: () => {
    return api.post('/auth/refresh')
  },

  // 用户登出
  logout: () => {
    return api.post('/auth/logout')
  },

  // 修改密码
  changePassword: (data) => {
    return api.put('/auth/password', data)
  },

  // 忘记密码
  forgotPassword: (email) => {
    return api.post('/auth/forgot-password', { email })
  },

  // 重置密码
  resetPassword: (data) => {
    return api.post('/auth/reset-password', data)
  }
}