<template>
  <el-row :gutter="15">
    <el-col :span="24">
      <TabControl :TabControl="TabControl"></TabControl>
      <el-col :span="24" style="padding: 0;" v-if="TabControl.TabControlCurrent === '能耗分析'">
        <el-form :inline="true">
          <el-form-item label="选择时间：">
            <el-date-picker type="date" v-model="formParameters.date" :picker-options="pickerOptions" size="mini" format="yyyy-MM-dd" style="width: 130px;" :clearable="false" @change=""></el-date-picker>
          </el-form-item>
        </el-form>
        <div class="platformContainer">

        </div>
      </el-col>
      <div class="platformContainer" v-if="TabControl.TabControlCurrent === '设备效率分析'">
        <span class="color-lightgreen">设备效率分析</span>
      </div>
      <div class="platformContainer" v-if="TabControl.TabControlCurrent === '制冷量分析'">
        <span class="color-lightgreen">制冷量分析</span>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  import TabControl from '@/components/TabControl'
  var moment = require('moment');
  export default {
    name: "IntelligentAnalysis",
    components:{TabControl},
    data(){
      return {
        TabControl:{
          TabControlCurrent:"",
          TabControlOptions:[
            {name:"能耗分析"},
            {name:"设备效率分析"},
            {name:"制冷量分析"}
          ],
        },
        formParameters:{
          date:moment()
        },
        pickerOptions:{
          disabledDate(time) {
            return time.getTime() > moment();
          }
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
