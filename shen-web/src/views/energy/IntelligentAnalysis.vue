<template>
  <el-row :gutter="15">
    <el-col :span="24">
      <TabControl :TabControl="TabControl"></TabControl>
      <el-row :gutter="15" v-if="TabControl.TabControlCurrent === '能耗分析'">
        <el-col :span="24">
          <el-form :inline="true" class="blackComponents">
            <el-form-item label="选择时间：">
              <el-date-picker type="date" v-model="formParameters.energyDate" :picker-options="pickerOptions" size="mini" format="yyyy-MM-dd" style="width: 130px;" :clearable="false" @change="getEnergyAnalysisCharts(),getEnergyData()"></el-date-picker>
            </el-form-item>
          </el-form>
          <div class="platformContainer">
            <ve-line :data="chartData" :extend="ChartExtend" height="350px"></ve-line>
          </div>
          <el-row :gutter="15">
            <el-col :span="5">
              <div class="platformContainer">
                <p class="color-offwhite text-size-14 marginBottom">今日能耗总量</p>
                <p class="color-lightgreen text-size-16 marginBottom">{{ todayEnergy }}kwh</p>
                <p class="color-offwhite text-size-14 marginBottom">选择日能耗总量（全天）</p>
                <p class="color-darkblue text-size-16 marginBottom">{{ compareAllDateEnergy }}kwh</p>
                <p class="color-offwhite text-size-14 marginBottom">选择日截止{{ nowTime }}能耗</p>
                <p class="color-darkblue text-size-16 marginBottom">{{ compareEnergy }}kwh</p>
                <p class="color-offwhite text-size-14 marginBottom">对比</p>
                <p class="text-size-16 marginBottom" :class="todayEnergy-compareEnergy>0?'color-red':'color-success'">{{ energyCompareRatio }}</p>
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
                  <p class="color-lightgreen marginBottom">运行</p>
                  <p class="marginBottom color-grayblack text-size-12"><span>次数</span><span class="floatRight">时间占比</span></p>
                  <p class="color-lightgreen"><span>3</span><span class="floatRight">72.4%</span></p>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="cardContainer">
                  <p class="color-lightgreen marginBottom">停机</p>
                  <p class="marginBottom color-grayblack text-size-12"><span>次数</span><span class="floatRight">时间占比</span></p>
                  <p class="color-lightgreen"><span>3</span><span class="floatRight">12.5%</span></p>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="cardContainer">
                  <p class="color-lightgreen marginBottom">故障</p>
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
              <el-date-picker type="date" v-model="formParameters.refrigerationDate" :picker-options="pickerOptions" size="mini" format="yyyy-MM-dd" style="width: 130px;" :clearable="false" @change="getmakecoolanalysis(),getmakecoolanalysisData()"></el-date-picker>
            </el-form-item>
          </el-form>
          <div class="platformContainer">
            <ve-line :data="chartRefrigerationData" :extend="refrigerationExtend" height="350px"></ve-line>
          </div>
          <el-row :gutter="15">
            <el-col :span="5">
              <div class="platformContainer">
                <p class="color-offwhite text-size-14 marginBottom">今日制冷总量</p>
                <p class="color-lightgreen text-size-16 marginBottom">{{ ZLtodayData }}</p>
                <p class="color-offwhite text-size-14 marginBottom">选择日制冷总量</p>
                <p class="color-lightgreen text-size-16 marginBottom">{{ ZLcompareAllDateData }}</p>
                <p class="color-offwhite text-size-14 marginBottom">选择日截止{{ nowTime }}的制冷量</p>
                <p class="color-darkblue text-size-16 marginBottom">{{ZLcompareData  }}</p>
                <p class="color-offwhite text-size-14 marginBottom">对比</p>
                <p class="text-size-16 marginBottom" :class="ZLtodayData-ZLcompareData>0?'color-red':'color-success'">{{ ZLCompareRatio }}</p>
              </div>
            </el-col>
            <el-col :span="5">
              <div class="platformContainer">
                <p class="color-offwhite text-size-14 marginBottom">今日热负载总量</p>
                <p class="color-lightgreen text-size-16 marginBottom">{{ hottodayData }}</p>
                <p class="color-offwhite text-size-14 marginBottom">选择日热负载总量</p>
                <p class="color-lightgreen text-size-16 marginBottom">{{ hotcompareAllDateData }}</p>
                <p class="color-offwhite text-size-14 marginBottom">选择日截止{{ nowTime }}的热负载</p>
                <p class="color-darkblue text-size-16 marginBottom">{{ hotcompareData }}</p>
                <p class="color-offwhite text-size-14 marginBottom">对比</p>
                <p class="text-size-16 marginBottom" :class="hottodayData-hotcompareData>0?'color-red':'color-success'">{{ hotCompareRatio }}</p>
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
          energyDate:moment().subtract(1,'day').format('YYYY-MM-DD'),
          refrigerationDate:moment().subtract(1,'day').format('YYYY-MM-DD'),
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
          rows:[]
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
          rows:[]
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
          rows:[]
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
          rows:[]
        },
        nowTime:"",
        todayEnergy:"",
        compareEnergy:"",
        compareAllDateEnergy:"",
        ZLtodayData:"",
        ZLcompareData:"",
        ZLcompareAllDateData:"",
        hottodayData:"",
        hotcompareData:"",
        hotcompareAllDateData:""
      }
    },
    created(){
      this.getEnergyAnalysisCharts()
      this.getEnergyData()
      this.getmakecoolanalysis()
      this.getmakecoolanalysisData()
    },
    mounted(){

    },
    watch:{

    },
    computed:{
      energyCompareRatio(){
        if(this.todayEnergy > 0){
          var compare = (this.todayEnergy - this.compareEnergy) / this.todayEnergy * 100
          if(this.todayEnergy - this.compareEnergy > 0){
            return "+" + compare.toFixed(2) + "%"
          }else{
            return compare.toFixed(2) + "%"
          }
        }else{
          if(this.compareEnergy > 0){
            return "-" + 100 + "%"
          }else{
            return 0 + "%"
          }
        }
      },
      ZLCompareRatio(){
        if(this.ZLtodayData > 0){
          var compare = (this.ZLtodayData - this.ZLcompareData) / this.ZLtodayData * 100
          if(this.ZLtodayData - this.ZLcompareData > 0){
            return "+" + compare.toFixed(2) + "%"
          }else{
            return compare.toFixed(2) + "%"
          }
        }else{
          if(this.ZLcompareData > 0){
            return "-" + 100 + "%"
          }else{
            return 0 + "%"
          }
        }
      },
      hotCompareRatio(){
        if(this.hottodayData > 0){
          var compare = (this.hottodayData - this.hotcompareData) / this.hottodayData * 100
          if(this.hottodayData - this.hotcompareData > 0){
            return "+" + compare.toFixed(2) + "%"
          }else{
            return compare.toFixed(2) + "%"
          }
        }else{
          if(this.hotcompareData > 0){
            return "-" + 100 + "%"
          }else{
            return 0 + "%"
          }
        }
      },
    },
    methods: {
      getEnergyAnalysisCharts(){  //获取能耗分析的两个图表
        var that = this
        var params = {
          CompareTime:moment(this.formParameters.energyDate).format("YYYY-MM-DD")
        }
        this.axios.get("/api/energyanalysis",{
          params: params
        }).then(res =>{
          that.chartData.rows = res.data.lineChartRows
          that.chartFacilityData.rows = res.data.histogramChartRows
        },res =>{
          console.log("请求错误")
        })
      },
      getEnergyData(){ //获取今天和选择天的能耗量
        var that = this
        var api = "/api/energyselectbytime"
        var nowTime = moment().format('HH:mm').substring(0,4) + "0"
        var todayStartTime = moment().day(moment().day()).startOf('day').format('YYYY-MM-DD HH:mm')
        var todayEndTime = moment().day(moment().day()).endOf('day').format('YYYY-MM-DD HH:mm')
        var compareDateStartTime = moment(this.formParameters.energyDate).day(moment(this.formParameters.energyDate).day()).startOf('day').format('YYYY-MM-DD HH:mm')
        var compareDateEndTime = moment(this.formParameters.energyDate).format('YYYY-MM-DD ') + nowTime
        var compareDateEndAllTime = moment(this.formParameters.energyDate).day(moment(this.formParameters.energyDate).day()).endOf('day').format('YYYY-MM-DD HH:mm')
        this.nowTime = nowTime
        this.axios.all([
          this.axios.get(api,{params: {begin: todayStartTime,end:todayEndTime}}),//获取今天能耗
          this.axios.get(api,{params: {begin: compareDateStartTime,end:compareDateEndTime}}),//获取对比天截止当前时间能耗
          this.axios.get(api,{params: {begin: compareDateStartTime,end:compareDateEndAllTime}}),//获取对比整天能耗
        ]).then(this.axios.spread((todayData,CompareData,CompareAllData) =>{
          that.todayEnergy = todayData.data
          that.compareEnergy = CompareData.data
          that.compareAllDateEnergy = CompareAllData.data
        }))
      },
      getmakecoolanalysis(){ //获取制冷量分析两个图表
        var that = this
        var params = {
          CompareTime:moment(this.formParameters.refrigerationDate).format("YYYY-MM-DD")
        }
        this.axios.get("/api/makecoolanalysis",{
          params: params
        }).then(res =>{
          console.log(res.data)
          that.chartRefrigerationData.rows = res.data.lineChartRows
          that.chartRefrigerationStatisticsData.rows = res.data.histogramChartRows
        },res =>{
          console.log("请求错误")
        })
      },
      getmakecoolanalysisData(){ //获取今天和选择天的能耗量
        var that = this
        var api = "/api/makecoolselectbytime"
        var nowTime = moment().format('HH:mm').substring(0,4) + "0"
        var todayStartTime = moment().day(moment().day()).startOf('day').format('YYYY-MM-DD HH:mm')
        var todayEndTime = moment().day(moment().day()).endOf('day').format('YYYY-MM-DD HH:mm')
        var compareDateStartTime = moment(this.formParameters.refrigerationDate).day(moment(this.formParameters.refrigerationDate).day()).startOf('day').format('YYYY-MM-DD HH:mm')
        var compareDateEndTime = moment(this.formParameters.refrigerationDate).format('YYYY-MM-DD ') + nowTime
        var compareDateEndAllTime = moment(this.formParameters.refrigerationDate).day(moment(this.formParameters.refrigerationDate).day()).endOf('day').format('YYYY-MM-DD HH:mm')
        this.nowTime = nowTime
        this.axios.all([
          this.axios.get(api,{params: {begin: todayStartTime,end:todayEndTime,TagCode:"ZLLLoad"}}),//获取今天制冷量
          this.axios.get(api,{params: {begin: compareDateStartTime,end:compareDateEndTime,TagCode:"ZLLLoad"}}),//获取对比天截止当前时间制冷量
          this.axios.get(api,{params: {begin: compareDateStartTime,end:compareDateEndAllTime,TagCode:"ZLLLoad"}}),//获取对比整天制冷量
          this.axios.get(api,{params: {begin: todayStartTime,end:todayEndTime,TagCode:"TotalHotLoad"}}),//获取今天热负载
          this.axios.get(api,{params: {begin: compareDateStartTime,end:compareDateEndTime,TagCode:"TotalHotLoad"}}),//获取对比天截止当前时间热负载
          this.axios.get(api,{params: {begin: compareDateStartTime,end:compareDateEndAllTime,TagCode:"TotalHotLoad"}}),//获取对比整天热负载
        ]).then(this.axios.spread((todayData,CompareData,CompareAllData,hottodayData,hotCompareData,hotCompareAllData) =>{
          that.ZLtodayData = todayData.data
          that.ZLcompareData = CompareData.data
          that.ZLcompareAllDateData = CompareAllData.data
          that.hottodayData = hottodayData.data
          that.hotcompareData = hotCompareData.data
          that.hotcompareAllDateData = hotCompareAllData.data
        }))
      },
    }
  }
</script>
<style>

</style>
