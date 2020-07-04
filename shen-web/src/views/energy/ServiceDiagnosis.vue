<template>
  <el-row :gutter="15">
    <el-col :span="24">
      <TabControl :TabControl="TabControl"></TabControl>
        <div class="platformContainer" v-if="TabControl.TabControlCurrent === '冷水机组加减载'">
          <span class="color-lightgreen">冷水机组加减载</span>
        </div>
        <div class="platformContainer" v-if="TabControl.TabControlCurrent === '深度学习模型'">
          <span class="color-lightgreen">深度学习模型</span>
        </div>
        <div class="platformContainer" v-if="TabControl.TabControlCurrent === '制冷量模型'">
          <span class="color-lightgreen">制冷量模型</span>
        </div>
    </el-col>
  </el-row>
</template>

<script>
  import TabControl from '@/components/TabControl'
  var moment = require('moment');
  export default {
    name: "ServiceDiagnosis",
    components:{TabControl},
    data(){
      return {
        TabControl:{
          TabControlCurrent:"",
          TabControlOptions:[
            {name:"冷水机组加减载"},
            {name:"深度学习模型"},
            {name:"制冷量模型"},
            {name:"冷冻泵自动变频"},
            {name:"冷却塔自动加减载"}
          ],
        }
      }
    },
    created(){

    },
    mounted(){

    },
    watch:{

    },
    computed:{

    },
    methods: {

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
