import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import config from '@/components/config'
import Login from '@/components/login'
import Home from '@/views/home'
import SystemMonitor from '@/views/energy/SystemMonitor'
import IntelligentAnalysis from '@/views/energy/IntelligentAnalysis'
import IntelligentOperation from '@/views/energy/IntelligentOperation'
import IntelligentMaintenance from '@/views/energy/IntelligentMaintenance'
import ParameterConfiguration from '@/views/energy/ParameterConfiguration'
import DataManagement from '@/views/energy/DataManagement'
import ServiceDiagnosis from '@/views/energy/ServiceDiagnosis'
import IntelligentModel from '@/views/energy/IntelligentModel'
import Organization from '@/views/system/Organization'
import Role from '@/views/system/Role'
import Personnel from '@/views/system/Personnel'
import Calendar from '@/views/system/Calendar'
import Log from '@/views/system/Log'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index,
      redirect:'/SystemMonitor', //index主页默认加载home页面
      children:[
        {path:'/home',name:'home',meta:{ title:'工作台'},component:Home},
        {path:'/SystemMonitor',name:'SystemMonitor',meta:{ title:'工作台'},component:SystemMonitor},
        {path:'/IntelligentAnalysis',name:'IntelligentAnalysis',meta:{ title:'工作台'},component:IntelligentAnalysis},
        {path:'/IntelligentOperation',name:'IntelligentOperation',meta:{ title:'工作台'},component:IntelligentOperation},
        {path:'/IntelligentMaintenance',name:'IntelligentMaintenance',meta:{ title:'工作台'},component:IntelligentMaintenance},
        {path:'/ParameterConfiguration',name:'ParameterConfiguration',meta:{ title:'工作台'},component:ParameterConfiguration},
        {path:'/DataManagement',name:'DataManagement',meta:{ title:'工作台'},component:DataManagement},
        {path:'/ServiceDiagnosis',name:'ServiceDiagnosis',meta:{ title:'工作台'},component:ServiceDiagnosis},
        {path:'/IntelligentModel',name:'IntelligentModel',meta:{ title:'工作台'},component:IntelligentModel},
        {path:'/Organization',name:'Organization',meta:{ title:'组织架构'},component:Organization},
        {path:'/Role',name:'Role',meta:{ title:'角色管理'},component:Role},
        {path:'/Personnel',name:'Personnel',meta:{ title:'人员管理'},component:Personnel},
        {path:'/Calendar',name:'Calendar',meta:{ title:'工作日历'},component:Calendar},
        {path:'/Log',name:'Log',meta:{ title:'系统日志'},component:Log},
      ]
    },{
      path: '/login',
      name: 'login',
      meta:{ title:'登录'},
      component: Login,
    },,{
      path: '/config',
      name: 'config',
      component: config,
    },
  ]
})
