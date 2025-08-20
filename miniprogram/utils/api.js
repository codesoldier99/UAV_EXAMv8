/**
 * API接口工具类
 */
const app = getApp()

// API基础配置
const API_BASE_URL = 'http://localhost:8000/api/v1'

/**
 * 网络请求封装
 */
function request(options) {
  return new Promise((resolve, reject) => {
    // 显示加载提示
    if (options.loading !== false) {
      wx.showLoading({
        title: options.loadingText || '加载中...',
        mask: true
      })
    }

    wx.request({
      url: `${API_BASE_URL}${options.url}`,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        'content-type': 'application/json',
        ...options.header
      },
      success: (res) => {
        // 隐藏加载提示
        if (options.loading !== false) {
          wx.hideLoading()
        }

        if (res.statusCode === 200) {
          resolve(res.data)
        } else {
          // 处理HTTP错误状态码
          handleError(res.statusCode, res.data)
          reject(res)
        }
      },
      fail: (err) => {
        // 隐藏加载提示
        if (options.loading !== false) {
          wx.hideLoading()
        }

        // 处理网络错误
        console.error('网络请求失败:', err)
        wx.showToast({
          title: '网络连接失败',
          icon: 'error',
          duration: 2000
        })
        reject(err)
      }
    })
  })
}

/**
 * 处理API错误
 */
function handleError(statusCode, data) {
  let message = '请求失败'
  
  switch (statusCode) {
    case 400:
      message = data?.detail || '请求参数错误'
      break
    case 401:
      message = '登录已过期，请重新登录'
      // 清除本地认证信息
      wx.removeStorageSync('token')
      wx.removeStorageSync('userInfo')
      break
    case 403:
      message = '没有权限访问'
      break
    case 404:
      message = '请求的资源不存在'
      break
    case 500:
      message = '服务器内部错误'
      break
    default:
      message = data?.detail || data?.message || '未知错误'
  }

  wx.showToast({
    title: message,
    icon: 'error',
    duration: 3000
  })
}

/**
 * GET请求
 */
function get(url, params = {}, options = {}) {
  const query = Object.keys(params).map(key => 
    `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`
  ).join('&')
  
  const requestUrl = query ? `${url}?${query}` : url
  
  return request({
    url: requestUrl,
    method: 'GET',
    ...options
  })
}

/**
 * POST请求
 */
function post(url, data = {}, options = {}) {
  return request({
    url,
    method: 'POST',
    data,
    ...options
  })
}

/**
 * PUT请求
 */
function put(url, data = {}, options = {}) {
  return request({
    url,
    method: 'PUT',
    data,
    ...options
  })
}

/**
 * DELETE请求
 */
function del(url, options = {}) {
  return request({
    url,
    method: 'DELETE',
    ...options
  })
}

/**
 * 上传文件
 */
function upload(filePath, options = {}) {
  return new Promise((resolve, reject) => {
    wx.showLoading({
      title: '上传中...',
      mask: true
    })

    wx.uploadFile({
      url: `${API_BASE_URL}${options.url}`,
      filePath,
      name: options.name || 'file',
      formData: options.data || {},
      header: options.header || {},
      success: (res) => {
        wx.hideLoading()
        
        try {
          const data = JSON.parse(res.data)
          resolve(data)
        } catch (e) {
          resolve(res.data)
        }
      },
      fail: (err) => {
        wx.hideLoading()
        console.error('文件上传失败:', err)
        wx.showToast({
          title: '上传失败',
          icon: 'error'
        })
        reject(err)
      }
    })
  })
}

// 导出API方法
module.exports = {
  // 基础请求方法
  request,
  get,
  post,
  put,
  delete: del,
  upload,

  // 公共API（无需认证）
  getVenuesStatus: () => get('/public/venues-status', {}, { loading: false }),
  candidateLogin: (data) => post('/public/candidate/login', data),
  getCandidateQRCode: (candidateId) => get(`/public/candidate/${candidateId}/qrcode`),
  checkinCandidate: (data) => post('/public/checkin', data),
  getTodaySchedule: () => get('/public/schedule/today'),
  getPublicInstitutions: () => get('/public/institutions'),
  getPublicExamProducts: () => get('/public/exam-products'),
  healthCheck: () => get('/public/health'),

  // 认证相关API
  auth: {
    login: (data) => post('/auth/login', data),
    logout: () => post('/auth/logout'),
    getCurrentUser: () => get('/auth/me'),
    refreshToken: () => post('/auth/refresh')
  },

  // 考场相关API
  venues: {
    getVenues: (params) => get('/venues', params),
    getVenue: (id) => get(`/venues/${id}`),
    createVenue: (data) => post('/venues', data),
    updateVenue: (id, data) => put(`/venues/${id}`, data),
    deleteVenue: (id) => del(`/venues/${id}`)
  },

  // 机构相关API
  institutions: {
    getInstitutions: (params) => get('/institutions', params),
    getInstitution: (id) => get(`/institutions/${id}`),
    createInstitution: (data) => post('/institutions', data),
    updateInstitution: (id, data) => put(`/institutions/${id}`, data)
  },

  // 考生相关API
  candidates: {
    getCandidates: (params) => get('/candidates', params),
    getCandidate: (id) => get(`/candidates/${id}`),
    createCandidate: (data) => post('/candidates', data),
    updateCandidate: (id, data) => put(`/candidates/${id}`, data),
    deleteCandidate: (id) => del(`/candidates/${id}`),
    importCandidates: (file) => upload(file, { url: '/candidates/import', name: 'file' })
  },

  // 考试产品相关API
  examProducts: {
    getExamProducts: (params) => get('/exam-products', params),
    getExamProduct: (id) => get(`/exam-products/${id}`),
    createExamProduct: (data) => post('/exam-products', data),
    updateExamProduct: (id, data) => put(`/exam-products/${id}`, data)
  },

  // 日程相关API
  schedules: {
    getSchedules: (params) => get('/schedules', params),
    getSchedule: (id) => get(`/schedules/${id}`),
    createSchedule: (data) => post('/schedules', data),
    updateSchedule: (id, data) => put(`/schedules/${id}`, data),
    deleteSchedule: (id) => del(`/schedules/${id}`),
    batchCreateSchedules: (data) => post('/schedules/batch', data)
  },

  // 用户相关API
  users: {
    getUsers: (params) => get('/users', params),
    getUser: (id) => get(`/users/${id}`),
    createUser: (data) => post('/users', data),
    updateUser: (id, data) => put(`/users/${id}`, data),
    deleteUser: (id) => del(`/users/${id}`)
  }
}