<template>
  <el-row :gutter="15">
    <el-col :span="24">
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-normol">服务诊断</span>
      </div>
      <el-row :gutter="25">
        <el-col :span="10">
          <p class="color-white text-size-18 marginBottom">websocket 服务</p>
          <div class="platformContainer" style="height: 400px;">
            <div class="scrollable" style="padding-bottom: 36px;">
              <p v-for="(item,index) in newArr" class="marginBottom">
                <i class="dotState bg-lightgreen" v-if="item.tagData.toLowerCase() != 'NONE' || item.tagData.toLowerCase() != 'INIT'"></i>
                <i class="dotState bg-red" v-if="item.tagData.toLowerCase() === 'NONE' || item.tagData.toLowerCase() === 'INIT'"></i>
                {{ item.tag }}
                <span class="floatRight color-lightgreen" v-if="item.tagData.toLowerCase() != 'NONE' || item.tagData.toLowerCase() != 'INIT'">数据正常</span>
                <span class="floatRight color-red" v-if="item.tagData.toLowerCase() === 'NONE' || item.tagData.toLowerCase() === 'INIT'">无数据</span>
              </p>
            </div>
          </div>
        </el-col>
        <el-col :span="7">
          <p class="color-white text-size-18 marginBottom">OPC 服务</p>
          <div class="platformContainer" style="height: 400px;">
            <p>
              <i class="dotState bg-grayblack" v-if="opcState === ''"></i>
              <i class="dotState bg-lightgreen" v-if="opcState === true"></i>
              <i class="dotState bg-red" v-if="opcState === false"></i>
              <span class="color-white">运行状态</span>
              <span class="floatRight color-grayblack" v-if="opcState === ''"></span>
              <span class="floatRight color-lightgreen" v-if="opcState === true">运行正常</span>
              <span class="floatRight color-red" v-if="opcState === false">服务未启动</span>
            </p>
          </div>
        </el-col>
        <el-col :span="7">
          <p class="color-white text-size-18 marginBottom">节能服务</p>
          <div class="platformContainer" style="height: 400px;">
            <p class="marginBottom">
              <i class="dotState bg-grayblack" v-if="jnState === ''"></i>
              <i class="dotState bg-lightgreen" v-if="jnState === true"></i>
              <i class="dotState bg-red" v-if="jnState === false"></i>
              <span class="color-white">运行状态</span>
              <span class="floatRight color-grayblack" v-if="jnState === ''"></span>
              <span class="floatRight color-lightgreen" v-if="jnState === true">运行正常</span>
              <span class="floatRight color-red" v-if="jnState === false">服务未启动</span>
            </p>
            <p>
              <i class="dotState bg-grayblack" v-if="jnValue === ''"></i>
              <i class="dotState bg-lightgreen" v-if="jnValue === '1'"></i>
              <i class="dotState bg-black" v-if="jnValue === '0'"></i>
              <span class="color-white">节能状态</span>
              <span class="floatRight" v-if="jnValue === ''"></span>
              <span class="floatRight color-lightgreen" v-if="jnValue === '1'">开启</span>
              <span class="floatRight color-grayblack" v-if="jnValue === '0'">关闭</span>
            </p>
          </div>
        </el-col>
        <el-col :span="24">
          <transition name="el-zoom-in-top">
            <p id="newArrInfo" v-show="showNewArr" class="color-white text-size-18">
              共检测tag值 {{ newArrNum }}个，其中未获取到数据的tag有{{ newArrErrorNum }}个，您可以 <span class="color-darkblue" style="cursor: pointer;" @click="initWebSocket">重新检测服务</span>
            </p>
          </transition>
        </el-col>
      </el-row>
    </el-col>
  </el-row>
</template>

<script>
  var moment = require('moment');
  export default {
    name: "ServiceDiagnosis",
    data(){
      return {
        socket:null,
        websockVarData:{},
        arr:[],
        newArr:[],
        newArrErrorNum:0,
        newArrNum:0,
        showNewArr:false,
        opcState:'',
        jnState:'',
        jnValue:'',
      }
    },
    created(){
      this.initWebSocket()
    },
    mounted(){

    },
    watch:{

    },
    computed:{

    },
    methods: {
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
        var that = this
        that.arr = []
        that.newArr = []
        that.newArrErrorNum = 0
        that.newArrNum = 0
        that.showNewArr=false
        that.opcState=''
        that.jnState=''
        that.jnValue=''
        for(var key in that.websockVarData){//循环返回的对象，并转成数组格式
          that.arr.push({[key]:that.websockVarData[key]})
        }
        that.arr.forEach((item,index) =>{  //循环数组
          (function(index) {
            setTimeout(function() { //延迟循环，依次导入新的数组，实现延迟加载数据的效果
              for(var skey in item){
                that.newArrNum++
                if(item[skey].toLowerCase() != 'NONE' || item[skey].toLowerCase() != 'INIT'){
                  that.newArr.push({
                    tag:skey,
                    tagData:item[skey]
                  })
                  that.opcState = true
                }else{
                  that.newArr.push({
                    tag:skey,
                    tagData:item[skey]
                  })
                  that.newArrErrorNum++
                }
                if(skey === 'LS_JN_FLAG'){  //判断节能的tag值
                  if(item[skey].toLowerCase() != 'NONE' || item[skey].toLowerCase() != 'INIT'){
                    that.jnState = true
                    that.jnValue = item[skey]
                  }else{
                    that.jnState = false
                  }
                }
                var scrollHeight = $('.scrollable').prop("scrollHeight");
                $(".scrollable").scrollTop(scrollHeight) //将滚动条移动到最底部
              }
              if(index === that.arr.length -1){
                that.showNewArr = true
                if(that.opcState === ''){
                  that.opcState = false
                }
              }
            }, (index + 1) * 100);
          })(index)
        })
        that.websock.close()
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
    }
  }
</script>
<style>

</style>
