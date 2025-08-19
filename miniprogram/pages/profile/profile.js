/**
 * 个人中心页面
 */
const app = getApp()

Page({
  data: {
    userInfo: null,
    isLoggedIn: false,
    idCard: '',
    openid: '',
    schedules: [],
    qrCodeData: '',
    showQRCode: false,
    queuePosition: null
  },

  onLoad() {
    console.log('个人中心页面加载')
    this.checkLoginStatus()
  },

  onShow() {
    this.checkLoginStatus()
    if (this.data.isLoggedIn) {
      this.loadUserData()
    }
  },

  // 检查登录状态
  checkLoginStatus() {
    const userInfo = wx.getStorageSync('userInfo')
    const accessToken = wx.getStorageSync('access_token')
    
    if (userInfo && accessToken) {
      this.setData({
        userInfo,
        isLoggedIn: true
      })
    } else {
      this.setData({
        userInfo: null,
        isLoggedIn: false
      })
    }
  },

  // 加载用户数据
  loadUserData() {
    if (this.data.userInfo.role === 'candidate') {
      this.loadCandidateSchedules()
      this.loadQueuePosition()
    }
  },

  // 微信登录
  onWeChatLogin() {
    wx.login({
      success: (res) => {
        if (res.code) {
          // 获取openid（这里简化处理）
          this.setData({
            openid: 'mock_openid_' + Date.now()
          })
          this.showLoginForm()
        } else {
          wx.showToast({
            title: '微信登录失败',
            icon: 'error'
          })
        }
      },
      fail: () => {
        wx.showToast({
          title: '微信登录失败',
          icon: 'error'
        })
      }
    })
  },

  // 显示登录表单
  showLoginForm() {
    wx.showModal({
      title: '身份证登录',
      content: '请输入您的身份证号',
      editable: true,
      placeholderText: '身份证号',
      success: (res) => {
        if (res.confirm && res.content) {
          this.performLogin(res.content)
        }
      }
    })
  },

  // 执行登录
  performLogin(idCard) {
    wx.showLoading({
      title: '登录中...'
    })

    wx.request({
      url: `${app.globalData.apiBaseUrl}/wechat/login`,
      method: 'POST',
      header: {
        'content-type': 'application/json'
      },
      data: {
        id_card: idCard,
        openid: this.data.openid
      },
      success: (res) => {
        console.log('登录响应', res.data)
        wx.hideLoading()
        
        if (res.statusCode === 200) {
          // 保存登录信息
          wx.setStorageSync('access_token', res.data.access_token)
          wx.setStorageSync('userInfo', res.data.user)
          
          this.setData({
            userInfo: res.data.user,
            isLoggedIn: true,
            idCard
          })
          
          wx.showToast({
            title: '登录成功',
            icon: 'success'
          })
          
          this.loadUserData()
        } else {
          wx.showToast({
            title: res.data.detail || '登录失败',
            icon: 'error'
          })
        }
      },
      fail: (err) => {
        console.error('登录失败', err)
        wx.hideLoading()
        wx.showToast({
          title: '网络错误',
          icon: 'error'
        })
      }
    })
  },

  // 加载考生日程
  loadCandidateSchedules() {
    wx.request({
      url: `${app.globalData.apiBaseUrl}/wechat/candidate/schedule`,
      method: 'GET',
      header: {
        'Authorization': `Bearer ${wx.getStorageSync('access_token')}`
      },
      success: (res) => {
        if (res.statusCode === 200) {
          this.setData({
            schedules: res.data
          })
        }
      },
      fail: (err) => {
        console.error('获取日程失败', err)
      }
    })
  },

  // 加载排队位置
  loadQueuePosition() {
    wx.request({
      url: `${app.globalData.apiBaseUrl}/wechat/candidate/queue-position`,
      method: 'GET',
      header: {
        'Authorization': `Bearer ${wx.getStorageSync('access_token')}`
      },
      success: (res) => {
        if (res.statusCode === 200) {
          this.setData({
            queuePosition: res.data
          })
        }
      },
      fail: (err) => {
        console.error('获取排队位置失败', err)
      }
    })
  },

  // 显示二维码
  showMyQRCode() {
    wx.request({
      url: `${app.globalData.apiBaseUrl}/wechat/candidate/qrcode`,
      method: 'GET',
      header: {
        'Authorization': `Bearer ${wx.getStorageSync('access_token')}`
      },
      success: (res) => {
        if (res.statusCode === 200) {
          this.setData({
            qrCodeData: res.data.qr_code,
            showQRCode: true
          })
        }
      },
      fail: (err) => {
        console.error('获取二维码失败', err)
        wx.showToast({
          title: '获取二维码失败',
          icon: 'error'
        })
      }
    })
  },

  // 关闭二维码
  closeQRCode() {
    this.setData({
      showQRCode: false,
      qrCodeData: ''
    })
  },

  // 查看日程详情
  onScheduleDetail(e) {
    const { schedule } = e.currentTarget.dataset
    wx.showModal({
      title: '日程详情',
      content: `考试：${schedule.exam_product_name}\n考场：${schedule.venue_name}\n时间：${schedule.start_time}\n状态：${schedule.status}`,
      showCancel: false,
      confirmText: '知道了'
    })
  },

  // 退出登录
  logout() {
    wx.showModal({
      title: '确认退出',
      content: '确定要退出登录吗？',
      success: (res) => {
        if (res.confirm) {
          wx.clearStorageSync()
          this.setData({
            userInfo: null,
            isLoggedIn: false,
            schedules: [],
            queuePosition: null
          })
          wx.showToast({
            title: '已退出登录',
            icon: 'success'
          })
        }
      }
    })
  },

  // 刷新数据
  onRefresh() {
    if (this.data.isLoggedIn) {
      this.loadUserData()
      wx.showToast({
        title: '刷新成功',
        icon: 'success'
      })
    }
  }
})
