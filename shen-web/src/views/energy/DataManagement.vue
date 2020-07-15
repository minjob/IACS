<template>
  <el-row :gutter="15">
      <el-col :span="24">
        <TabControl :TabControl="TabControl"></TabControl>
          <el-row :gutter="20" v-if="TabControl.TabControlCurrent === '趋势分析'">
              <el-col :span="6">
                <div class="Datepick platformContainer blackComponents" style="height:310px;">
                    <DatePicker type="date" multiple placeholder="Select date" style="width: 300px" v-model='valuedate' size="default" @on-ok="getSelectDate" :open='true' :confirm='true'></DatePicker>
                    
                </div>
                <div class="platformContainer blackComponents asidetree" style="height:750px;">
                    <el-tree 
                      :data="treedata"
                      show-checkbox
                      node-key="id"
                      ref="tree"
                      @check-change='getChecked()'
                      :default-expanded-keys="[2, 3]"
                      :default-checked-keys="[5]"
                      :props="defaultProps">
                    </el-tree>
                </div>
              </el-col>
              <el-col :span="18">
                <div class="platformContainer blackComponents" style="position:relative;">
                   <div id="main" style="width:100%; height:800px; backgroundColor:#3D4048;">数据图表</div>
                   <div class="Timepick" style="height:33px;width:175px">
                      <TimePicker  placeholder="选择时间" style="width: 168px" v-model='valuetime' :confirm='true' @on-ok="getSelectTime" ></TimePicker>
                  </div>
                   <div class="staticbox" style="width:100%; height:245px;">
                     <div class="platformContainer blackComponents" >
                       <div class="containBottom ">
                         <p>{{dateset[0]}}期间平均值</p>
                         <div class="cardContainer">{{averagevalue1}}</div>
                       </div>
                       <div class="containBottom ">
                         <p>选择期间对比时间</p>
                         <div class="cardContainer">{{comparetime}}</div>
                       </div>
                       <div class="containBottom ">
                         <p>{{dateset[1]}}期间平均值</p>
                         <div class="cardContainer">{{averagevalue2}}</div>
                       </div>
                     </div>
                     <div class="platformContainer blackComponents" >
                       <div class="containBottom ">
                         <p>{{dateset[2]}}期间平均值</p>
                         <div class="cardContainer">{{averagevalue3}}</div>
                       </div>
                       <div class="containBottom ">
                         <p>{{dateset[3]}}期间平均值</p>
                         <div class="cardContainer">{{averagevalue4}}</div>
                       </div>
                       <div class="containBottom ">
                         <p>{{dateset[4]}}期间平均值</p>
                         <div class="cardContainer">{{averagevalue5}}</div>
                       </div>
                     </div>
                   </div>
                </div>
              </el-col>
          </el-row>
          <el-row :gutter="20" v-if="TabControl.TabControlCurrent === '数据录入'">
              <span class="color-lightgreen">数据录入</span>
          </el-row>
      </el-col>
  </el-row>
</template>

<script>
  import TabControl from '@/components/TabControl'
  var moment = require('moment');
  import echarts from '@/assets/js/echarts.js'

  export default {
    name: "Home",
    components:{TabControl},
    data(){
      return {
        TabControl:{
          TabControlCurrent:"",
          TabControlOptions:[
            {name:"趋势分析"},
            {name:"数据录入"}
          ]
        },
        treedata:[],
        defaultProps: {
          children: 'children',
          label: 'label'
        },
        valuedate:'',
        dates:[],
        dataline1:[],
        dataline2:[],
        dataline3:[],
        dataline4:[],
        dataline5:[],
        maxvalue:10,
        averagevalue1:0,
        averagevalue2:0,
        averagevalue3:0,
        averagevalue4:0,
        averagevalue5:0,
        comparevalue:0,
        dataIndex:0,
        comparetime:'00:00:04',
        valuetime:'23:59:59',
        valuedate:[],
        starttime:'2020-06-20 00:00:00',
        endtime:'2020-06-20 08:30:00',
        childrentree:[],
        TagCodes:'',
        TagCode:'',
        treenumber:[],
        TagChecked:[],
        dateset:[],
        allday:'',//获取单个tag点日期字符串,
        yyddate:'2020-06-20'
      }
    },
    mounted(){
        this.getAsidemenu()
        this.dr()
    },
    watch:{

    },
    computed:{ //计算属性


    },
    methods: {
      drawLine(dataline1,dataline2,dataline3,dataline4,dataline5,dateset){
        var myChart = echarts.init(document.getElementById('main'));
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
                      width: 1
                  }
              },
              {
                  name: dateset[1],
                  type: 'line',
                  data: dataline2,
                  smooth: true,
                  showSymbol: false,
                  lineStyle: {
                      width: 1
                  }
              },
              {
                  name: dateset[2],
                  type: 'line',
                  data: dataline3,
                  smooth: true,
                  showSymbol: false,
                  lineStyle: {
                      width: 1
                  }
              },
              {
                  name: dateset[3],
                  type: 'line',
                  data: dataline4,
                  smooth: true,
                  showSymbol: false,
                  lineStyle: {
                      width: 1
                  }
              },
              {
                  name: dateset[4],
                  type: 'line',
                  data: dataline5,
                  smooth: true,
                  showSymbol: false,
                  lineStyle: {
                      width: 1
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
                    { coord: [this.dates[0],1000] }
                ]]
            }
              }
          ]
      };
    var j = 0; 
    var max = Math.max.apply(Math, this.dataline1); //数据的最大值
    option.series[0].data = this.dataline1;
    option.visualMap.pieces[0] = {gte: 500, lte: max, color: 'yellow'} //数据大于42742569显示黄色

