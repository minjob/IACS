<template>
  <el-row :gutter="15">
      <el-col :span="24">
       <div class="navOptionsItem">
        <ul>
          <li v-for="item in navOptions" @click="showPage(item.value)"><a href="javascript:;" :class="{ active:item.value===navOptionsCurrent }" v-html="item.name"></a></li>
        </ul>
      </div>
      </el-col>
      <div v-if="navOptionsCurrent==1" class="mainshow"><img src="../assets/img/IntelligentModel3.png"></div>
  </el-row>
</template>

<script>
  var moment = require('moment');
  export default {
    name: "Home",
    data(){
      return {
        navOptionsCurrent:1,
        navOptions:[
          {name:"冷水机组加减载",value:1},
          {name:"深度学习模型",value:2},
          {name:"制冷量模型",value:3},
          {name:"冷冻泵自动变频",value:4},
          {name:"冷却塔自动加减载",value:5}
        ],
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
</style>
