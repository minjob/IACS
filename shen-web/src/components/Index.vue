<template>
  <el-container class="body-container">
    <!-- 侧边栏 -->
    <el-aside width="180px" class="left-aside">
      <el-row>
        <el-col :span="24">
          <div class="aside-head">
            <router-link :to="{name:'SystemMonitor'}" class="fa fa-home" style="font-size: 24px;"></router-link>
          </div>
          <div :style="selfHeight" class="aside-menu">
            <el-menu class="menu-ul" :default-active="defaultActiveUrl" :collapse="isCollapse" :router="true" @select="menuSelect">
              <template v-for="item in subMenulist">
                <el-menu-item v-if="!item.children" :index="item.url"><i :class="item.icon"></i><span slot="title">{{ item.name }}</span></el-menu-item>
                <el-submenu v-if="item.children" :index="item.name">
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
            <li><div class='item-title'>深圳桃园地铁站能耗智能分析控制系统</div></li>
            <li class="mainMenuList" v-for="(item,index) in mainMenuList" :key="index" @click="clickMainMenu(index)" v-bind:class="{active:index==isactive}">{{ item.text }}</li>
          </ul>
        </div>
        <div class="head-menu floatRight">
          <ul>
            <li>
              <el-tooltip class="head-menu-item eq_stu" effect="dark" content="故障提醒" placement="bottom">
                <el-badge>
                  <i class="eq_stuIcon color-red text-size-18 el-icon-bell" @click="getStu_Equ"></i>
                </el-badge>
              </el-tooltip>
              <el-drawer
                :visible.sync="drawerStu_Equ"
                :with-header="false">
                <div style="padding: 15px;">
                  <p class="marginBottom">当前LS1故障信息</p>
                  <p v-for="(item,index) in LS1EqStuInfo" v-if="LS1EqStuInfo.length > 0" class="marginBottomS text-size-14 color-red">{{ item.value }}</p>
                  <p v-if="LS1EqStuInfo.length === 0" class="text-size-14">暂无故障</p>
                  <p class="marginTop marginBottom">当前LS2故障信息</p>
                  <p v-for="(item,index) in LS2EqStuInfo" v-if="LS2EqStuInfo.length > 0" class="marginBottomS text-size-14 color-red">{{ item.value }}</p>
                  <p v-if="LS2EqStuInfo.length === 0" class="text-size-14">暂无故障</p>
                </div>
              </el-drawer>
            </li>
            <li>
              <el-tooltip class="head-menu-item" effect="dark" content="全屏" placement="bottom">
                <i class="color-white text-size-18" :class="isFullScreen?'el-icon-aim':'el-icon-full-screen'" @click="getFullCreeen"></i>
              </el-tooltip>
            </li>
            <li>
              <el-dropdown trigger="click" @command="handleCommand" style="cursor: pointer;color: #fff;">
                <span class="text-size-16">
                  <i class="dotState bg-lightgreen"></i>{{ this.$store.state.UserName }}<i class="el-icon-arrow-down el-icon--right text-size-12"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item command="a">个人信息</el-dropdown-item>
                  <el-dropdown-item command="b" style="text-align: center"><i class="fa fa-power-off"></i></el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
              <el-dialog title="用户信息" :visible.sync="dialogUserVisible" width="50%">
                <el-form>
                  <el-form-item label="用户名：">{{ userInfo.Name }}</el-form-item>
                  <el-form-item label="工号：">{{ userInfo.WorkNumber }}</el-form-item>
                  <el-form-item label="最近登录时间：">{{ userInfo.LastLoginTime }}</el-form-item>
                  <el-form-item label="权限：">{{ userInfo.Permissions }}</el-form-item>
                </el-form>
                <span slot="footer" class="dialog-footer">
                  <el-button @click="dialogUserVisible = false">取 消</el-button>
                </span>
              </el-dialog>
            </li>
          </ul>
        </div>
      </el-header>
      <!-- 页面主体 -->
      <el-main style="clear: both;padding-top: 0;margin-top: 10px;">
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
      dialogUserVisible:false, //是否弹出个人信息
      userInfo:{},
      isactive:"0", //主菜单选中索引值
      defaultActiveUrl:"",
      mainMenuList:[ //主菜单导航列表
        {text:"智能管理"},
        {text:"系统管理"}
      ],
      subMenulist:[], //子菜单导航列表
      energyMenulist:[
        {name: "系统监控", icon: "el-icon-zoom-in",url:"/SystemMonitor"},
        {name: "智能分析", icon: "el-icon-data-analysis", url: "/IntelligentAnalysis"},
        {name: "智能运行", icon: "el-icon-document", url: "/IntelligentOperation"},
        {name: "智能维保", icon: "el-icon-set-up", url: "/IntelligentMaintenance"},
        {name: "数据管理", icon: "el-icon-data-analysis", url: "DataManagement"},
        {name: "服务诊断", icon: "el-icon-service", url: "/ServiceDiagnosis"},
        {name: "智能模型", icon: "el-icon-suitcase-1", url: "/IntelligentModel"},

      ],
      systemMenulist:[
        {name:"组织架构",icon:"el-icon-office-building",url:"/Organization"},
        {name:"角色管理",icon:"el-icon-s-check",url:"/Role"},
        {name:"班组管理",icon:"el-icon-receiving",url:"/TeamGroup"},
        {name:"人员管理",icon:"el-icon-user",url:"/Personnel"},
        {name:"权限维护",icon:"el-icon-lock",url:"/Permission"},
        {name:"系统日志",icon:"el-icon-notebook-1",url:"/Log"}
      ],
      isFullScreen:false, //是否全屏
      websock:null,
      websockVarData:{},
      drawerStu_Equ:false,
      LS1EqStuInfo:[],
      LS2EqStuInfo:[],
      LS1Stu_Equ:[
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_109",value:"一号压缩机不停机报警",stu:0},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_109",value:"二号压缩机不停机报警",stu:1},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_109",value:"吸排气压差过低报警",stu:2},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_109",value:"吸气压力过低报警",stu:3},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_109",value:"排气压力过高报警",stu:4},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_109",value:"一号压缩机低油位报警",stu:5},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_109",value:"二号压缩机低油位报警",stu:6},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_109",value:"出水温度防冻保护报警",stu:7},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_109",value:"一号压缩机不运行报警",stu:8},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_109",value:"二号压缩机不运行报警",stu:9},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_109",value:"电源掉电报警",stu:10},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_109",value:"冷媒水温度传感器故障报警",stu:11},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_109",value:"吸气压力传感器故障报警",stu:12},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_109",value:"排气压力传感器故障报警",stu:13},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_109",value:"电源电压过高报警",stu:14},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_109",value:"电源电压过低报警",stu:15},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_110",value:"冷媒水断流报警",stu:0},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_110",value:"一号压缩机热继电器过载",stu:1},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_110",value:"一号压缩机油温过高",stu:2},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_110",value:"一号压缩机电机过热",stu:3},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_110",value:"一号压缩机电流过载报警",stu:4},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_110",value:"二号压缩机电流过载报警",stu:5},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_110",value:"二号压缩机热继电器过载",stu:6},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_110",value:"二号压缩机油温过高",stu:7},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_110",value:"二号压缩机电机过热",stu:8},
      ],
      LS2Stu_Equ:[
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_112",value:"一号压缩机不停机报警",stu:0},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_112",value:"二号压缩机不停机报警",stu:1},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_112",value:"吸排气压差过低报警",stu:2},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_112",value:"吸气压力过低报警",stu:3},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_112",value:"排气压力过高报警",stu:4},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_112",value:"一号压缩机低油位报警",stu:5},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_112",value:"二号压缩机低油位报警",stu:6},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_112",value:"出水温度防冻保护报警",stu:7},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_112",value:"一号压缩机不运行报警",stu:8},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_112",value:"二号压缩机不运行报警",stu:9},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_112",value:"电源掉电报警",stu:10},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_112",value:"冷媒水温度传感器故障报警",stu:11},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_112",value:"吸气压力传感器故障报警",stu:12},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_112",value:"排气压力传感器故障报警",stu:13},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_112",value:"电源电压过高报警",stu:14},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_112",value:"电源电压过低报警",stu:15},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_113",value:"冷媒水断流报警",stu:0},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_113",value:"一号压缩机热继电器过载",stu:1},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_113",value:"一号压缩机油温过高",stu:2},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_113",value:"一号压缩机电机过热",stu:3},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_113",value:"一号压缩机电流过载报警",stu:4},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_113",value:"二号压缩机电流过载报警",stu:5},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_113",value:"二号压缩机热继电器过载",stu:6},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_113",value:"二号压缩机油温过高",stu:7},
        {tag:"PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_113",value:"二号压缩机电机过热",stu:8},
      ],
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
    }else{
      this.$router.push("/login");
    }
    this.initWebSocket()
  },
  destroyed() {

  },
  watch:{
    LS1EqStuInfo(val,newVal){
      if(newVal.length > 0){
        $(".eq_stu").addClass("blink")
        $(".eq_stuIcon").addClass("color-red").removeClass("color-white")
      }else{
        $(".eq_stu").removeClass("blink")
        $(".eq_stuIcon").addClass("color-white").removeClass("color-red")
      }
    }
  },
  methods:{
    getMenuHeight(){
      this.selfHeight.height = window.innerHeight - 230+'px';
    },
    menuSelect(key,keyPath){  //点击菜单跳转时  添加query参数避免相同路由跳转时报错
      this.$router.push({
        query:moment()
      })
    },
    handleCommand(command) {  //判断用户下拉点击
      if(command == "a"){
        this.dialogUserVisible = true
        this.userInfo.LastLoginTime = sessionStorage.getItem('LastLoginTime')
        this.userInfo.WorkNumber = sessionStorage.getItem('WorkNumber')
        this.userInfo.Name = sessionStorage.getItem('UserName')
        this.userInfo.Permissions = JSON.parse(sessionStorage.getItem('Permissions')).join('，')
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
    initWebSocket(){ //初始化weosocket
      // this.websock = new WebSocket('ws://' + location.host + '/socket');
      this.websock = new WebSocket('ws://127.0.0.1:5002/socket');
      this.websock.onmessage = this.websocketonmessage;
      this.websock.onopen = this.websocketonopen;
      this.websock.onerror = this.websocketonerror;
      this.websock.onclose = this.websocketclose;
    },
    websocketonopen(){ //连接建立之后执行send方法发送数据
      this.websocketsend();
    },
    websocketonerror(){//连接建立失败重连
      console.log("websocket连接失败")
    },
    websocketonmessage(e){ //数据接收
      this.websockVarData = JSON.parse(e.data)
      this.LS1EqStuInfo = []
      this.LS2EqStuInfo = []
      for(var i in this.websockVarData){
        this.LS1Stu_Equ.forEach(item =>{
          if(item.tag === i){
            var value = parseInt(this.websockVarData[i],10).toString(2).split("")
            var stu = value[value.length - 1 - item.stu]
            if(stu === "1"){
              this.LS1EqStuInfo.push({
                value:item.value
              })
            }
          }

        })
        this.LS2Stu_Equ.forEach(item =>{
          if(item.tag === i){
            var value = parseInt(this.websockVarData[i],10).toString(2).split("")
            var stu = value[value.length - 1 - item.stu]
            if(stu === "1"){
              this.LS2EqStuInfo.push({
                value:item.value
              })
            }
          }
        })
      }
    },
    websocketsend(Data){//数据发送
      this.websock.send(Data);
    },
    websocketclose(e){  //关闭
      console.log("websocket关闭")
    },
    closesocket(){
      this.websock.close()
    },
    getStu_Equ(){  //获取设备故障信息
      this.drawerStu_Equ = true
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
  .head-menu li{
    display: inline-block;
    margin-right: 30px;
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
  .blink{
    -webkit-animation: twinkling 1s infinite ease-in-out;
  }
  @-webkit-keyframes twinkling{    /*透明度由0到1*/
    0%{
      opacity:1; /*透明度为0*/
    }
    50%{
      opacity:0; /*透明度为1*/
    }
    100%{
      opacity:1; /*透明度为1*/
    }
   }
</style>
