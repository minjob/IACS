<template>
  <el-row :gutter="15">
      <el-col :span="24">
        <TabControl :TabControl="TabControl"></TabControl>
          <el-row :gutter="20" v-if="TabControl.TabControlCurrent === '趋势分析'">
              <el-col :span="6">
                <div class="Datepick platformContainer blackComponents" style="height:310px;">
                    <DatePicker type="date" multiple placeholder="Select date" style="width: 300px" v-model='valuedate' size="large" :open='true'></DatePicker>
                </div>
                <div class="platformContainer blackComponents asidetree" style="height:791px;">
                    <el-tree 
                      :data="treedata"
                      show-checkbox
                      node-key="id"
                      ref="tree"
                      @check-change='getChecked()'
                      :props="defaultProps">
                    </el-tree>
                </div>
              </el-col>
              <el-col :span="18">
                 <div class="Timepick" style="height:42px;">
                      <el-time-picker is-range v-model="value1"  range-separator="至" start-placeholder="开始时间" end-placeholder="结束时间"  @change="getSelectTime" placeholder="选择时间范围"></el-time-picker>
                  </div>
                <div class="platformContainer blackComponents" style="position:relative;">
                   <div id="main" style="width:100%; height:750px; backgroundColor:#3D4048;" v-loading="loading">数据图表</div>
                   <div class="staticbox" style="width:100%; height:295px;">
                     <div class="platformContainer blackComponents">
                        <el-table
                            :data="tableData"
                            style="width: 100%">
                            <el-table-column
                              prop="name"
                              label="统计线名称"
                              >
                            </el-table-column>
                            <el-table-column
                              prop="comparetime"
                              label="对比时间"
                              width="180">
                            </el-table-column>
                            <el-table-column
                              prop="averag"
                              label="平均值"
                              width="180">
                            </el-table-column>
                            <el-table-column
                              prop="max"
                              label="最大值"
                              width="180">
                            </el-table-column>
                             <el-table-column
                              prop="min"
                              label="最小值"
                              width="180">
                            </el-table-column>
                          </el-table>                     
                     </div>
                   </div>
                </div>
              </el-col>
          </el-row>
          <el-row :gutter="20" v-if="TabControl.TabControlCurrent === '数据汇总分析'">
              <el-col :span=24 >
                   <div class="blackComponents">
                     <el-form ref="ruleForm">
                        <el-form-item>
                              <el-time-picker is-range v-model="value2"   class="selecttime" range-separator="至" start-placeholder="开始时间" end-placeholder="结束时间"  @change="getVal2" placeholder="选择时间范围"></el-time-picker>
                              <el-button type="primary">数据导入</el-button>
                              <el-button type="success">excel导出</el-button>
                        </el-form-item>
                     </el-form>
                   </div>
                    <tableView class="blackComponents" :tableData="TableData" @getTableData="getRepairTable" @takeOrder="takeOrder" ></tableView>
              </el-col>
          </el-row>
      </el-col>
  </el-row>
</template>

