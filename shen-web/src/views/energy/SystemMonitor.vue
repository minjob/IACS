<template>
<div>
  <el-row :gutter="15">
      <el-col :span="24">
        <TabControl :TabControl="TabControl"></TabControl>
        <el-col :span="24" style="background: #34383E;overflow: hidden;" v-if="TabControl.TabControlCurrent === '大系统'">
          <div class="MainContain BorderRadius4 SysMonbg" @mousedown="move" data-move>
            <div class="hf-6 color-boxbgc" style="top:55px;left: 53px;">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 color-boxbgc" style="left:162px;top:96px;">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 color-boxbgc" style="left: 429px;top:149px;">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 color-boxbgc" style="left:339px;top:287px;">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 color-boxbgc" style="left:343px;top:586px;">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 573px;top: 94px;">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 802px;top: 94px;">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 799px;top: 249px;">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 685px;top: 191px;">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 573px;top: 249px;">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 573px;top: 572px;">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 802px;top: 572px;">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 685px;top: 630px;">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 573px;top: 771px;">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 799px;top: 771px;">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 color-boxbgc" style="left: 946px;top: 149px;">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 color-boxbgc" style="left: 1038px;top: 586px;">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 color-boxbgc" style="left: 1214px;top: 96px;">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 color-boxbgc" style="left: 1038px;top: 287px;">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 color-boxbgc" style="top:56px;left:1323px;">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="BorderRadius4 color-lightbluebgc sfs" style="top:95px;left:260px;">湿风室</div>
            <div class="BorderRadius4 color-lightbluebgc sfs" style="top:95px;left:1142px;">湿风室</div>
            <div class="text-box color-mainbgc" style="top:118px;left:53px;">新风亭</div>
            <div class="text-box color-mainbgc" style="top:581px;left:53px;">排风亭</div>
            <div class="text-box color-mainbgc" style="top:118px;left:1322px;">新风亭</div>
            <div class="text-box color-mainbgc" style="top:581px;left:1322px;">排风亭</div>
         </div>
        </el-col>
        <div class="platformContainer" v-if="TabControl.TabControlCurrent === '深度学习模型'">
          <span class="color-lightgreen">小系统</span>
        </div>
        <div class="platformContainer" v-if="TabControl.TabControlCurrent === '制冷量模型'">
          <span class="color-lightgreen">冷却系统</span>
        </div>
      </el-col>
  </el-row>
</div>
</template>

<script>
  var moment = require('moment');
  import TabControl from '@/components/TabControl'
  export default {
    name: "SystemMonitor",
    components:{TabControl},
    data(){
      return {
        TabControl:{
          TabControlCurrent:"",
          TabControlOptions:[
            {name:"大系统"},
            {name:"小系统"},
            {name:"冷却系统"},
          ],
        },
        websock:null,
      }
    },
    created(){
      this.initWebSocket()
    },
    mounted(){

    },
    watch:{

    },
    computed:{ //计算属性

    },
    destroyed() {
      if(this.websock){
        this.websock.close() //离开路由之后断开websocket连接
      }
    },
    methods: {
      move(e){
        let odiv = e.target; //获取目标元素
        if(odiv.attributes.hasOwnProperty("data-move")){
          //算出鼠标相对元素的位置
          let disX = e.clientX - odiv.offsetLeft;
          let disY = e.clientY - odiv.offsetTop;
          document.onmousemove = (e)=>{ //鼠标按下并移动的事件
            //用鼠标的位置减去鼠标相对元素的位置，得到元素的位置
            let left = e.clientX - disX - 15;
            let top = e.clientY - disY - 75;
            //绑定元素位置到positionX和positionY上面
            this.positionX = top;
            this.positionY = left;
            //移动当前元素
            odiv.style.left = left + 'px';
            odiv.style.top = top + 'px';
          };
          document.onmouseup = (e) => {
            document.onmousemove = null;
            document.onmouseup = null;
          };
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
        var resdata = JSON.parse(e.data);
        console.log(resdata)

      },
      websocketsend(Data){//数据发送
        this.websock.send(Data);
      },
      websocketclose(e){  //关闭
        console.log("websocket关闭")
      },
      closesocket(){
        this.websock.close()
      }
    }
  }
</script>
<style>

</style>
