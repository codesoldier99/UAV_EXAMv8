/**
 * Pinia Store 主文件
 */
import { defineStore } from 'pinia'

// 导出所有 store
export { useUserStore } from './user'
export { useInstitutionStore } from './institution'
export { useVenueStore } from './venue'
export { useExamStore } from './exam'
export { useAppStore } from './app'