/**
 * 考生管理API
 */
import request from './index'
import { API_ENDPOINTS } from './config'

/**
 * 获取考生列表
 * @param {Object} params - 查询参数
 * @param {number} params.skip - 跳过数量
 * @param {number} params.limit - 限制数量
 * @param {number} params.institution_id - 机构ID
 * @param {number} params.exam_product_id - 考试产品ID
 * @param {string} params.status - 状态
 */
export function getCandidateList(params = {}) {
  return request({
    url: API_ENDPOINTS.CANDIDATES.LIST,
    method: 'get',
    params
  })
}

/**
 * 获取考生详情
 * @param {number} id - 考生ID
 */
export function getCandidateDetail(id) {
  return request({
    url: API_ENDPOINTS.CANDIDATES.DETAIL(id),
    method: 'get'
  })
}

/**
 * 创建考生
 * @param {Object} data - 考生数据
 * @param {string} data.real_name - 真实姓名
 * @param {string} data.id_card - 身份证号
 * @param {number} data.exam_product_id - 考试产品ID
 * @param {number} data.institution_id - 机构ID
 * @param {string} data.phone - 手机号
 * @param {string} data.email - 邮箱
 */
export function createCandidate(data) {
  return request({
    url: API_ENDPOINTS.CANDIDATES.CREATE,
    method: 'post',
    data
  })
}

/**
 * 更新考生信息
 * @param {number} id - 考生ID
 * @param {Object} data - 更新数据
 */
export function updateCandidate(id, data) {
  return request({
    url: API_ENDPOINTS.CANDIDATES.UPDATE(id),
    method: 'put',
    data
  })
}

/**
 * 删除考生
 * @param {number} id - 考生ID
 */
export function deleteCandidate(id) {
  return request({
    url: API_ENDPOINTS.CANDIDATES.DELETE(id),
    method: 'delete'
  })
}

/**
 * 批量导入考生
 * @param {File} file - Excel文件
 */
export function batchImportCandidates(file) {
  const formData = new FormData()
  formData.append('file', file)
  
  return request({
    url: API_ENDPOINTS.CANDIDATES.BATCH_IMPORT,
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

/**
 * 下载考生导入模板
 */
export function downloadCandidateTemplate() {
  return request({
    url: API_ENDPOINTS.CANDIDATES.TEMPLATE,
    method: 'get',
    responseType: 'blob'
  })
}

/**
 * 获取考生统计信息
 */
export function getCandidateStatistics() {
  return request({
    url: API_ENDPOINTS.CANDIDATES.STATISTICS,
    method: 'get'
  })
}

/**
 * 验证身份证号格式
 * @param {string} idCard - 身份证号
 */
export function validateIdCard(idCard) {
  if (!idCard) return false
  
  // 18位身份证号正则
  const pattern = /^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/
  
  if (!pattern.test(idCard)) {
    return false
  }
  
  // 验证校验码
  const factors = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
  const checkCodes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
  
  let sum = 0
  for (let i = 0; i < 17; i++) {
    sum += parseInt(idCard[i]) * factors[i]
  }
  
  const checkCode = checkCodes[sum % 11]
  return checkCode === idCard[17].toUpperCase()
}

/**
 * 验证手机号格式
 * @param {string} phone - 手机号
 */
export function validatePhone(phone) {
  if (!phone) return true // 手机号可选
  
  const pattern = /^1[3-9]\d{9}$/
  return pattern.test(phone)
}

/**
 * 验证邮箱格式
 * @param {string} email - 邮箱
 */
export function validateEmail(email) {
  if (!email) return true // 邮箱可选
  
  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return pattern.test(email)
}

/**
 * 验证考生数据
 * @param {Object} data - 考生数据
 */
export function validateCandidateData(data) {
  const errors = {}
  
  if (!data.real_name || data.real_name.trim().length === 0) {
    errors.real_name = '姓名不能为空'
  } else if (data.real_name.length > 50) {
    errors.real_name = '姓名不能超过50个字符'
  }
  
  if (!data.id_card || data.id_card.trim().length === 0) {
    errors.id_card = '身份证号不能为空'
  } else if (!validateIdCard(data.id_card)) {
    errors.id_card = '身份证号格式不正确'
  }
  
  if (!data.exam_product_id) {
    errors.exam_product_id = '请选择考试产品'
  }
  
  if (!data.institution_id) {
    errors.institution_id = '请选择机构'
  }
  
  if (data.phone && !validatePhone(data.phone)) {
    errors.phone = '手机号格式不正确'
  }
  
  if (data.email && !validateEmail(data.email)) {
    errors.email = '邮箱格式不正确'
  }
  
  return {
    isValid: Object.keys(errors).length === 0,
    errors
  }
}

/**
 * 格式化考生状态
 * @param {string} status - 状态
 */
export function formatCandidateStatus(status) {
  const statusMap = {
    'pending': { text: '待审核', type: 'warning' },
    'approved': { text: '已通过', type: 'success' },
    'rejected': { text: '已拒绝', type: 'danger' },
    'cancelled': { text: '已取消', type: 'info' }
  }
  
  return statusMap[status] || { text: '未知', type: 'info' }
}
