/**
 * UAV考点运营管理系统 - 微信小程序入口文件
 */
App({
  onLaunch() {
    console.log('UAV考点运营管理系统小程序启动')
    
    // 检查更新
    this.checkForUpdate()
    
    // 获取用户信息
    this.getUserProfile()
    
    // 初始化全局数据
    this.globalData = {
      userInfo: null,
      systemInfo: null,
      apiBaseUrl: 'https://your-api-domain.com/api/v1',
      version: '1.0.0'
    }
  },

  onShow() {
    console.log('小程序显示')
  },

  onHide() {
    console.log('小程序隐藏')
  },

  onError(msg) {
    console.error('小程序错误:', msg)
  },

  // 检查小程序更新
  checkForUpdate() {
    if (wx.canIUse('getUpdateManager')) {
      const updateManager = wx.getUpdateManager()
      
      updateManager.onCheckForUpdate((res) => {
        if (res.hasUpdate) {
          console.log('发现新版本')
        }
      })

      updateManager.onUpdateReady(() => {
        wx.showModal({
          title: '更新提示',
          content: '新版本已经准备好，是否重启应用？',
          success: (res) => {
            if (res.confirm) {
              updateManager.applyUpdate()
            }
          }
        })
      })

      updateManager.onUpdateFailed(() => {
        wx.showModal({
          title: '更新失败',
          content: '新版本下载失败，请检查网络后重试',
          showCancel: false
        })
      })
    }
  },

  // 获取用户基本信息
  getUserProfile() {
    wx.getUserProfile({
      desc: '用于完善用户资料',
      success: (res) => {
        console.log('获取用户信息成功:', res.userInfo)
        this.globalData.userInfo = res.userInfo
      },
      fail: (err) => {
        console.log('获取用户信息失败:', err)
      }
    })

    // 获取系统信息
    wx.getSystemInfo({
      success: (res) => {
        console.log('系统信息:', res)
        this.globalData.systemInfo = res
      }
    })
  },

  // 全局数据
  globalData: {
    userInfo: null,
    systemInfo: null,
    apiBaseUrl: 'https://your-api-domain.com/api/v1',
    version: '1.0.0'
  },

  // 工具方法
  utils: {
    // 显示加载提示
    showLoading(title = '加载中...') {
      wx.showLoading({
        title: title,
        mask: true
      })
    },

    // 隐藏加载提示
    hideLoading() {
      wx.hideLoading()
    },

    // 显示成功提示
    showSuccess(title) {
      wx.showToast({
        title: title,
        icon: 'success',
        duration: 2000
      })
    },

    // 显示错误提示
    showError(title) {
      wx.showToast({
        title: title,
        icon: 'error',
        duration: 3000
      })
    },

    // 显示确认对话框
    showConfirm(options) {
      return new Promise((resolve, reject) => {
        wx.showModal({
          title: options.title || '提示',
          content: options.content || '',
          confirmText: options.confirmText || '确定',
          cancelText: options.cancelText || '取消',
          success: (res) => {
            if (res.confirm) {
              resolve(true)
            } else {
              resolve(false)
            }
          },
          fail: reject
        })
      })
    },

    // 格式化时间
    formatTime(date) {
      const year = date.getFullYear()
      const month = date.getMonth() + 1
      const day = date.getDate()
      const hour = date.getHours()
      const minute = date.getMinutes()

      return `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')} ${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`
    }
  }
})