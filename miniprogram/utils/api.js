/**
 * API接口工具类
 */
const app = getApp()

// API基础配置
const API_BASE_URL = 'https://your-api-domain.com/api/v1'

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

  // 认证相关API
  auth: {
    login: (data) => post('/auth/login', data),
    logout: () => post('/auth/logout'),
    getCurrentUser: () => get('/auth/me'),
    refreshToken: () => post('/auth/refresh')
  },

  // 考场相关API
  venues: {
    getPublicStatus: () => get('/public/venues/status', {}, { loading: false }),
    getVenues: (params) => get('/venues', params),
    getVenue: (id) => get(`/venues/${id}`),
    checkin: (data) => post('/venues/checkin', data)
  },

  // 机构相关API
  institutions: {
    getList: (params) => get('/institutions', params),
    getDetail: (id) => get(`/institutions/${id}`),
    getStats: (id) => get(`/institutions/${id}/stats`)
  },

  // 考试相关API
  exams: {
    getList: (params) => get('/exams', params),
    getDetail: (id) => get(`/exams/${id}`),
    register: (data) => post('/exams/register', data)
  },

  // 签到相关API
  checkin: {
    scan: (data) => post('/checkin/scan', data),
    getHistory: (params) => get('/checkin/history', params),
    getStats: () => get('/checkin/stats')
  },

  // 微信小程序专用API
  wechat: {
    getDashboard: () => get('/wechat/venues/dashboard', {}, { loading: false }),
    login: (data) => post('/wechat/login', data),
    bindUser: (data) => post('/wechat/bind', data)
  }
}