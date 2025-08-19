/**
 * API配置文件
 */

// 获取API基础URL
const getApiBaseUrl = () => {
  // 开发环境
  if (import.meta.env.DEV) {
    return 'http://localhost:8000'
  }
  
  // 生产环境
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }
  
  // 默认使用相对路径
  return ''
}

export const API_BASE_URL = getApiBaseUrl()

// API端点配置
export const API_ENDPOINTS = {
  // 认证相关
  AUTH: {
    LOGIN: '/api/v1/auth/token',
    REGISTER: '/api/v1/auth/register',
    ME: '/api/v1/auth/me',
    LOGOUT: '/api/v1/auth/logout',
    REFRESH: '/api/v1/auth/refresh'
  },
  
  // 机构管理
  INSTITUTIONS: {
    LIST: '/api/v1/institutions',
    CREATE: '/api/v1/institutions',
    DETAIL: (id) => `/api/v1/institutions/${id}`,
    UPDATE: (id) => `/api/v1/institutions/${id}`,
    DELETE: (id) => `/api/v1/institutions/${id}`,
    VENUES: (id) => `/api/v1/institutions/${id}/venues`,
    STATS: (id) => `/api/v1/institutions/${id}/stats`
  },
  
  // 考试产品
  EXAM_PRODUCTS: {
    LIST: '/api/v1/exam-products',
    CREATE: '/api/v1/exam-products',
    DETAIL: (id) => `/api/v1/exam-products/${id}`,
    UPDATE: (id) => `/api/v1/exam-products/${id}`,
    DELETE: (id) => `/api/v1/exam-products/${id}`,
    TOGGLE_STATUS: (id) => `/api/v1/exam-products/${id}/toggle-status`
  },
  
  // 考生管理
  CANDIDATES: {
    LIST: '/api/v1/candidates',
    CREATE: '/api/v1/candidates',
    DETAIL: (id) => `/api/v1/candidates/${id}`,
    UPDATE: (id) => `/api/v1/candidates/${id}`,
    DELETE: (id) => `/api/v1/candidates/${id}`,
    BATCH_IMPORT: '/api/v1/candidates/batch-import',
    TEMPLATE: '/api/v1/candidates/template/download',
    STATISTICS: '/api/v1/candidates/statistics'
  },
  
  // 微信小程序
  WECHAT: {
    LOGIN: '/api/v1/wechat/login',
    SCHEDULE: '/api/v1/wechat/candidate/schedule',
    QRCODE: '/api/v1/wechat/candidate/qrcode',
    VENUES_STATUS: '/api/v1/wechat/venues/status',
    CHECKIN: '/api/v1/wechat/checkin',
    QUEUE_POSITION: '/api/v1/wechat/candidate/queue-position',
    DASHBOARD: '/api/v1/wechat/dashboard'
  },
  
  // 公共接口
  PUBLIC: {
    VENUES_STATUS: '/api/v1/public/venues/status',
    SYSTEM_INFO: '/api/v1/system/info'
  },
  
  // 健康检查
  HEALTH: '/health'
}

// 请求配置
export const REQUEST_CONFIG = {
  timeout: 10000, // 10秒超时
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
}

// 响应状态码
export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  NO_CONTENT: 204,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  INTERNAL_SERVER_ERROR: 500
}

// 错误消息映射
export const ERROR_MESSAGES = {
  [HTTP_STATUS.BAD_REQUEST]: '请求参数错误',
  [HTTP_STATUS.UNAUTHORIZED]: '未登录或登录已过期',
  [HTTP_STATUS.FORBIDDEN]: '权限不足',
  [HTTP_STATUS.NOT_FOUND]: '请求的资源不存在',
  [HTTP_STATUS.INTERNAL_SERVER_ERROR]: '服务器内部错误',
  'NETWORK_ERROR': '网络连接失败',
  'TIMEOUT': '请求超时',
  'UNKNOWN': '未知错误'
}
