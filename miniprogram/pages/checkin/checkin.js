/**
 * 扫码签到页面
 */
const app = getApp()

Page({
  data: {
    userInfo: null,
    isExaminer: false,
    recentCheckins: [],
    stats: {
      todayCheckins: 0,
      successRate: 100
    }
  },

  onLoad() {
    console.log('扫码签到页面加载')
    this.checkUserRole()
    this.loadRecentCheckins()
  },

  onShow() {
    this.loadRecentCheckins()
  },

  // 检查用户角色
  checkUserRole() {
    const userInfo = wx.getStorageSync('userInfo')
    if (userInfo) {
      this.setData({
        userInfo,
        isExaminer: ['admin', 'examiner'].includes(userInfo.role)
      })
    } else {
      // 未登录，跳转到登录页
      wx.showModal({
        title: '提示',
        content: '请先登录后使用扫码功能',
        showCancel: false,
        success: () => {
          wx.switchTab({
            url: '/pages/profile/profile'
          })
        }
      })
    }
  },

  // 开始扫码
  startScan() {
    if (!this.data.isExaminer) {
      wx.showToast({
        title: '无扫码权限',
        icon: 'error'
      })
      return
    }

    wx.scanCode({
      success: (res) => {
        console.log('扫码成功', res)
        this.processQRCode(res.result)
      },
      fail: (err) => {
        console.error('扫码失败', err)
        if (err.errMsg.includes('cancel')) {
          return // 用户取消扫码
        }
        wx.showToast({
          title: '扫码失败',
          icon: 'error'
        })
      }
    })
  },

  // 处理二维码数据
  processQRCode(qrData) {
    try {
      const data = JSON.parse(qrData)
      console.log('二维码数据', data)
      
      if (data.type === 'candidate' && data.schedule_id) {
        this.performCheckin(data.schedule_id)
      } else {
        wx.showToast({
          title: '无效的二维码',
          icon: 'error'
        })
      }
    } catch (error) {
      console.error('解析二维码失败', error)
      wx.showToast({
        title: '二维码格式错误',
        icon: 'error'
      })
    }
  },

  // 执行签到
  performCheckin(scheduleId) {
    wx.showLoading({
      title: '签到中...'
    })

    wx.request({
      url: `${app.globalData.apiBaseUrl}/wechat/checkin`,
      method: 'POST',
      header: {
        'content-type': 'application/json',
        'Authorization': `Bearer ${wx.getStorageSync('access_token')}`
      },
      data: {
        schedule_id: scheduleId,
        venue_id: 1 // 这里应该根据实际情况获取考场ID
      },
      success: (res) => {
        console.log('签到响应', res.data)
        wx.hideLoading()
        
        if (res.statusCode === 200 && res.data.success) {
          wx.showToast({
            title: res.data.message,
            icon: 'success'
          })
          
          // 更新签到记录
          this.loadRecentCheckins()
          
          // 播放成功音效
          wx.vibrateShort()
        } else {
          wx.showToast({
            title: res.data.message || '签到失败',
            icon: 'error'
          })
        }
      },
      fail: (err) => {
        console.error('签到失败', err)
        wx.hideLoading()
        wx.showToast({
          title: '网络错误',
          icon: 'error'
        })
      }
    })
  },

  // 加载最近签到记录
  loadRecentCheckins() {
    // 模拟数据，实际应该从服务器获取
    const recentCheckins = [
      {
        id: 1,
        candidateName: '张三',
        examProduct: '多旋翼视距内驾驶员',
        venue: '多旋翼A号实操场',
        checkinTime: '14:30:25',
        status: 'success'
      },
      {
        id: 2,
        candidateName: '李四',
        examProduct: '固定翼视距内驾驶员',
        venue: '固定翼实操区',
        checkinTime: '14:25:10',
        status: 'success'
      }
    ]

    this.setData({
      recentCheckins,
      stats: {
        todayCheckins: recentCheckins.length,
        successRate: 100
      }
    })
  },

  // 查看签到详情
  onCheckinDetail(e) {
    const { checkin } = e.currentTarget.dataset
    wx.showModal({
      title: '签到详情',
      content: `考生：${checkin.candidateName}\n考试：${checkin.examProduct}\n考场：${checkin.venue}\n时间：${checkin.checkinTime}`,
      showCancel: false,
      confirmText: '知道了'
    })
  },

  // 手动输入考生信息签到
  manualCheckin() {
    wx.showModal({
      title: '手动签到',
      content: '请输入考生准考证号',
      editable: true,
      placeholderText: '准考证号',
      success: (res) => {
        if (res.confirm && res.content) {
          // 处理手动签到
          this.processManualCheckin(res.content)
        }
      }
    })
  },

  // 处理手动签到
  processManualCheckin(candidateNumber) {
    wx.showToast({
      title: '功能开发中',
      icon: 'none'
    })
  }
})
