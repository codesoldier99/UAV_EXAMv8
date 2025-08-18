/**
 * 机构管理相关API
 */
import api from './index'

export const institutionApi = {
  // 获取机构列表
  getInstitutions: (params) => {
    return api.get('/institutions', { params })
  },

  // 获取机构详情
  getInstitution: (id) => {
    return api.get(`/institutions/${id}`)
  },

  // 创建机构
  createInstitution: (data) => {
    return api.post('/institutions', data)
  },

  // 更新机构信息
  updateInstitution: (id, data) => {
    return api.put(`/institutions/${id}`, data)
  },

  // 删除机构
  deleteInstitution: (id) => {
    return api.delete(`/institutions/${id}`)
  },

  // 获取机构考场列表
  getInstitutionVenues: (id, params) => {
    return api.get(`/institutions/${id}/venues`, { params })
  },

  // 获取机构统计信息
  getInstitutionStats: (id) => {
    return api.get(`/institutions/${id}/stats`)
  },

  // 审核机构
  approveInstitution: (id, approved) => {
    return api.put(`/institutions/${id}`, { is_approved: approved })
  },

  // 启用/禁用机构
  toggleInstitutionStatus: (id, isActive) => {
    return api.put(`/institutions/${id}`, { is_active: isActive })
  }
}