<template>
  <el-row :gutter="15">
      <el-col :span="24">
        <TabControl :TabControl="TabControl"></TabControl>
          <el-row :gutter="20" v-if="TabControl.TabControlCurrent === '趋势分析'">
              <el-col :span="6">
                <div class="platformContainer blackComponents asidetree" style="height:1134px;">
                    <el-tree 
                      :data="treedata"
                      show-checkbox
                      node-key="id"
                      ref="tree"
                      default-expand-all
                      :props="defaultProps">
                    </el-tree>
                </div>
              </el-col>
              <el-col :span="18">
                 <div class="Timepick blackComponents" style="height:43px;">
                   <el-form>
                   <el-form-item label="开始时间">
                      <el-date-picker
                        v-model="valuedatetime1"
                        type="datetime"
                        placeholder="选择日期时间"
                        default-time="valuedatetime1">
                      </el-date-picker>
                  </el-form-item>
                  <el-form-item label="结束时间">
                       <el-date-picker
                        v-model="valuedatetime2"
                        type="datetime"
                        placeholder="选择日期时间"
                        default-time="valuedatetime2">
                      </el-date-picker>
                  </el-form-item>
                   </el-form>
                  <el-button type="primary" @click="StartMake">趋势查询</el-button>
                  <el-button type="success" @click="OutExcel">数据导出</el-button>
              </div>
              <el-dialog title="选择导出的趋势线" :visible.sync="isout" width="50%">
                  <div>
                    <el-checkbox-group v-model="checkedtag">
                      <el-checkbox v-for="(item,index) in dateset" :label="item" :key="index" border size="small"></el-checkbox>
                    </el-checkbox-group>
                  </div>
                  <span slot="footer" class="dialog-footer">
                    <el-button @click="isout = false">取 消</el-button>
                    <el-button type="primary" @click="saveTeamGroup">确定导出</el-button>
                  </span>
              </el-dialog>
              <div class="platformContainer blackComponents mainechart" style="position:relative;">
                   <div id="main" style="width:100%; height:750px; backgroundColor:#3D4048;" v-loading="loading">数据图表</div>
                   <div class="staticbox" style="width:100%; height:295px;overflow:auto;">
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
                          <div class="Timepick blackComponents" style="height:43px;marginBottom:0px;">
                      <el-form>
                      <el-form-item label="开始时间">
                        <el-date-picker
                          v-model="valuedatetime3"
                          type="date"
                          placeholder="选择日期">
                        </el-date-picker>
                    </el-form-item>
                    <el-form-item label="类型选择">
                      <el-select v-model="dateclass" placeholder="请选择日期类型">
                        <el-option label="日" value="day"></el-option>
                        <el-option label="月" value="month"></el-option>
                      </el-select>
                    </el-form-item>
                    <el-button type="primary" @click='Searchdata'>数据查询</el-button>
                    <el-button type="success" @click='Excelout'>excel导出</el-button>
                   </el-form>
                   </div>
                    </el-form-item>
                  </el-form>
                  </div>
                    <tableView class="blackComponents" :tableData="TableData" @getTableData="getRepairTable" @takeOrder="takeOrder" ></tableView>
              </el-col>
              <download-excel
                    class="export-excel-wrapper"
                    :data="json_data"
                    :fields="json_fields"
                    name="趋势图查询.xls">
                    <el-button type="primary" size="small">导出EXCEL</el-button>
              </download-excel>
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
        checkedtag:[],
        json_fields:{},
        json_data:[],
        json_meta:[],
        exo:[],
        allvalue:[],
        dateclass:'day',
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
            min:0,

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
          }],
        treedata:[],
        defaultProps: {
          children: 'children',
          label: 'label'
        },
        isout:false,
        value2:'',
        dates:[],
        myChart:null,
        dataline1:[],
        dataline2:[],
        dataline3:[],
        dataline4:[],
        dataline5:[],
        maxvalue:10,
        date1:moment().format('YYYY-MM-DD'),
        date2:moment().format('YYYY-MM-DD'),
        loading:false,
        averagevalue1:0,
        averagevalue2:0,
        averagevalue3:0,
        averagevalue4:0,
        averagevalue5:0,
        dataIndex:0,
        comparetime:'00:00:04',
        time1:'00:00:00',
        time2:'12:00:00',
        valuedatetime1:moment().format('YYYY-MM-DD 00:00:00'),
        valuedatetime2:moment().format('YYYY-MM-DD 12:00:00'),
        valuedatetime3:'2020-06-20',
        starttime:moment().format('YYYY-MM-DD 00:00:00'),
        endtime:moment().format('YYYY-MM-DD 12:00:00'),
        childrentree:[],
        TagCodes:"",
        TagCode:'',
        treenumber:[],
        TagChecked:[],
        dateset:[],
        allday:'',//获取单个tag点日期字符串,
        currentdate:moment().format('YYYY-MM-DD'),
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
            {prop:"StationHallTemperature",label:"站厅温度",type:"input",value:""},
            {prop:"PlatformTemperature",label:"站台温度",type:"input",value:""},
            {prop:"StationHallHumidity",label:"站厅湿度",type:"input",value:""},
            {prop:"PlatformHumidity",label:" 站台湿度",type:"input",value:""},
            {prop:"CarbonDioxideContent",label:"二氧化碳含量",type:"input",value:""},
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
          dialogVisible: false,
          dialogTitle:'',
          handleType:[
          ],
          rowClick:"handleEQRowClick",
          rowClickData:{},
        },
      }
    },
    mounted(){
        this.getAsidemenu()
        this.Initdesktop()
        this.Searchdata()
    },
    watch:{

    },
    computed:{ //计算属性


    },
    methods: {
      Excelout(){ //excel导出
      if(this.dateclass==='day'){
        var startTime=moment(this.valuedatetime3).format('YYYY-MM-DD')
        var endTime=moment(this.valuedatetime3).format('YYYY-MM-DD')
      }else{
         var startTime=moment(this.valuedatetime3).format('YYYY-MM-01')
         var endTime=moment(this.valuedatetime3).format('YYYY-MM-31')
      }
      window.location.href = "/api/exceloutdatasummaryanalysis?StartTime="+startTime+"&EndTime="+endTime
      },
      Searchdata(){ //数据查询按钮
        this.valuedatetime3=moment(this.valuedatetime3).format('YYYY-MM-DD')
        var params={
          CollectDay:this.valuedatetime3,
          CollectClass :this.dateclass,
          limit:this.TableData.limit,
          offset:this.TableData.offset - 1
        }
       this.axios.get('/api/insertdb_datasummaryanalysis',{params:params}).then((res) => {
          this.TableData.data = res.data.rows
          this.TableData.total = res.data.total
       })
      },
      saveTeamGroup(){
        this.exo=[]
        this.json_data=[]
       alert(this.checkedtag)
       for(var i=0;i<this.dateset.length;i++){
         for(var j=0;j<this.checkedtag.length;j++){
           if(this.dateset[i]===this.checkedtag[j]){
            this.exo.push(this.allvalue[i])
           }
         }
       }
      for(var i=0;i<this.exo.length;i++){
            var obj=this.exo[i].map((res) => {
             return {
                time1: res.time1,
                value1: res.value1,
                time2: res.time2,
                value2: res.value2
        }
            })
      this.json_data=obj
      }
      this.json_fields={"趋势线一时刻": "time1","数值": "value1","趋势线二时刻": "time2", "数值": "value2"}
      this.json_meta= [[{" key ": " charset "," value ": " utf- 8 "}]],
        this.isout=false
        this.checkedtag=[]
      },
      OutExcel(){
        this.isout=true
      },
      takeOrder(){
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
              color:['#4472C5','#ED7C30','#80FF80','#FF8096','#800080'], 
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
              yAxis: [{
                type: 'value',
                name: dateset[0],
                min: 10,
                max: 2500,
                position: 'left',
                axisLabel: {
                    formatter: '{value}',
                },
                axisLine: {
                    lineStyle: {
                        color: '#8392A5',
                    },
                },
              }],
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
                  yAxisIndex:0, 
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
         that.averagevalue1=(num1/index1).toFixed(2)
         that.averagevalue2=(num2/index1).toFixed(2)
         that.averagevalue3=(num3/index1).toFixed(2)
         that.averagevalue4=(num4/index1).toFixed(2)
         that.averagevalue5=(num5/index1).toFixed(2)
         that.tag1Max=Math.max.apply(Math, arr1).toFixed(2)
         that.tag1Min=Math.min.apply(Math, arr1).toFixed(2)
         that.tag2Max=Math.max.apply(Math, arr2).toFixed(2)
         that.tag2Min=Math.min.apply(Math, arr2).toFixed(2)
         that.tag3Max=Math.max.apply(Math, arr3).toFixed(2)
         that.tag3Min=Math.min.apply(Math, arr3).toFixed(2)
         that.tag4Max=Math.max.apply(Math, arr4).toFixed(2)
         that.tag4Min=Math.min.apply(Math, arr4).toFixed(2)
         that.tag5Max=Math.max.apply(Math, arr5).toFixed(2)
         that.tag5Min=Math.min.apply(Math, arr5).toFixed(2)
         that.InitTable()
       }
     })
    this.myChart.on('legendselectchanged',function(params){
      that.myChart.setOption({
         yAxis: [{
                type: 'value',
                name: params.name,
                min: this.tag1Min,
                max: this.tag1Max,
                position: 'left',
                axisLabel: {
                    formatter: '{value}',
                },
                axisLine: {
                    lineStyle: {
                        color: '#4E6EC1',
                    },
                },
              }]
       })
    })
    this.myChart.on('click', renderBrushed); //点击绘制对比线
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
         this.axios.get('/api/tags').then((res) => {
            this.treedata=res.data.data
         })
      },
      StartMake(){
        this.changestart()
        this.getChecked()
      },
      changestart(){
        if(moment(moment(this.valuedatetime1).format('YYYY-MM-DD HH:mm:ss')).diff(moment(moment(this.valuedatetime2).format('YYYY-MM-DD HH:mm:ss')), 'seconds')>0){
        this.$message({
          message: '时间选取错误，开始时间大于结束时间',
          type: 'warning'
        });
          return;
        }
        this.time1=moment(this.valuedatetime1).format('HH:mm:ss')
        this.date1=moment(this.valuedatetime1).format('YYYY-MM-DD')
        this.starttime=moment(this.valuedatetime1).format('YYYY-MM-DD HH:mm:ss')
        this.time2=moment(this.valuedatetime2).format('HH:mm:ss')
        this.date2=moment(this.valuedatetime2).format('YYYY-MM-DD')
        this.endtime=moment(this.valuedatetime2).format('YYYY-MM-DD HH:mm:ss')
        
      },
      getChecked(){ //选取选中的节点
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
              this.InitTrenddata(this.TagCodes)
            }else if(ziset.length===1){//单个tag 的情况
              this.TagCode=ziset[0].id
              this.SingleTag(this.TagCode)

            }else{
              console.log('选中的父节点')
            }
      },
       InitTrenddata(t){ //一天多个tag
         if(moment(this.valuedatetime1).format('YYYY-MM-DD')!==moment(this.valuedatetime2).format('YYYY-MM-DD')){
          this.$message({
            showClose: true,
            message: '渲染失败,选择了多天',
            type: 'error'
        });
          return;
        }
         var params1={
            TagCodes:t,
            begin:this.starttime,
            end:this.endtime,
            TagFlag:'first'
          }
            this.allvalue=[]
            this.loading=true
            this.axios.get('/api/energy_trend',{params:params1}).then((res) => {
              var rows=res.data.data
              this.allvalue=rows
              this.dates = rows[0].map(function (item) {
                return item.time1.slice(11, 19)
              })
              this.dataline1 = rows[0].map(function (item) {
                  return +item.value1;
               });
              this.dataline2 = rows[1].map(function (item) {
                  return +item.value2;
               });
               if(rows[2]){
                 this.dataline3 = rows[2].map(function (item) {
                  return +item.value3;
               });
               }else{
                 this.dataline3=[]
               }
              if(rows[3]){
                this.dataline4 = rows[3].map(function (item) {
                  return +item.value4;
               });
              }else{
                 this.dataline4=[]
               }
              if(rows[4]){
                this.dataline5 = rows[4].map(function (item) {
                  return +item.value5;
               });     
              }else{
                 this.dataline5=[]
               }
              this.loading=false
              this.drawLine(this.dataline1,this.dataline2,this.dataline3,this.dataline4,this.dataline5,this.dateset);
                })
      },
      SingleTag(tagcode){ // 获取一个tag多天的数据
          var params={
            TagCode:tagcode,
            start_date:this.date1,
            end_date:this.date2,
            start_time:this.time1,
            end_time:this.time2
          }
          this.loading=true
          this.allvalue=[]
          this.axios.get('/api/energy_trend',{params:params}).then((res)=>{
              var rows=res.data.data
              this.allvalue=rows
              this.dates= rows[0].map(function (item) {
                      return item.time1.slice(11, 19)
              })
               if(moment(this.valuedatetime1).format('YYYY-MM-DD')==moment(this.valuedatetime2).format('YYYY-MM-DD')){
                  this.dateset=[]
                  this.dateset.push(moment(this.valuedatetime1).format('YYYY-MM-DD'))
              }else{
                  this.dateset=res.data.date
              }
              this.dataline1 = rows[0].map(function (item) {
                  return +item.value1;
                });
              if(rows[1]){
                  this.dataline2 = rows[1].map(function (item) {
                    return +item.value2;
                });
                }else{
                 this.dataline2=[]
               }
              if(rows[2]){
                 this.dataline3 = rows[2].map(function (item) {
                  return +item.value3;
               });
               }else{
                 this.dataline3=[]
               }
              if(rows[3]){
                this.dataline4 = rows[3].map(function (item) {
                  return +item.value4;
               });
              }else{
                 this.dataline4=[]
               }
              if(rows[4]){
                this.dataline5 = rows[4].map(function (item) {
                  return +item.value5;
               });     
              }else{
                 this.dataline5=[]
               }
              this.loading=false
              this.drawLine(this.dataline1,this.dataline2,this.dataline3,this.dataline4,this.dataline5,this.dateset);
          })
      },
      InitTable(){
        this.tableData= [{averag: 0,name: 'Tag1',comparetime:'00:00:04',max: 0,min:0},{averag: 0,name: 'Tag2',comparetime:'00:00:04',max: 0,min:0},{averag: 0,name: 'Tag3',comparetime:'00:00:04',max: 0,min:0},{averag: 0,name: 'Tag4',comparetime:'00:00:04',max: 0,min:0},{averag: 0,name: 'Tag5',comparetime:'00:00:04',max: 0,min:0}]
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
            TagCodes:"ZT02_SD_AVG,ZT02_TEMP_AVG",
            begin:this.starttime,
            end:this.endtime,
            TagFlag:'first'
          }
          this.dateset=['站厅湿度平均值','站厅温度平均值']
          this.axios.get('/api/energy_trend',{params:params}).then((res) => {
              var rows=res.data.data
              this.allvalue=rows
              this.dates= rows[0].map(function (item) {
                return item.time1.slice(11, 19)
              })
              this.dataline1 = rows[0].map(function (item) {
                  return +item.value1;
               });
              this.dataline2 = rows[1].map(function (item) {
                  return +item.value2;
              });
              this.drawLine(this.dataline1,this.dataline2,this.dataline3,this.dataline4,this.dataline5,this.dateset);
                })
      }
    }
  }
</script>
<style scoped>
.containBottom{
  float: left;
  width:33%;
  height: 100px;
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
  margin-bottom: 15px;
  border-radius: 4px;
  background-color: #3D4048;
}
.asidetree{
  overflow: auto;
  padding-left: 0px;
  padding-right: 0px;
  border-radius: 4px;
}
.mainechart{
  border-radius: 4px;
}
</style>