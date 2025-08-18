/**
 * 小程序首页逻辑
 */
const app = getApp()

Page({
  data: {
    userInfo: {},
    hasUserInfo: false,
    canIUseGetUserProfile: false,
    systemStats: {
      totalVenues: 0,
      activeVenues: 0,
      todayCheckins: 0,
      waitingCount: 0
    },
    quickActions: [
      {
        id: 'venues',
        name: '考场状态',
        icon: 'venue',
        color: '#1890FF',
        path: '/pages/venues/venues'
      },
      {
        id: 'checkin',
        name: '扫码签到',
        icon: 'checkin',
        color: '#52C41A',
        path: '/pages/checkin/checkin'
      },
      {
        id: 'schedule',
        name: '考试安排',
        icon: 'schedule',
        color: '#FA8C16',
        path: '/pages/schedule/schedule'
      },
      {
        id: 'profile',
        name: '个人中心',
        icon: 'profile',
        color: '#722ED1',
        path: '/pages/profile/profile'
      }
    ],
    announcements: [],
    loading: false
  },

  onLoad() {
    console.log('首页加载')
    
    // 检查是否支持getUserProfile
    if (wx.canIUse('getUserProfile')) {
      this.setData({
        canIUseGetUserProfile: true
      })
    }

    // 加载首页数据
    this.loadHomeData()
  },

  onShow() {
    console.log('首页显示')
    
    // 获取用户信息
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    }
    
    // 刷新数据
    this.refreshData()
  },

  onPullDownRefresh() {
    console.log('下拉刷新')
    this.refreshData()
  },

  // 获取用户信息
  getUserProfile() {
    wx.getUserProfile({
      desc: '用于完善用户资料',
      success: (res) => {
        console.log('获取用户信息成功', res)
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
        app.globalData.userInfo = res.userInfo
      },
      fail: (err) => {
        console.log('获取用户信息失败', err)
        wx.showToast({
          title: '获取用户信息失败',
          icon: 'error'
        })
      }
    })
  },

  // 加载首页数据
  loadHomeData() {
    this.setData({ loading: true })
    
    // 获取系统统计数据
    this.getSystemStats()
    
    // 获取公告信息
    this.getAnnouncements()
  },

  // 刷新数据
  refreshData() {
    this.loadHomeData()
    
    // 停止下拉刷新
    setTimeout(() => {
      wx.stopPullDownRefresh()
      this.setData({ loading: false })
    }, 1000)
  },

  // 获取系统统计数据
  getSystemStats() {
    wx.request({
      url: `${app.globalData.apiBaseUrl}/public/venues/status`,
      method: 'GET',
      header: {
        'content-type': 'application/json'
      },
      success: (res) => {
        console.log('获取系统统计成功', res.data)
        if (res.statusCode === 200) {
          const { venues, summary } = res.data
          this.setData({
            systemStats: {
              totalVenues: summary.total_venues || 0,
              activeVenues: summary.active_venues || 0,
              todayCheckins: 128, // 模拟数据
              waitingCount: summary.total_waiting || 0
            }
          })
        }
      },
      fail: (err) => {
        console.error('获取系统统计失败', err)
        wx.showToast({
          title: '获取数据失败',
          icon: 'error'
        })
      }
    })
  },

  // 获取公告信息
  getAnnouncements() {
    // 模拟公告数据
    const announcements = [
      {
        id: 1,
        title: '系统维护通知',
        content: '系统将于今晚22:00-24:00进行维护升级',
        time: '2025-08-18 14:30',
        type: 'warning'
      },
      {
        id: 2,
        title: '新功能上线',
        content: '考场实时状态监控功能已上线',
        time: '2025-08-18 10:00',
        type: 'info'
      }
    ]
    
    this.setData({
      announcements
    })
  },

  // 快速操作点击
  onQuickActionTap(e) {
    const { action } = e.currentTarget.dataset
    const actionItem = this.data.quickActions.find(item => item.id === action)
    
    if (actionItem && actionItem.path) {
      wx.navigateTo({
        url: actionItem.path,
        fail: (err) => {
          console.error('页面跳转失败', err)
          wx.showToast({
            title: '功能开发中',
            icon: 'none'
          })
        }
      })
    }
  },

  // 查看公告详情
  viewAnnouncement(e) {
    const { id } = e.currentTarget.dataset
    const announcement = this.data.announcements.find(item => item.id === id)
    
    if (announcement) {
      wx.showModal({
        title: announcement.title,
        content: announcement.content,
        showCancel: false,
        confirmText: '我知道了'
      })
    }
  },

  // 跳转到考场状态页面
  goToVenues() {
    wx.switchTab({
      url: '/pages/venues/venues'
    })
  },

  // 跳转到扫码签到页面
  goToCheckin() {
    wx.switchTab({
      url: '/pages/checkin/checkin'
    })
  }
})