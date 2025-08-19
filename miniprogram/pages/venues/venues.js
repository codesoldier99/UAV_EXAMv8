/**
 * 考场状态页面
 */
const app = getApp()

Page({
  data: {
    venues: [],
    loading: false,
    refreshing: false,
    summary: {
      total_venues: 0,
      active_venues: 0,
      total_waiting: 0
    },
    updateTime: ''
  },

  onLoad() {
    console.log('考场状态页面加载')
    this.loadVenuesData()
    
    // 设置定时刷新（每10秒）
    this.timer = setInterval(() => {
      this.loadVenuesData(false)
    }, 10000)
  },

  onUnload() {
    // 清除定时器
    if (this.timer) {
      clearInterval(this.timer)
    }
  },

  onShow() {
    this.loadVenuesData()
  },

  onPullDownRefresh() {
    this.loadVenuesData(true)
  },

  // 加载考场数据
  loadVenuesData(showLoading = true) {
    if (showLoading) {
      this.setData({ loading: true })
    }
    
    wx.request({
      url: `${app.globalData.apiBaseUrl}/wechat/venues/status`,
      method: 'GET',
      header: {
        'content-type': 'application/json'
      },
      success: (res) => {
        console.log('获取考场状态成功', res.data)
        if (res.statusCode === 200) {
          this.setData({
            venues: res.data.map(venue => ({
              ...venue,
              status_color: this.getStatusColor(venue.status),
              status_text: this.getStatusText(venue.status)
            })),
            updateTime: new Date().toLocaleTimeString()
          })
          
          // 计算汇总信息
          this.calculateSummary()
        }
      },
      fail: (err) => {
        console.error('获取考场状态失败', err)
        wx.showToast({
          title: '获取数据失败',
          icon: 'error'
        })
      },
      complete: () => {
        this.setData({ loading: false })
        if (showLoading) {
          wx.stopPullDownRefresh()
        }
      }
    })
  },

  // 计算汇总信息
  calculateSummary() {
    const venues = this.data.venues
    const summary = {
      total_venues: venues.length,
      active_venues: venues.filter(v => v.status === 'available').length,
      total_waiting: venues.reduce((sum, v) => sum + v.waiting_count, 0)
    }
    this.setData({ summary })
  },

  // 获取状态颜色
  getStatusColor(status) {
    const colors = {
      'available': '#52c41a',
      'occupied': '#ff4d4f', 
      'maintenance': '#faad14',
      'disabled': '#d9d9d9'
    }
    return colors[status] || '#d9d9d9'
  },

  // 获取状态文本
  getStatusText(status) {
    const texts = {
      'available': '可用',
      'occupied': '占用中',
      'maintenance': '维护中', 
      'disabled': '已禁用'
    }
    return texts[status] || '未知'
  },

  // 手动刷新
  onRefresh() {
    this.setData({ refreshing: true })
    this.loadVenuesData()
    setTimeout(() => {
      this.setData({ refreshing: false })
    }, 1000)
  },

  // 查看考场详情
  onVenueDetail(e) {
    const { venue } = e.currentTarget.dataset
    wx.showModal({
      title: venue.venue_name,
      content: `类型：${venue.venue_type}\n容量：${venue.capacity}人\n等待：${venue.waiting_count}人\n${venue.current_candidate ? '当前：' + venue.current_candidate : ''}`,
      showCancel: false,
      confirmText: '知道了'
    })
  }
})
