// 考生登录页面
const api = require('../../utils/api.js')

Page({
  data: {
    form: {
      id_card: '',
      phone: ''
    },
    loading: false,
    showPassword: false
  },

  onLoad() {
    // 检查是否已经登录
    const candidateInfo = wx.getStorageSync('candidateInfo')
    if (candidateInfo) {
      wx.switchTab({
        url: '/pages/profile/profile'
      })
    }
  },

  // 输入身份证号
  onIdCardInput(e) {
    this.setData({
      'form.id_card': e.detail.value
    })
  },

  // 输入手机号
  onPhoneInput(e) {
    this.setData({
      'form.phone': e.detail.value
    })
  },

  // 登录
  async onLogin() {
    if (this.data.loading) return

    const { id_card, phone } = this.data.form

    // 表单验证
    if (!id_card) {
      wx.showToast({
        title: '请输入身份证号',
        icon: 'none'
      })
      return
    }

    if (!phone) {
      wx.showToast({
        title: '请输入手机号',
        icon: 'none'
      })
      return
    }

    // 验证身份证号格式
    if (!this.validateIdCard(id_card)) {
      wx.showToast({
        title: '身份证号格式不正确',
        icon: 'none'
      })
      return
    }

    // 验证手机号格式
    if (!this.validatePhone(phone)) {
      wx.showToast({
        title: '手机号格式不正确',
        icon: 'none'
      })
      return
    }

    this.setData({ loading: true })

    try {
      const response = await api.candidateLogin({
        id_card,
        phone
      })

      // 保存考生信息
      wx.setStorageSync('candidateInfo', response)
      wx.setStorageSync('userInfo', {
        id: response.id,
        name: response.name,
        type: 'candidate'
      })

      wx.showToast({
        title: '登录成功',
        icon: 'success'
      })

      // 延迟跳转到个人中心
      setTimeout(() => {
        wx.switchTab({
          url: '/pages/profile/profile'
        })
      }, 1500)

    } catch (error) {
      console.error('登录失败:', error)
      wx.showToast({
        title: error.message || '登录失败，请检查信息',
        icon: 'none',
        duration: 2000
      })
    } finally {
      this.setData({ loading: false })
    }
  },

  // 使用演示账号登录
  onDemoLogin() {
    this.setData({
      'form.id_card': '110101199001011234',
      'form.phone': '13800138001'
    })
    
    wx.showToast({
      title: '已填入演示账号',
      icon: 'success'
    })
  },

  // 清空表单
  onClearForm() {
    this.setData({
      form: {
        id_card: '',
        phone: ''
      }
    })
  },

  // 返回首页
  onBackToHome() {
    wx.switchTab({
      url: '/pages/index/index'
    })
  },

  // 验证身份证号
  validateIdCard(idCard) {
    const reg = /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/
    return reg.test(idCard)
  },

  // 验证手机号
  validatePhone(phone) {
    const reg = /^1[3-9]\d{9}$/
    return reg.test(phone)
  },

  // 获取帮助
  onGetHelp() {
    wx.showModal({
      title: '登录帮助',
      content: '请使用报名时填写的身份证号和手机号进行登录。\n\n如果遇到问题，请联系考务人员或拨打客服电话：400-123-4567',
      showCancel: false
    })
  },

  // 联系客服
  onContactService() {
    wx.makePhoneCall({
      phoneNumber: '400-123-4567'
    })
  }
})