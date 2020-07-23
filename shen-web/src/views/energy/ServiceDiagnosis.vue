<template>
  <el-row :gutter="15">
    <el-col :span="24">
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-normol">服务诊断</span>
      </div>
      <el-row :gutter="25">
        <el-col :span="8">
          <p class="color-white text-size-18 marginBottom">websocket 服务</p>
          <div class="platformContainer" style="height: 400px;">
            <div class="scrollable" style="padding-bottom: 36px;">
              <p v-for="(item,index) in newArr" class="marginBottom">
                <i class="dotState bg-lightgreen" v-if="item.tagData != null"></i>
                <i class="dotState bg-red" v-if="item.tagData === null"></i>
                {{ item.tag }}
                <span class="floatRight color-lightgreen" v-if="item.tagData != null">数据正常</span>
                <span class="floatRight color-red" v-if="item.tagData === null">无数据</span>
              </p>
            </div>
          </div>
        </el-col>
        <el-col :span="8">
          <p class="color-white text-size-18 marginBottom">OPC 服务</p>
          <div class="platformContainer" style="height: 400px;">

          </div>
        </el-col>
        <el-col :span="8">
          <p class="color-white text-size-18 marginBottom">节能服务</p>
          <div class="platformContainer" style="height: 400px;">

          </div>
        </el-col>
        <el-col :span="24">
          <transition name="el-zoom-in-top">
            <p id="newArrInfo" v-show="showNewArr" class="color-white text-size-18">共检测tag值 {{ newArrNum }}个,其中未获取到数据的tag有{{ newArrErrorNum }}个</p>
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
        showNewArr:false
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
        for(var key in that.websockVarData){//循环返回的对象，并转成数组格式
          that.arr.push({[key]:that.dd[key]})
        }
        that.arr.forEach((item,index) =>{  //循环数组
          (function(index) {
            setTimeout(function() { //延迟循环，依次导入新的数组，实现延迟加载数据的效果
              for(var skey in item){
                that.newArrNum++
                if(item[skey] != null){
                  that.newArr.push({
                    tag:skey,
                    tagData:item[skey]
                  })
                }else{
                  that.newArr.push({
                    tag:skey,
                    tagData:item[skey]
                  })
                  that.newArrErrorNum++
                }
                var scrollHeight = $('.scrollable').prop("scrollHeight");
                $(".scrollable").scrollTop(scrollHeight) //将滚动条移动到最底部
              }
              if(index === that.arr.length -1){
                that.websock.close() //循环到最后一条数据时，停止websock
                that.showNewArr = true
              }
            }, (index + 1) * 200);
          })(index)
        })
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
