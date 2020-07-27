// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import axios from 'axios'
import qs from 'qs'
Vue.use(ElementUI)
import 'element-ui/lib/theme-chalk/index.css'
import './assets/common.css'
import 'font-awesome/css/font-awesome.min.css'
import VCharts from 'v-charts'
import store from './store'
import $ from 'jquery'
import './icons'

import JsonExcel from 'vue-json-excel';
Vue.component('downloadExcel',JsonExcel);

Vue.config.productionTip = false
Vue.prototype.axios = axios
Vue.prototype.qs = qs
Vue.use(VCharts)
import has from './assets/js/btnPermissions.js';

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
