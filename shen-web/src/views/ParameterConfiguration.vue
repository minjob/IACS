<template>
  <el-row :gutter="15">
      <el-col :span="24">
       <div class="navOptionsItem">
        <ul>
          <li v-for="item in navOptions" @click="showPage(item.value)"><a href="javascript:;" :class="{ active:item.value===navOptionsCurrent }" v-html="item.name"></a></li>
        </ul>
      </div>
      </el-col>
      <div class="mainshow"><img src="../assets/img/ParameterConfiguration.png"></div>
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
