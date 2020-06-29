import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import Home from '@/views/home'
import SystemMonitor from '@/views/SystemMonitor'
import IntelligentAnalysis from '@/views/IntelligentAnalysis'
import IntelligentOperation from '@/views/IntelligentOperation'
import IntelligentMaintenance from '@/views/IntelligentMaintenance'
import ParameterConfiguration from '@/views/ParameterConfiguration'
import DataManagement from '@/views/DataManagement'
import ServiceDiagnosis from '@/views/ServiceDiagnosis'
import IntelligentModel from '@/views/IntelligentModel'
import config from '@/components/config'

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
      ]},
    {
      path: '/config',
      name: 'config',
      component: config,
    },
  ]
})
