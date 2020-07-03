<template>
  <el-container class="body-container">
    <!-- 侧边栏 -->
    <el-aside width="180px" class="left-aside">
      <el-row>
        <el-col :span="24">
          <div class="aside-head">
            <router-link :to="{name:'home'}" class="fa fa-home" style="font-size: 24px;"></router-link>
          </div>
          <div :style="selfHeight" class="aside-menu">
            <el-menu class="menu-ul" :default-active="defaultActiveUrl" :collapse="isCollapse" :router="true">
              <template v-for="item in subMenulist">
                <el-menu-item v-if="!item.children" :index="item.url"><i :class="item.icon"></i><span slot="title">{{ item.name }}</span></el-menu-item>
                <el-submenu v-if="!item.url" :index="item.name">
                  <template slot="title"><i :class="item.icon"></i><span>{{ item.name }}</span></template>
                  <el-menu-item v-for="(child,childIndex) in item.children" :key="childIndex" :index="child.url" @click="clickSubMenu(child.name)"><span style="margin-left:10px;">{{child.name}}</span></el-menu-item>
                </el-submenu>
              </template>
            </el-menu>
          </div>
          <div class="aside-foot">
            <el-button :icon="sideIcon" size="mini" circle @click="iconToggle"></el-button>
          </div>
        </el-col>
      </el-row>
    </el-aside>
    <!-- 右侧部分 -->
    <el-container>
      <!-- 头部 -->
      <el-header>
        <div class="head-menu floatLeft">
          <ul>
            <li><div class='item-title'>深圳桃源地铁站能耗智能分析控制系统</div></li>
            <li class="mainMenuList" v-for="(item,index) in mainMenuList" :key="index" @click="clickMainMenu(index)" v-bind:class="{active:index==isactive}">{{ item.text }}</li>
          </ul>
        </div>
        <div class="head-menu floatRight">
          <ul>
            <li>
              <el-tooltip class="head-menu-item" effect="dark" content="全屏" placement="bottom">
                <i :class="isFullScreen?'el-icon-aim':'el-icon-full-screen'" @click="getFullCreeen"></i>
              </el-tooltip>
            </li>
            <li>
              <el-dropdown trigger="click" @command="handleCommand" style="cursor: pointer;color: #fff;">
                <span class="text-size-16">
                  <i class="el-icon-user-solid el-icon--left"></i>{{ this.$store.state.UserName }}<i class="el-icon-arrow-down el-icon--right"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item command="a">个人信息</el-dropdown-item>
                  <el-dropdown-item command="b" style="text-align: center"><i class="fa fa-power-off"></i></el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </li>
          </ul>
        </div>
      </el-header>
      <!-- 页面主体 -->
      <el-main style="clear: both;">
        <transition name="move" mode="out-in">
         <!--渲染子页面-->
          <router-view :key="$route.fullPath"></router-view>
       </transition>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