//数据中的某一项为某个值时 分段显示
// var j = 0; 
// option.series[0].data = this.data1; 
// //连续为300时，颜色变为红色
// var arr=this.data1
// for(let i = 0; i < arr.length; i++) {
//     if(arr[i] === 300 && arr[i + 1] === 300) {
//         option.visualMap.pieces[j] =  {gte:i,lte:i+1,color:'red'}; 
//         j++; 
//     }
// }
    var that=this
     myChart.on('updateAxisPointer', function (event) {  //拉着tooltips 触发滑动事件
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
       }
     })
    myChart.off("click");//解绑事件处理函数（可根据情况而定是否需要，这里我这边会重绘几次表，所以需要解绑事件处理函数）。
    myChart.on('click', renderBrushed);
    function renderBrushed(params) {
      var time=params.name
      var datas=params.data
      var index=params.dataIndex
      that.dataIndex=params.dataIndex
      that.comparetime=params.name
      that.comparevalue=that.dataline1[index]
       myChart.setOption({
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
                    { coord: [that.comparetime,1000] }
                ]]
            }
              }
       })
        }
    myChart.setOption(option);
      },
      getAsidemenu(){
         var params = {
          tableName:'ParentTagMaintain',
          limit:1000,
          offset:0
        }
         this.axios.get('/api/CUID',{params}).then((res) => {
           var arr=JSON.parse(res.data).rows
          //  console.log(arr)
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
              // console.log(arr)
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
      getChecked(){
        var arr=this.$refs.tree.getCheckedNodes()
        console.log(arr)
        if(arr.length==1){
          this.TagCode=arr[0].id
          this.SingleTag(this.TagCode,this.allday)

       }else{
         //执行多个tagcodes 一天
        this.dateset=[]
        for(var i=0;i<arr.length;i++){
          if(arr[i].hasOwnProperty('ParentTagCode')){  //判断子节点
                this.dateset.push(arr[i].label)
            }
        }
        var j=0
        this.TagCodes=''
        for(var i=0;i<arr.length;i++){
          if(arr[i].hasOwnProperty('ParentTagCode')){  //判断子节点
            this.TagCodes=this.TagCodes+arr[i].id+','
            j++
          }
        }
        this.treenumber=j
        this.TagCodes=this.TagCodes.slice(0,-1)
        this.InitTrenddata(this.TagCodes,this.starttime,this.endtime)
       }
      },
      InitTrenddata(t,b,e){ //一天多个tag
         var params1={
            TagCodes:t,
            begin:b,
            end:e,
            TagFlag:'first'
          }
            this.axios.get('/api/energytrendtu',{params:params1}).then((res) => {
              var rows=[]
              var rows=res.data
              console.log(res)
              this.dates = rows.map(function (item) {
                return +item[1];
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
         SingleTag(tagcode,allday){ // 获取一个tag多天的数据
          var params={
            TagCode:tagcode,
            PointDates:allday,
            ParagraBegin:'08:00:00',
            ParagraEnd:'12:00:00',
          }
          this.axios.get('/api/energytrendtu',{params:params}).then((res)=>{
            console.log(res)

          })
      },
      dr(){
        var params={
          TagCode:"SCADA.AI.E119HTS_HF1AIWD",
          PointDates:'2020-06-18,2020-06-19,2020-06-20,2020-06-21,2020-06-22,',
          ParagraBegin:'08:00:00',
          ParagraEnd:'12:00:00',
        }
        var params2={
           TagCodes:'PersonHotLoad,People_No',
            begin:'2020-06-20 00:00:00',
            end:'2020-06-20 12:00:00',
            TagFlag:'first'
        }
        this.axios.get('/api/energytrendtu',{params:params}).then((res) => {
          console.log(res)
          
        })
      },
      getSelectDate(){
        if(this.valuedate[0]===false){
            console.log('请选择你的日期')
            return;
          }else if(this.valuedate.length>=2){ //5天 1个tag
            var arr=this.valuedate
            this.dateset=[]
            this.allday=''
            for(var i=0;i<arr.length;i++){
              this.yyddate=moment(arr[i]).format('YYYY-MM-DD')
              this.starttime=moment(arr[i]).format('YYYY-MM-DD  00:00:00')
              this.endtime=this.yyddate+' '+this.valuetime
              this.dateset.push(this.yyddate)
              this.allday=this.allday+this.yyddate+','
            }
           this.allday=this.allday.slice(0, -1)
        }else{ //1天 多个tag
            this.yyddate=moment(this.valuedate[0]).format('YYYY-MM-DD')
            this.starttime=moment(this.valuedate[0]).format('YYYY-MM-DD 00:00:00')
            this.endtime=moment(this.valuedate[0]).format('YYYY-MM-DD 23:59:59')
        }
      },
      getSelectTime(){     
        this.endtime=this.valuedate+' '+this.valuetime
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
    width: 175px;
    position: absolute;
    top: 10px;
}
.asidetree{
  overflow: auto;
}
</style>