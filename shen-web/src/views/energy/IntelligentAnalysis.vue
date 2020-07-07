<template>
  <el-row :gutter="15">
    <el-col :span="24">
      <TabControl :TabControl="TabControl"></TabControl>
      <el-row :gutter="15">
        <el-col :span="24" v-if="TabControl.TabControlCurrent === '能耗分析'">
          <el-form :inline="true" class="blackComponents">
            <el-form-item label="选择时间：">
              <el-date-picker type="date" v-model="formParameters.date" :picker-options="pickerOptions" size="mini" format="yyyy-MM-dd" style="width: 130px;" :clearable="false" @change=""></el-date-picker>
            </el-form-item>
          </el-form>
          <div class="platformContainer">
            <ve-line :data="chartData" :extend="ChartExtend" v-loading="ChartsLoading" height="350px"></ve-line>
          </div>
          <el-row :gutter="15">
            <el-col :span="5">
              <div class="platformContainer">
                <p class="color-offwhite text-size-16 marginBottom">今日能耗总量</p>
                <p class="color-lightgreen text-size-20 marginBottom">234234kwh</p>
                <p class="color-offwhite text-size-16 marginBottom">选择日能耗总量（全天）</p>
                <p class="color-darkblue text-size-20 marginBottom">234234kwh</p>
                <p class="color-offwhite text-size-16 marginBottom">选择日（截止14：10）</p>
                <p class="color-darkblue text-size-18 marginBottom">234234kwh</p>
                <p class="color-offwhite text-size-16 marginBottom">对比</p>
                <p class="text-size-16 marginBottom">+1.12%</p>
              </div>
            </el-col>
            <el-col :span="19">
              <div class="platformContainer">
                <ve-histogram :data="chartFacilityData" :extend="FacilityExtend" v-loading="FacilityChartsLoading" height="300px"></ve-histogram>
              </div>
            </el-col>
          </el-row>
        </el-col>
      </el-row>
      <el-row :gutter="15" v-if="TabControl.TabControlCurrent === '设备效率分析'">
        <el-col :span="4">
          <div class="platformContainer blackComponents">
            <el-tree
              :data="TreeFacilityData"
              show-checkbox
              :default-expand-all="true"
            >
            </el-tree>
          </div>
        </el-col>
        <el-col :span="20">
          <div class="platformContainer">

          </div>
        </el-col>
      </el-row>
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
        },
        ChartsLoading:false,
        ChartExtend: {
          title:{
            text:"时段能耗趋势",
            textStyle:{
              color:"#9B9B9B"
            }
          },
          legend: {
            inactiveColor: '#777',
            textStyle: { color: '#fff' }
          },
          xAxis:{
            axisLine: { lineStyle: { color: '#9B9B9B' } },
            //splitLine:{ show: true, lineStyle: { color: ['#F3F3F3']} }
          },
          yAxis:{
            axisLine: { lineStyle: { color: '#9B9B9B' } },
            splitLine:{ show: true, lineStyle: { color: ['#1B1E27']} }
          },
          grid:{
            left:'0px',
            right:'10px',
            bottom:'0',
            top:'60px'
          },
          series:{
            smooth: false
          }
        },
        FacilityChartsLoading:false,
        FacilityExtend: {
          title:{
            text:"能耗统计",
            textStyle:{
              color:"#9B9B9B"
            }
          },
          legend: {
            inactiveColor: '#777',
            textStyle: { color: '#fff' }
          },
          xAxis:{
            axisLine: { lineStyle: { color: '#9B9B9B' } },
          },
          yAxis:{
            axisLine: { lineStyle: { color: '#9B9B9B' } },
            splitLine:{ show: true, lineStyle: { color: ['#1B1E27']} }
          },
          grid:{
            left:'0px',
            right:'10px',
            bottom:'0',
            top:'60px'
          },
          series:{
            barMaxWidth : 30,
            smooth: false
          }
        },
        chartData:{
          columns:["时间","今日能耗","对比日能耗"],
          rows:[
            {"时间":"2020-07-02","今日能耗":254,"对比日能耗":299},
            {"时间":"2020-07-03","今日能耗":345,"对比日能耗":455},
            {"时间":"2020-07-04","今日能耗":574,"对比日能耗":666},
            {"时间":"2020-07-05","今日能耗":451,"对比日能耗":315},
            {"时间":"2020-07-06","今日能耗":"","对比日能耗":315},
          ]
        },
        chartFacilityData:{
          columns:["电表","今日","对比日"],
          rows:[
            {"电表":"冷水机组1","今日":254,"对比日":299},
            {"电表":"冷水机组2","今日":345,"对比日":455},
            {"电表":"总和","今日":574,"对比日":666},
          ]
        },
        TreeFacilityData:[
          {label:"冷水机组1",children:[{label:"冷水机组1-1"},{label:"冷水机组1-2"}]},
          {label:"冷水机组2",children:[{label:"冷水机组2-1"},{label:"冷水机组2-1"}]},
        ]
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
