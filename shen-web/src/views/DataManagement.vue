<template>
  <el-row :gutter="15">
      <el-col :span="24">
       <div class="navOptionsItem">
        <ul>
          <li v-for="item in navOptions" @click="showPage(item.value)"><a href="javascript:;" :class="{ active:item.value===navOptionsCurrent }" v-html="item.name"></a></li>
        </ul>
      </div>
      </el-col>
      <div v-if="navOptionsCurrent==1" class="mainshow"><img src="../assets/img/DataManagement1.png"></div>
      <div v-if="navOptionsCurrent==2" class="mainshow"><img src="../assets/img/DataManagement2.png"></div>
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
            {name:"趋势分析",value:1},
            {name:"数据录入",value:2}
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
