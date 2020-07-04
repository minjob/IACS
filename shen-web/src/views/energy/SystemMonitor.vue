<template>
<div>
  <el-row :gutter="15">
      <el-col :span="24">
         <TabControl :TabControl="TabControl"></TabControl>
         <div class="platformContainer" v-if="TabControl.TabControlCurrent === '冷水机组加减载'">
              <span class="color-lightgreen">大系统</span>
            </div>
            <div class="platformContainer" v-if="TabControl.TabControlCurrent === '深度学习模型'">
              <span class="color-lightgreen">小系统</span>
            </div>
            <div class="platformContainer" v-if="TabControl.TabControlCurrent === '制冷量模型'">
              <span class="color-lightgreen">冷却系统</span>
            </div>
            </el-col>
      <el-col :span="24">
        <div class="color-mainbgc ">
           <el-button v-for="item in modelOption" @click="selectModel(item.value)"  :key='item.value' :class="{'el-button--primary':item.value===modelOptionCurrent}">{{item.name}}</el-button>
       </div>
      </el-col>
      <el-col :span="24" style="overflow:auto">
        <div class="MainContain BorderRadius4 SysMonbg">
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
        navOptionsCurrent:1,
        modelOptionCurrent:1,
        navOptions:[
          {name:"大系统",value:1},
          {name:"小系统",value:2},
          {name:"冷却系统",value:3}
        ],
        modelOption:[{name:'正常',value:1},{name:'节能模式1',value:2},{name:'节能模式2',value:3},{name:'运行参数',value:4}]
      }
    },
    created(){

    },
    watch:{

    },
    computed:{ //计算属性

    },
    methods: {
      showPage(index) {
        this.navOptionsCurrent = index
      },
      selectModel(index){
        this.modelOptionCurrent=index
      }
    }
  }
</script>
<style>
 .second-header{
    background-color: skyblue;
    height: 57px;
    width:100%;
    background:rgba(52,56,62,1);
    border-radius:4px;
  }
.home-container{
  background-color: #1B1E27;
}
.mainshow{
    width: 100%;
    height: 100%;
}
.mainshow img{
    width: 100%;
    height: 100%;
}
.el-row {
  margin-bottom: 10px;
}
.el-row:last-child {
  margin-bottom: 0;
}
.navOptionsItem{
  margin-bottom: 20px;
}
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
