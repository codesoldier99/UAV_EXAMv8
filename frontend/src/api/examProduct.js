/**
 * 考试产品管理API
 */
import request from './index'
import { API_ENDPOINTS } from './config'

/**
 * 获取考试产品列表
 * @param {Object} params - 查询参数
 * @param {number} params.skip - 跳过数量
 * @param {number} params.limit - 限制数量
 * @param {boolean} params.is_active - 是否启用
 * @param {string} params.exam_type - 考试类型
 */
export function getExamProductList(params = {}) {
  return request({
    url: API_ENDPOINTS.EXAM_PRODUCTS.LIST,
    method: 'get',
    params
  })
}

/**
 * 获取考试产品详情
 * @param {number} id - 产品ID
 */
export function getExamProductDetail(id) {
  return request({
    url: API_ENDPOINTS.EXAM_PRODUCTS.DETAIL(id),
    method: 'get'
  })
}

/**
 * 创建考试产品
 * @param {Object} data - 产品数据
 * @param {string} data.name - 产品名称
 * @param {string} data.code - 产品代码
 * @param {string} data.description - 产品描述
 * @param {number} data.duration_minutes - 考试时长（分钟）
 * @param {string} data.exam_type - 考试类型
 * @param {boolean} data.is_active - 是否启用
 */
export function createExamProduct(data) {
  return request({
    url: API_ENDPOINTS.EXAM_PRODUCTS.CREATE,
    method: 'post',
    data
  })
}

/**
 * 更新考试产品
 * @param {number} id - 产品ID
 * @param {Object} data - 更新数据
 */
export function updateExamProduct(id, data) {
  return request({
    url: API_ENDPOINTS.EXAM_PRODUCTS.UPDATE(id),
    method: 'put',
    data
  })
}

/**
 * 删除考试产品
 * @param {number} id - 产品ID
 */
export function deleteExamProduct(id) {
  return request({
    url: API_ENDPOINTS.EXAM_PRODUCTS.DELETE(id),
    method: 'delete'
  })
}

/**
 * 切换考试产品状态
 * @param {number} id - 产品ID
 */
export function toggleExamProductStatus(id) {
  return request({
    url: API_ENDPOINTS.EXAM_PRODUCTS.TOGGLE_STATUS(id),
    method: 'post'
  })
}

/**
 * 获取考试类型选项
 */
export function getExamTypeOptions() {
  return [
    { label: '理论考试', value: '理论' },
    { label: '实操考试', value: '实操' }
  ]
}

/**
 * 验证考试产品数据
 * @param {Object} data - 产品数据
 */
export function validateExamProductData(data) {
  const errors = {}
  
  if (!data.name || data.name.trim().length === 0) {
    errors.name = '产品名称不能为空'
  } else if (data.name.length > 200) {
    errors.name = '产品名称不能超过200个字符'
  }
  
  if (!data.code || data.code.trim().length === 0) {
    errors.code = '产品代码不能为空'
  } else if (data.code.length > 50) {
    errors.code = '产品代码不能超过50个字符'
  } else if (!/^[A-Z0-9_]+$/.test(data.code)) {
    errors.code = '产品代码只能包含大写字母、数字和下划线'
  }
  
  if (!data.exam_type) {
    errors.exam_type = '请选择考试类型'
  }
  
  if (!data.duration_minutes || data.duration_minutes <= 0) {
    errors.duration_minutes = '考试时长必须大于0'
  } else if (data.duration_minutes > 480) {
    errors.duration_minutes = '考试时长不能超过8小时'
  }
  
  return {
    isValid: Object.keys(errors).length === 0,
    errors
  }
}
