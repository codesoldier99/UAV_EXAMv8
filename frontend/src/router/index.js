/**
 * Vue Router 配置
 */
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/user'

// 路由组件懒加载
const Login = () => import('@/views/Login.vue')
const Dashboard = () => import('@/views/Dashboard.vue')
const Layout = () => import('@/components/Layout.vue')

// 机构管理
const InstitutionList = () => import('@/views/institution/InstitutionList.vue')
const InstitutionDetail = () => import('@/views/institution/InstitutionDetail.vue')

// 考场管理
const VenueList = () => import('@/views/venue/VenueList.vue')
const VenueDetail = () => import('@/views/venue/VenueDetail.vue')
const VenueMonitor = () => import('@/views/venue/VenueMonitor.vue')

// 考试管理
const ExamList = () => import('@/views/exam/ExamList.vue')
const ExamDetail = () => import('@/views/exam/ExamDetail.vue')
const ExamSchedule = () => import('@/views/exam/ExamSchedule.vue')

// 考生管理
const CandidateList = () => import('@/views/candidate/CandidateList.vue')
const CandidateDetail = () => import('@/views/candidate/CandidateDetail.vue')
const CandidateImport = () => import('@/views/candidate/CandidateImport.vue')

// 签到管理
const CheckinList = () => import('@/views/checkin/CheckinList.vue')
const CheckinMonitor = () => import('@/views/checkin/CheckinMonitor.vue')

// 系统管理
const UserList = () => import('@/views/system/UserList.vue')
const Settings = () => import('@/views/system/Settings.vue')

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { 
      title: '登录',
      requiresAuth: false 
    }
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: { 
          title: '控制台',
          icon: 'HomeFilled'
        }
      }
    ]
  },
  {
    path: '/institution',
    component: Layout,
    meta: { 
      title: '机构管理',
      icon: 'OfficeBuilding',
      requiresAuth: true 
    },
    children: [
      {
        path: '',
        name: 'InstitutionList',
        component: InstitutionList,
        meta: { title: '机构列表' }
      },
      {
        path: ':id',
        name: 'InstitutionDetail',
        component: InstitutionDetail,
        meta: { title: '机构详情' }
      }
    ]
  },
  {
    path: '/venue',
    component: Layout,
    meta: { 
      title: '考场管理',
      icon: 'School',
      requiresAuth: true 
    },
    children: [
      {
        path: '',
        name: 'VenueList',
        component: VenueList,
        meta: { title: '考场列表' }
      },
      {
        path: ':id',
        name: 'VenueDetail',
        component: VenueDetail,
        meta: { title: '考场详情' }
      },
      {
        path: 'monitor',
        name: 'VenueMonitor',
        component: VenueMonitor,
        meta: { title: '考场监控' }
      }
    ]
  },
  {
    path: '/exam',
    component: Layout,
    meta: { 
      title: '考试管理',
      icon: 'EditPen',
      requiresAuth: true 
    },
    children: [
      {
        path: '',
        name: 'ExamList',
        component: ExamList,
        meta: { title: '考试列表' }
      },
      {
        path: ':id',
        name: 'ExamDetail',
        component: ExamDetail,
        meta: { title: '考试详情' }
      },
      {
        path: 'schedule',
        name: 'ExamSchedule',
        component: ExamSchedule,
        meta: { title: '考试排期' }
      }
    ]
  },
  {
    path: '/candidate',
    component: Layout,
    meta: { 
      title: '考生管理',
      icon: 'User',
      requiresAuth: true 
    },
    children: [
      {
        path: '',
        name: 'CandidateList',
        component: CandidateList,
        meta: { title: '考生列表' }
      },
      {
        path: ':id',
        name: 'CandidateDetail',
        component: CandidateDetail,
        meta: { title: '考生详情' }
      },
      {
        path: 'import',
        name: 'CandidateImport',
        component: CandidateImport,
        meta: { title: '批量导入' }
      }
    ]
  },
  {
    path: '/checkin',
    component: Layout,
    meta: { 
      title: '签到管理',
      icon: 'Checked',
      requiresAuth: true 
    },
    children: [
      {
        path: '',
        name: 'CheckinList',
        component: CheckinList,
        meta: { title: '签到列表' }
      },
      {
        path: 'monitor',
        name: 'CheckinMonitor',
        component: CheckinMonitor,
        meta: { title: '签到监控' }
      }
    ]
  },
  {
    path: '/system',
    component: Layout,
    meta: { 
      title: '系统管理',
      icon: 'Setting',
      requiresAuth: true,
      roles: ['admin', 'super_admin']
    },
    children: [
      {
        path: 'users',
        name: 'UserList',
        component: UserList,
        meta: { title: '用户管理' }
      },
      {
        path: 'settings',
        name: 'Settings',
        component: Settings,
        meta: { title: '系统设置' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - UAV考点运营管理系统` : 'UAV考点运营管理系统'
  
  // 检查认证
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next('/login')
    return
  }
  
  // 检查角色权限
  if (to.meta.roles && !to.meta.roles.includes(userStore.user?.role)) {
    next('/dashboard')
    return
  }
  
  // 已登录用户访问登录页重定向到首页
  if (to.path === '/login' && userStore.isAuthenticated) {
    next('/dashboard')
    return
  }
  
  next()
})

export default router