<template>
  <el-row :gutter="15">
    <el-col :span="24">
      <TabControl :TabControl="TabControl"></TabControl>
      <el-row :gutter="15" v-if="TabControl.TabControlCurrent === '能耗分析'">
        <el-col :span="24">
          <el-form :inline="true" class="blackComponents">
            <el-form-item label="选择时间：">
              <el-date-picker type="date" v-model="formParameters.energyDate" :picker-options="pickerOptions" size="mini" format="yyyy-MM-dd" style="width: 130px;" :clearable="false" @change=""></el-date-picker>
            </el-form-item>
          </el-form>
          <div class="platformContainer">
            <ve-line :data="chartData" :extend="ChartExtend" height="350px"></ve-line>
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
                <ve-histogram :data="chartFacilityData" :extend="FacilityExtend" height="300px"></ve-histogram>
              </div>
            </el-col>
          </el-row>
        </el-col>
      </el-row>
      <el-row :gutter="15" v-if="TabControl.TabControlCurrent === '设备效率分析'">
        <el-col :span="5">
          <div class="platformContainer blackComponents" style="min-height: 560px;">
            <el-tree
              :data="TreeFacilityData"
              show-checkbox
              :default-expand-all="true"
            >
            </el-tree>
          </div>
        </el-col>
        <el-col :span="19">
          <div class="platformContainer">
            <p class="marginBottom">设备运行图</p>
            <el-row :gutter="15">
              <el-col :span="6">
                <div class="cardContainer">
                  <p class="color-lightgreen marginBottom">开机</p>
                  <p class="marginBottom color-grayblack text-size-12"><span>次数</span><span class="floatRight">时间占比</span></p>
                  <p class="color-lightgreen"><span>3</span><span class="floatRight">72.4%</span></p>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="cardContainer">
                  <p class="color-lightgreen marginBottom">关机</p>
                  <p class="marginBottom color-grayblack text-size-12"><span>次数</span><span class="floatRight">时间占比</span></p>
                  <p class="color-lightgreen"><span>3</span><span class="floatRight">12.5%</span></p>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="cardContainer">
                  <p class="color-lightgreen marginBottom">空载</p>
                  <p class="marginBottom color-grayblack text-size-12"><span>次数</span><span class="floatRight">时间占比</span></p>
                  <p class="color-lightgreen"><span>3</span><span class="floatRight">2.4%</span></p>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="cardContainer">
                  <p class="color-lightgreen marginBottom">功率</p>
                  <p class="marginBottom color-grayblack text-size-12"><span>额定功率</span><span class="floatRight">平均功率</span></p>
                  <p class="color-lightgreen"><span>45.546</span><span class="floatRight">54.45</span></p>
                </div>
              </el-col>
              <el-col :span="24" class="marginTop">
                <div class="platformContainer">
                  <ve-line :data="chartRunEfficiencyData" :extend="RunEfficiencyExtend" height="300px"></ve-line>
                </div>
              </el-col>
            </el-row>
          </div>
        </el-col>
      </el-row>
      <el-row :gutter="15" v-if="TabControl.TabControlCurrent === '制冷量分析'">
        <el-col :span="24">
          <el-form :inline="true" class="blackComponents">
            <el-form-item label="选择时间：">
              <el-date-picker type="date" v-model="formParameters.refrigerationDate" :picker-options="pickerOptions" size="mini" format="yyyy-MM-dd" style="width: 130px;" :clearable="false" @change=""></el-date-picker>
            </el-form-item>
          </el-form>
          <div class="platformContainer">
            <ve-line :data="chartRefrigerationData" :extend="refrigerationExtend" height="350px"></ve-line>
          </div>
          <el-row :gutter="15">
            <el-col :span="5">
              <div class="platformContainer">
                <p class="color-offwhite text-size-16 marginBottom">今日制冷总量</p>
                <p class="color-lightgreen text-size-20 marginBottom">234234kwh</p>
                <p class="color-offwhite text-size-16 marginBottom">选择日制冷总量</p>
                <p class="color-lightgreen text-size-20 marginBottom">234234kwh</p>
                <p class="color-offwhite text-size-16 marginBottom">选择日（截止14：10）</p>
                <p class="color-darkblue text-size-18 marginBottom">234234kwh</p>
                <p class="color-offwhite text-size-16 marginBottom">对比</p>
                <p class="text-size-16 marginBottom">+1.12%</p>
              </div>
            </el-col>
            <el-col :span="5">
              <div class="platformContainer">
                <p class="color-offwhite text-size-16 marginBottom">今日热负载总量</p>
                <p class="color-lightgreen text-size-20 marginBottom">234234</p>
                <p class="color-offwhite text-size-16 marginBottom">选择日热负载总量</p>
                <p class="color-lightgreen text-size-20 marginBottom">234234</p>
                <p class="color-offwhite text-size-16 marginBottom">选择日（截止14：10）</p>
                <p class="color-darkblue text-size-18 marginBottom">234234</p>
                <p class="color-offwhite text-size-16 marginBottom">对比</p>
                <p class="text-size-16 marginBottom">+1.12%</p>
              </div>
            </el-col>
            <el-col :span="14">
              <div class="platformContainer">
                 <ve-histogram :data="chartRefrigerationStatisticsData" :extend="RefrigerationStatisticsExtend" height="300px"></ve-histogram>
              </div>
            </el-col>
          </el-row>
        </el-col>
      </el-row>
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
          energyDate:moment(),
          refrigerationDate:moment(),
        },
        pickerOptions:{
          disabledDate(time) {
            return time.getTime() > moment();
          }
        },
        //能耗分析 时段能耗趋势图表
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
        //能耗分析 能耗统计图表
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
        chartFacilityData:{
          columns:["电表","今日","对比日"],
          rows:[
            {"电表":"冷水机组1","今日":254,"对比日":299},
            {"电表":"冷水机组2","今日":345,"对比日":455},
            {"电表":"总和","今日":574,"对比日":666},
          ]
        },
        //树形图数据
        TreeFacilityData:[
          {label:"冷水机组1",children:[{label:"冷水机组1-1"},{label:"冷水机组1-2"}]},
          {label:"冷水机组2",children:[{label:"冷水机组2-1"},{label:"冷水机组2-1"}]},
        ],
        //运行效率分析图表
        RunEfficiencyExtend: {
          title:{
            text:"时段功率趋势",
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
        chartRunEfficiencyData: {
          columns: ["时间", "功率"],
          rows:[
            {"时间":"00:00","功率":254},
            {"时间":"01:00","功率":345},
            {"时间":"02:00","功率":574},
          ]
        },
        //制冷分析图表
        refrigerationExtend: {
          title:{
            text:"制冷分析趋势",
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
        chartRefrigerationData:{
          columns: ["时间", "制冷量","热负载"],
          rows:[
            {"时间":"00:00","制冷量":254,"热负载":546},
            {"时间":"01:00","制冷量":345,"热负载":863},
            {"时间":"02:00","制冷量":574,"热负载":314},
            {"时间":"03:00","制冷量":674,"热负载":414},
          ]
        },
        // 制冷统计图表
        RefrigerationStatisticsExtend: {
          title:{
            text:"制冷统计分析",
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
        chartRefrigerationStatisticsData:{
          columns: ["统计", "今日","对比日"],
          rows:[
            {"统计":"制冷量","今日":254,"对比日":546},
            {"统计":"热负载","今日":345,"对比日":863},
          ]
        }
      }
    },
    created(){
      this.getEnergyAnalysisCharts()
    },
    mounted(){

    },
    watch:{

    },
    computed:{

    },
    methods: {
      getEnergyAnalysisCharts(){
        var that = this
        var params = {
          CompareTime:moment(this.formParameters.energyDate).format("YYYY-MM-DD")
        }
        this.axios.get("/api/energyanalysis",{
          params: params
        }).then(res =>{
          var data = JSON.parse(res.data)
          console.log(data)
        },res =>{
          console.log("请求错误")
        })
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