var moment = require('moment');
import screenfull from "screenfull"
export default {
  name: 'Index',
  data () {
    return {
      selfHeight:{ //自适应高度
        height:''
      },
      isCollapse: false, //左侧菜单栏是否缩进了
      sideIcon:'el-icon-arrow-left', //左侧菜单栏缩进点击切换图标
      isClickElseMenu:false,
      AreaArr:[],
      time:"",  //实时显示当前的时间
      dialogUserVisible:false, //是否弹出个人信息
      isactive:"0", //主菜单选中索引值
      defaultActiveUrl:"",
      mainMenuList:[ //主菜单导航列表
        {text:"能源管理"},
        {text:"系统管理"}
      ],
      subMenulist:[], //子菜单导航列表
      energyMenulist:[
        {name: "系统监控", icon: "el-icon-zoom-in",url:"/SystemMonitor"},
        {name: "智能分析", icon: "el-icon-data-analysis", url: "/IntelligentAnalysis"},
        {name: "智能运行", icon: "el-icon-document", url: "/IntelligentOperation"},
        {name: "智能维保", icon: "el-icon-set-up", url: "/IntelligentMaintenance"},
        {name: "参数配置", icon: "el-icon-s-operation", url: "/ParameterConfiguration"},
        {name: "数据管理", icon: "el-icon-data-analysis", url: "DataManagement"},
        {name: "服务诊断", icon: "el-icon-service", url: "/ServiceDiagnosis"},
        {name: "智能模型", icon: "el-icon-suitcase-1", url: "/IntelligentModel"},

      ],
      systemMenulist:[
        {name:"组织架构",icon:"el-icon-office-building",url:"/Organization"},
        {name:"角色管理",icon:"el-icon-s-check",url:"/Role"},
        {name:"人员管理",icon:"el-icon-user",url:"/Personnel"},
        {name:"工作日历",icon:"el-icon-date",url:"/Calendar"},
        {name:"系统日志",icon:"el-icon-notebook-1",url:"/Log"}
      ],
      isFullScreen:false, //是否全屏
      areaObj:{
        areaName:""
      },
    }
  },
  //依赖注入传值
  provide(){
    return{
      newAreaName:this.areaObj
    }
  },
  mounted(){
    if(this.$route.meta.title === "系统管理"){  //判断是否是属于系统管理模块，展示系统模块菜单
      this.isactive = 1
    }
    this.clickMainMenu(this.isactive)
    this.defaultActiveUrl = this.$route.path //将菜单激活项设置为当前页面地址
  },
  created(){
    window.addEventListener('resize', this.getMenuHeight);
    this.getMenuHeight()
    if(sessionStorage.getItem("LoginStatus")) {
      this.$store.commit('setUser',sessionStorage.getItem('WorkNumber'))
      this.axios.get("/api/CUID",{
        params: {
          tableName: "User",
          field:"WorkNumber",
          fieldvalue:sessionStorage.getItem('WorkNumber'),
          limit:1,
          offset:0
        }
      }).then(res =>{
        var data = JSON.parse(res.data)
        this.UserInfo =  data.rows[0]
      })
    }else{
      this.$router.push("/login");
    }
  },
  destroyed() {

  },
  methods:{
    getMenuHeight(){
      this.selfHeight.height = window.innerHeight - 230+'px';
    },
    clickSubMenu(areaName){  //点击左菜单传区域给子组件
      this.areaObj.areaName = areaName
    },
    handleCommand(command) {  //判断用户下拉点击
      if(command == "a"){
        this.dialogUserVisible = true
      }else if(command == "b"){
        this.$store.commit('removeUser')
        this.$router.replace("/login")
      }
    },
    iconToggle() {  //折叠菜单
      this.isCollapse = !this.isCollapse
      if(this.isCollapse){
        this.sideIcon = 'el-icon-arrow-right'
        $(".left-aside").animate({"width":"64px"})
      }else{
        this.sideIcon = 'el-icon-arrow-left'
        $(".left-aside").animate({"width":"180px"})
      }
    },
    clickMainMenu(index){  //切换模块
      this.isactive = index
      if(index == 0) {
        this.subMenulist = this.energyMenulist
        if(this.isClickElseMenu){
          this.defaultActiveUrl = this.subMenulist[0].children[0].url
        }
      }else if(index == 1){
        this.subMenulist = this.systemMenulist
        this.defaultActiveUrl = this.subMenulist[0].url
      }
    },
    getFullCreeen () {  //全屏
      if (screenfull.isEnabled) {
        screenfull.toggle()
        if(screenfull.isFullscreen){
          this.isFullScreen = false
        }else{
          this.isFullScreen = true
        }
      }
    },
  }
}
</script>
<style>
  .el-container,.el-aside,.el-aside .el-row,.el-aside .el-row .el-col{
    position: relative;
    height: 100%;
  }
  .el-header{
    overflow: hidden;
  }
  .body-container{
    background: #1B1E27;
  }
  .left-aside{
    background: #1B1E27;
    box-shadow:1px 0px 5px 3px rgba(255,255,255,0.5);
  }
  .aside-head{
    width: 100%;
    text-align: center;
    padding: 50px 0 30px;
  }
  .aside-head a{
    color: #fff;
  }
  .aside-foot{
    height:110px;
    width: 100%;
    text-align: center;
    font-size: 18px;
    padding-top: 20px;
  }
  .aside-menu{
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .menu-ul{
    border: none;
    clear: both;
    overflow: auto;
    scrollbar-width: none;
    -ms-overflow-style: none;
  }
  .menu-ul::-webkit-scrollbar {
    display: none;
  }
  .el-menu-item .fa {
    margin-right: 5px;
    width: 24px;
    text-align: center;
    font-size: 18px;
    vertical-align: middle;
  }
  .version-number{
    margin-top: 20px;
    color: #737373;
  }
  .head-menu{
    height: 60px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .head-menu i{
    font-size: 24px;
    color: #fff;
    cursor:pointer;
  }
  .head-menu li{
    display: inline-block;
    margin-right: 30px;
  }
  .head-menu li i{
    vertical-align: bottom;
  }
  .head-menu li .item-title{
    font-size: 22px;
    color:#fff;
  }
  .head-menu .mainMenuList{
    text-align: center;
    color: #72747A;
    font-size: 16px;
    text-decoration: none;
    cursor: pointer;
  }
  .mainMenuList.active{
    color: #fff;
  }
</style>
