import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';
Vue.use(Vuex);
export default new Vuex.Store({
  // 创建基本状态
  state: {
    WorkNumber:null,
    UserName:null,
    UserId:null,
    LoginStatus: false
  },
  // 创建改变状态的方法
  mutations: {
    setUser(state,user){
      state.WorkNumber = user;
      state.LoginStatus = true;
      axios.get("/api/CUID",{ //储存用户名
        params: {
          tableName: "User",
          field:"WorkNumber",
          fieldvalue:user,
          limit:1,
          offset:0
        }
      }).then(res =>{
        var data = JSON.parse(res.data)
        state.UserName = data.rows[0].Name
        state.UserId = data.rows[0].id
        sessionStorage.setItem('UserName', data.rows[0].Name)
        sessionStorage.setItem('UserId', data.rows[0].id)
      },res =>{
        console.log("获取用户信息时请求错误")
      })
      sessionStorage.setItem('WorkNumber', user)
      sessionStorage.setItem('LoginStatus', true)
    },
    removeUser(state){
      state.WorkNumber = null
      state.LoginStatus = false;
      sessionStorage.removeItem('WorkNumber')
      sessionStorage.removeItem('LoginStatus')
      sessionStorage.removeItem('UserId')
      sessionStorage.removeItem('UserName')
    }
  },
  actions: {},
  getters:{
    WorkNumber: state => state.WorkNumber,
    LoginStatus: state => state.LoginStatus
  }
});
