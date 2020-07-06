<template>
<div>
  <el-row :gutter="15">
      <el-col :span="24">
        <TabControl :TabControl="TabControl"></TabControl>
        <el-col :span="24" style="background: #34383E;overflow: hidden;" v-if="TabControl.TabControlCurrent === '大系统'">
          <div class="MainContain BorderRadius4 SysMonbg" @mousedown="move" data-move>
            <div class="hf-6 box1 color-boxbgc">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 box2 color-boxbgc">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 box3 color-boxbgc">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 box4 color-boxbgc">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 box5 color-boxbgc">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 box6 color-mainbgc">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 box7 color-mainbgc">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 box8 color-mainbgc">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 box9 color-mainbgc">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 box10 color-mainbgc">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 box11 color-mainbgc">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 box12 color-mainbgc">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 box13 color-mainbgc">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 box14 color-mainbgc">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 box15 color-mainbgc">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 box16 color-boxbgc">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 box17 color-boxbgc">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 box18 color-boxbgc">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 box19 color-boxbgc">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="hf-6 box191 color-boxbgc">
                <div class='smalllbox color-white'>28.6</div>
                <div class='smalllbox color-lightgreen'>66.2%</div>
            </div>
            <div class="box20 BorderRadius4 color-lightbluebgc sfs">湿风室</div>
            <div class="box21 BorderRadius4 color-lightbluebgc sfs">湿风室</div>
            <div class="box22  text-box color-mainbgc">新风亭</div>
            <div class="box23  text-box color-mainbgc ">排风亭</div>
            <div class="box24  text-box color-mainbgc">新风亭</div>
            <div class="box25  text-box color-mainbgc ">排风亭</div>
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
        this.websock = new WebSocket('ws://127.0.0.1:5002');
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
        console.log(e.data)
        var resdata = JSON.parse(e.data);

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
  .box1{
    top:55px;
    left: 53px;
  }
  .box2{
    left:162px;
    top:96px;
  }
  .box3{
    left: 429px;
    top:149px;
  }
  .box4{
    left:339px;
    top:287px;
  }
  .box5{
    left:343px;
    top:586px;
  }
  .box6{
    left: 573px;
    top: 94px;
  }
  .box7{
    left: 802px;
    top: 94px;
  }
  .box8{
    left: 799px;
    top: 249px;
  }
  .box9{
    left: 685px;
    top: 191px;
  }
  .box10{
    left: 573px;
    top: 249px;
  }
  .box11{
    left: 573px;
    top: 572px;
  }
  .box12{
    left: 802px;
    top: 572px;
  }
  .box13{
    left: 685px;
    top: 630px;
  }
  .box14{
    left: 573px;
    top: 771px;
  }
  .box15{
    left: 799px;
    top: 771px;
  }
  .box16{
    left: 946px;
    top: 149px;
  }
  .box17{
    left: 1038px;
    top: 586px;
  }
  .box18{
    left: 1214px;
    top: 96px;
  }
  .box19{
    left: 1038px;
    top: 287px;
  }
  .box20{
    top:95px;
    left:260px;
  }
  .box191{
    top:56px;
    left:1323px;
  }
  .box21{
    top:95px;
    left:1142px;
  }
  .box22{
    top:118px;
    left:53px;
  }
  .box23{
    top:581px;
    left:53px;
  }
  .box24{
    top:118px;
    left:1322px;
  }
  .box25{
    top:581px;
    left:1322px;
  }

</style>