<script>
  import TabControl from '@/components/TabControl'
  import tableView from '@/components/CommonTable'
  var moment = require('moment');
  import echarts from '@/assets/js/echarts.js'

  export default {
    name: "Home",
    components:{TabControl,tableView},
    data(){
      return {
        TabControl:{
          TabControlCurrent:"",
          TabControlOptions:[
            {name:"趋势分析"},
            {name:"数据汇总分析"}
          ]
        },
         tableData: [{
            averag: 0,
            name: 'Tag1',
            comparetime:'00:00:04',
            max: 0,
            min:0
          },{
            averag: 0,
            comparetime:'00:00:04',
            name: 'Tag2',
            max: 0,
            min:0
          },{
            averag: 0,
            comparetime:'00:00:04',
            name: 'Tag3',
            max: 0,
            min:0
          },{
            averag: 0,
            comparetime:'00:00:04',
            name: 'Tag4',
            max: 0,
            min:0
          },{
            averag: 0,
            comparetime:'00:00:04',
            name: 'Tag5',
            max: 0,
            min:0
          },],
        treedata:[],
        defaultProps: {
          children: 'children',
          label: 'label'
        },
        dates:[],
        myChart:null,
        dataline1:[],
        dataline2:[],
        dataline3:[],
        dataline4:[],
        dataline5:[],
        maxvalue:10,
        time1:'06:00:00',
        time2:'18:00:00',
        loading:false,
        value1:[new Date(2020, 6, 20, 8, 40), new Date(2020, 6, 20, 9, 40)],
        value2:[new Date(2000, 10, 10, 10, 10), new Date(2000, 10, 11, 10, 10)],
        averagevalue1:0,
        averagevalue2:0,
        averagevalue3:0,
        averagevalue4:0,
        averagevalue5:0,
        dataIndex:0,
        comparetime:'00:00:04',
        valuedate:[],
        starttime:'2020-06-20 00:00:00',
        endtime:'2020-06-20 08:30:00',
        childrentree:[],
        TagCodes:"TY_CO2_AVG,B_CO2_AVG",
        TagCode:'',
        treenumber:[],
        TagChecked:[],
        dateset:[],
        allday:'',//获取单个tag点日期字符串,
        currentdate:'2020-06-20',
        tag1Max:0,
        tag1Min:0,
        tag2Max:0,
        tag2Min:0,
        tag3Max:0,
        tag3Min:0,
        tag4Max:0,
        tag4Min:0,
        tag5Max:0,
        tag5Min:0,
        TableData:{
          tableName:"DataSummaryAnalysis",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"CollectionDate",label:"日期",type:"input",value:""},
            {prop:"StationHallTemperature",label:"站厅温度",type:"input",value:"",showField:false,searchProp:false},
            {prop:"PlatformTemperature",label:"站台温度",type:"input",value:""},
            {prop:"StationHallHumidity",label:"站厅湿度",type:"input",value:""},
            {prop:"PlatformHumidity ",label:" 站台湿度",type:"input",value:""},
            {prop:"CarbonDioxideConten",label:"二氧化碳含量",type:"input",value:""},
            {prop:"ConsumptionLfirst",label:"L1冷水机组耗量",type:"input",value:""},
            {prop:"ConsumptionLsecond",label:"L2冷水机组耗量",type:"input",value:""},
            {prop:"ConsumptionLtotal",label:"冷水机组总耗量",type:"input",value:""}
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          
          multipleSelection:[],
          tableSelection:true, //是否在第一列添加复选框
          tableSelectionRadio:false, //是否需要单选
          // searchProp:"",
          // searchVal:"",  //控制搜索框
          dialogVisible: false,
          dialogTitle:'',
          handleType:[
            // {type:"primary",label:"添加"},
            // {type:"primary",label:"修改"},
            // {type:"primary",label:"删除"},//操作
            // {type:"primary",label:"数据导入",clickEvent:"takeOrder"}, //对应的按钮事件
            // {type:"success",label:"excel导出",clickEvent:"maintainOK"},
          ],
          rowClick:"handleEQRowClick",
          rowClickData:{},
        },
      }
    },
    mounted(){
        this.getAsidemenu()
        this.Initdesktop()
        this.getRepairTable()
        this.asD()
    },
    watch:{

    },
    computed:{ //计算属性


    },
    methods: {
      getVal2(){
        console.log(this.value2)
      },
      takeOrder(){
        console.log(1)
        console.log(this.TableData.multipleSelection)
      },
      getRepairTable(){
        var that = this
        var params = {
          tableName: this.TableData.tableName,
          limit:this.TableData.limit,
          offset:this.TableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          var data = JSON.parse(res.data)
          console.log(data)
          that.TableData.data = data.rows
          that.TableData.total = data.total
        },res =>{
          console.log("请求错误")
        })
      },
      drawLine(dataline1,dataline2,dataline3,dataline4,dataline5,dateset){
        if(this.myChart){
          this.myChart.dispose()
        }
        this.myChart= echarts.init(document.getElementById('main'));
        var option = {
              backgroundColor: '#3D4048',
              color:['#2db7f5','#ff6600'], 
              legend: {
                  data:dateset ,
                  inactiveColor: '#777',
                  textStyle: {
                      color: '#fff'
                  }
              },
              tooltip: {
                  trigger: 'axis',
                  axisPointer: {
                      animation: false,
                      type: 'cross',
                      lineStyle: {
                          color: '#376df4',
                          width: 2,
                          opacity: 1
                      }
                  }
              },
              toolbox: {
                      feature: {
                          dataZoom: {
                              yAxisIndex: false
                          },
                          brush: {
                              type: ['lineX', 'clear']
                          }
                      }
                  },
              brush: {
                      xAxisIndex: 'all',
                      brushLink: 'all',
                      outOfBrush: {
                      colorAlpha: 0.1
                  }
              },
          xAxis: {
              type: 'category',
              data:this.dates,
              axisLine: { lineStyle: { color: '#8392A5' } }
          },
          yAxis: {
              scale: true,
              axisLine: { lineStyle: { color: '#8392A5' } },
              splitLine: { show: false }
          },
          grid: {
              bottom: 80,
              top:80
          },
          animation: false,
          visualMap: {
              show: false,
              dimension: 1,
              pieces: [],  //pieces的值由动态数据决定
              outOfRange: {
                  color: 'green'
              }
          },
         
          series: [
              {
                  name: dateset[0],
                  type: 'line',
                  data: dataline1,
                  smooth: true,
                  showSymbol: false,
                  lineStyle: {
                      width: 1,
                      color:'#8CBD47'
                  }
              },
              {
                  name: dateset[1],
                  type: 'line',
                  data: dataline2,
                  smooth: true,
                  showSymbol: false,
                  lineStyle: {
                      width: 1,
                      color:'#00FF66'
                  }
              },
              {
                  name: dateset[2],
                  type: 'line',
                  data: dataline3,
                  smooth: true,
                  showSymbol: false,
                  lineStyle: {
                      width: 1,
                      color:'#5B9A92'
                  }
              },
              {
                name: dateset[3],
                  type: 'line',
                  data: dataline4,
                  smooth: true,
                  showSymbol: false,
                  lineStyle: {
                    width: 1,
                    color:'#E28A36'
                  }
              },
              {
                  name: dateset[4],
                  type: 'line',
                  data: dataline5,
                  smooth: true,
                  showSymbol: false,
                  lineStyle: {
                      width: 1,
                      color:'#990033'
                  }
              },
              {
	          name: '平行于y轴的对比线',
            type: 'line',
            markLine: {
                name: 'cc',
                symbol:'none',//去掉箭头
                lineStyle:{
                        type:"solid",
                        color:"#FF4B5C",
                    },
                data: [[
                    { coord: [this.dates[0],0] },
                    { coord: [this.dates[0],100] }
                ]]
            }
              }
          ]
      };
    var that=this
     this.myChart.on('updateAxisPointer', function (event) {  //拉着tooltips 触发滑动事件
       if(event.axesInfo.length!=0){
         var index=event.dataIndex
        if(index>that.dataIndex){
          var arr1=that.dataline1.slice(that.dataIndex,index)
          var arr2=that.dataline2.slice(that.dataIndex,index)
          var arr3=that.dataline3.slice(that.dataIndex,index)
          var arr4=that.dataline4.slice(that.dataIndex,index)
          var arr5=that.dataline5.slice(that.dataIndex,index)
          var index1=index-that.dataIndex
        }else{
          var arr1=that.dataline1.slice(index, that.dataIndex)
          var arr2=that.dataline2.slice(index, that.dataIndex)
          var arr3=that.dataline3.slice(index, that.dataIndex)
          var arr4=that.dataline4.slice(index, that.dataIndex)
          var arr5=that.dataline5.slice(index, that.dataIndex)
          var index1=that.dataIndex-index
        }
        var num1=0
        var num2=0
        var num3=0
        var num4=0
        var num5=0
        for(var i=0;i<arr1.length;i++){
            num1=num1+arr1[i]
         }
        for(var i=0;i<arr2.length;i++){
            num2=num2+arr2[i]
         }
        for(var i=0;i<arr3.length;i++){
            num3=num3+arr3[i]
         }
        for(var i=0;i<arr4.length;i++){
            num4=num4+arr4[i]
         }
        for(var i=0;i<arr5.length;i++){
            num5=num5+arr5[i]
         }
         that.averagevalue1=num1/index1
         that.averagevalue2=num2/index1
         that.averagevalue3=num3/index1
         that.averagevalue4=num4/index1
         that.averagevalue5=num5/index1
         that.tag1Max=Math.max.apply(Math, arr1)
         that.tag1Min=Math.min.apply(Math, arr1)
         that.tag2Max=Math.max.apply(Math, arr2)
         that.tag2Min=Math.min.apply(Math, arr2)
         that.tag3Max=Math.max.apply(Math, arr3)
         that.tag3Min=Math.min.apply(Math, arr3)
         that.tag4Max=Math.max.apply(Math, arr4)
         that.tag4Min=Math.min.apply(Math, arr4)
         that.tag5Max=Math.max.apply(Math, arr5)
         that.tag5Min=Math.min.apply(Math, arr5)
         that.InitTable()
       }
     })
    this.myChart.on('click', renderBrushed);
    function renderBrushed(params) {
      var time=params.name
      var datas=params.data
      var index=params.dataIndex
      that.dataIndex=params.dataIndex
      that.comparetime=params.name
      var maxline=[]
      maxline.push(that.dataline1[index],that.dataline2[index],that.dataline3[index],that.dataline4[index],that.dataline5[index])
      var max=Math.max.apply(Math, maxline)
      that.myChart.setOption({
          series:{
	          name: '平行于y轴的对比线',
            type: 'line',
            markLine: {
                name: 'cc',
                symbol:'none',//去掉箭头
                lineStyle:{
                        type:"solid",
                        color:"#FF4B5C",
                    },
                data: [[
                    { coord: [that.comparetime,0] },
                    { coord: [that.comparetime,max] }
                ]]
            }
              }
       })
       that.InitTable()
        }
    this.myChart.setOption(option);
      },
      getAsidemenu(){
         var params = {
          tableName:'ParentTagMaintain',
          limit:1000,
          offset:0
        }
         this.axios.get('/api/CUID',{params}).then((res) => {
           var arr=JSON.parse(res.data).rows
           for(var i=0;i<arr.length;i++){
            this.getTagcode(arr[i].ParentTagCode)
           }
           this.treedata=arr.map((item, index) => {
              return { id:item.ParentTagCode,label: item.ParentTagName,children:[]}
            })
         })
      },
      getTagcode(ParentTag){
         var params2={
          tableName:'TagMaintain',
          field:'ParentTagCode',
          fieldvalue:ParentTag,
          limit:100,
          offset:0
        }
        this.axios.get('/api/CUID',{params:params2}).then((value) => {
          var arr=JSON.parse(value.data).rows
              this.childrentree=arr.map((item, index) => {
              return { id: item.TagCode,label: item.TagName,ParentTagCode:item.ParentTagCode}
            })
            for(var i=0;i<this.treedata.length;i++){
              for(var j=0;j<this.childrentree.length;j++){
                if(this.treedata[i].id===this.childrentree[j].ParentTagCode){
                  this.treedata[i].children=this.childrentree
                }
              }
            }
            })
      },
      getSelectDate(){
        if(this.valuedate[0]===false){
            console.log('请选择你的日期')
            return;
          }else if(this.valuedate.length>=2){ //5天 1个tag
            var arr=this.valuedate
            this.dateset=[] //传给echarts时间
            this.allday='' //请求拼接字符
            for(var i=0;i<arr.length;i++){
              this.currentdate=moment(arr[i]).format('YYYY-MM-DD')
              this.starttime=this.currentdate+' '+this.time1
              this.endtime=this.currentdate+' '+this.time2
              this.dateset.push(this.currentdate)
              this.allday=this.allday+this.currentdate+','
            }
            this.allday=this.allday.slice(0, -1)
            console.log(this.starttime)
            console.log(this.endtime)
        }else{ //1天 多个tag
            this.allday=''
            this.currentdate=moment(this.valuedate[0]).format('YYYY-MM-DD')
            this.starttime=this.currentdate+' '+this.time1
            this.endtime=this.currentdate+' '+this.time2
            this.allday=this.currentdate
             console.log(this.starttime)
            console.log(this.endtime)
        }
      },
      getSelectTime(){     
        this.time1=moment(this.value1[0]).format('hh:mm:ss')
        this.time2=moment(this.value1[1]).format('hh:mm:ss')
      },
      getChecked(){ //选取
      this.getSelectDate()
        var arr=this.$refs.tree.getCheckedNodes()
        var ziset=[]
         for(var i=0;i<arr.length;i++){
          if(arr[i].hasOwnProperty('ParentTagCode')){  //判断子节点
               ziset.push(arr[i])
          }}
            if(ziset.length>=2){ //多个tag
                this.dateset=[]
                this.TagCodes=''
                for(var i=0;i<ziset.length;i++){
                  this.dateset.push(ziset[i].label)//多个tag
                  this.TagCodes=this.TagCodes+ziset[i].id+','
                }
              this.TagCodes=this.TagCodes.slice(0,-1)
              this.InitTrenddata(this.TagCodes,this.starttime,this.endtime)
            }else if(ziset.length===1){//单个tag 的情况
              this.getSelectTime()
              this.TagCode=ziset[0].id
              this.SingleTag(this.TagCode,this.allday)
            }else{
              console.log('选中的父节点')
            }
      },
       InitTrenddata(t,b,e){ //一天多个tag
         var params1={
            TagCodes:t,
            begin:b,
            end:e,
            TagFlag:'first'
          }
            this.loading=true
            this.axios.get('/api/energytrendtu',{params:params1}).then((res) => {
              var rows=res.data
              this.dates = rows.map(function (item) {
               return item[0];
              });
              this.dataline1 = rows.map(function (item) {
                 return +item[1];
               });
              this.dataline2 = rows.map(function (item) {
                return +item[2];
              });
              this.dataline3 = rows.map(function (item) {
                return +item[3];
              });
              this.dataline4 = rows.map(function (item) {
                return +item[4];
              });
              this.dataline5 = rows.map(function (item) {
                return +item[5];
              });
              this.loading=false
              this.drawLine(this.dataline1,this.dataline2,this.dataline3,this.dataline4,this.dataline5,this.dateset);
                })
      },
      SingleTag(tagcode,allday){ // 获取一个tag多天的数据
          var params={
            TagCode:tagcode,
            PointDates:allday,
            ParagraBegin:this.time1,
            ParagraEnd:this.time2,
          }
          this.loading=true
          this.axios.get('/api/energytrendtu',{params:params}).then((res)=>{
            var arr=res.data
            var indexs=[]
            for(var i=0;i<arr.length;i++){
             if(arr[i][0].slice(0,10)!=arr[i+1][0].slice(0,10)){
               indexs.push(i) //断点分区
               var firstarr=arr.slice(0,indexs[0]+1)
               var secondarr=arr.slice(indexs[0]+1,indexs[1]+1)
               var thirdarr=arr.slice(indexs[1]+1,indexs[2]+1)
               var fourtharr=arr.slice(indexs[2]+1,indexs[3]+1)
               var fiftharr=arr.slice(indexs[3]+1,indexs[4]+1)
               this.dates=firstarr.map(function (item) {
                  return item[0].slice(11, 19);
                });
               this.dataline1=firstarr.map(function (item) {
                return +item[1];
              });
               this.dataline2=secondarr.map(function (item) {
                return +item[1];
              });
               this.dataline3=thirdarr.map(function (item) {
                return +item[1];
              });
               this.dataline4=fourtharr.map(function (item) {
                return +item[1];
              });
               this.dataline5=fiftharr.map(function (item) {
                return +item[1];
              });
              this.loading=false
              this.drawLine(this.dataline1,this.dataline2,this.dataline3,this.dataline4,this.dataline5,this.dateset);
             }
            }
          })
      },
      InitTable(){
        for(var i=0;i<this.dateset.length;i++){
          this.tableData[i].name=this.dateset[i]
        }
         this.tableData[0].averag=this.averagevalue1
         this.tableData[0].max=this.tag1Max
         this.tableData[0].min=this.tag1Min
         this.tableData[1].averag=this.averagevalue2
         this.tableData[1].max=this.tag2Max
         this.tableData[1].min=this.tag2Min
         this.tableData[2].averag=this.averagevalue3
         this.tableData[2].max=this.tag3Max
         this.tableData[2].min=this.tag3Min
         this.tableData[3].averag=this.averagevalue4
         this.tableData[3].max=this.tag4Max
         this.tableData[3].min=this.tag4Min
         this.tableData[4].averag=this.averagevalue5
         this.tableData[4].max=this.tag5Max
         this.tableData[4].min=this.tag5Min
         for(var i=0;i<5;i++){
           this.tableData[i].comparetime=this.comparetime
         }
        
      },
      Initdesktop(){
         var params={
            TagCodes:"TY_CO2_AVG,B_CO2_AVG",
            begin:this.starttime,
            end:this.endtime,
            TagFlag:'first'
          }
          this.dateset=['桃园站CO2平均值','站厅CO2平均值']
            this.axios.get('/api/energytrendtu',{params:params}).then((res) => {
              var rows=res.data
              this.dates = rows.map(function (item) {
               return item[0];
              });
              this.dataline1 = rows.map(function (item) {
                 return +item[1];
               });
              this.dataline2 = rows.map(function (item) {
                return +item[2];
              });
              this.dataline3 = rows.map(function (item) {
                return +item[3];
              });
              this.dataline4 = rows.map(function (item) {
                return +item[4];
              });
              this.dataline5 = rows.map(function (item) {
                return +item[5];
              });
              this.drawLine(this.dataline1,this.dataline2,this.dataline3,this.dataline4,this.dataline5,this.dateset);
             
                })
      },
      asD(){
        var params={
          StartTime:"2020-06-20",
          EndTime:"2020-06-21"
        }
        this.axios.get('/api/exceloutdatasummaryanalysis',{params:params}).then((value) => {
          console.log(value)
        })
      }
    }
  }
</script>
<style scoped>
.containBottom{
  float: left;
  width:33%;
  height: 100px;;
  padding-right: 20px;
  text-align: center;
}
.containBottom p{
  width:100%;
  height: 30px;;
  padding-right: 15px;
  text-align: center;
}
.staticbox .platformContainer{
  margin-bottom: 0px;
  padding:15px 0px;
}
.staticbox .cardContainer{
  padding-left:0px;
}
.Timepick{
    width: 100%;
    padding-bottom: 10px;
    background-color: #3D4048;
}
.asidetree{
  overflow: auto;
  padding-left: 0px;
  padding-right: 0px;
}
</style>