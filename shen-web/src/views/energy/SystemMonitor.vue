<template>
<div>
  <el-row :gutter="15">
      <el-col :span="24">
       <div class="navOptionsItem">
        <ul>
          <li v-for="item in navOptions" @click="showPage(item.value)" :key='item.value'><a href="javascript:;" :class="{ active:item.value===navOptionsCurrent }" v-html="item.name"></a></li>
        </ul>
      </div>
      </el-col>   
  </el-row>
  <el-row>
      <el-col :span="24">
        <div class="color-mainbgc ">
           <el-button v-for="item in modelOption" @click="selectModel(item.value)"  :key='item.value' :class="{'el-button--primary':item.value===modelOptionCurrent}">{{item.name}}</el-button>
       </div>
      </el-col>
  </el-row>
<div class="margintop20">
  <el-row>
      <el-col :span="24">
        <div class="color-mainbgc mainContain">
           内容区域
       </div>
      </el-col>
  </el-row>
</div>
</div>
</template>

<script>
  var moment = require('moment');
  export default {
    name: "Home",
    data(){
      return {
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
  margin-bottom: 0px;
}
.el-row:last-child {
  margin-bottom: 0;
}
.navOptionsItem{
  margin-bottom: 2px;
}
</style>
