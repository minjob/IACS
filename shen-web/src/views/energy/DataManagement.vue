<template>
  <el-row :gutter="15">
      <el-col :span="24">
        <TabControl :TabControl="TabControl"></TabControl>
          <el-row :gutter="20" v-if="TabControl.TabControlCurrent === '趋势分析'">
              <el-col :span="6">
                <div class="Datepick platformContainer blackComponents" style="height:500px;">
                    <DatePicker type="date" multiple placeholder="Select date" style="width: 300px" v-model='valuedate' size="default" @on-ok="getSelectDate" :open=true :confirm=true></DatePicker>
                
                </div>

                <div class="platformContainer blackComponents" style="height:750px;">
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
                <div class="platformContainer blackComponents">
                   <div id="main" style="width:100%; height:800px; backgroundColor:#3D4048;">数据图表</div>
                   <div class="staticbox" style="width:100%; height:245px;">
                     <div class="platformContainer blackComponents" >
                       <div class="containBottom ">
                         <p>选择期间平均值</p>
                         <div class="cardContainer">{{averagevalue}}</div>
                       </div>
                       <div class="containBottom ">
                         <p>选择期间对比时间</p>
                         <div class="cardContainer">{{comparetime}}</div>
                       </div>
                       <div class="containBottom ">
                         <p>选择期间平均值</p>
                         <div class="cardContainer">选择期间平均值</div>
                       </div>
                     </div>
                     <div class="platformContainer blackComponents" >
                       <div class="containBottom ">
                         <p>选择期间平均值</p>
                         <div class="cardContainer">选择期间平均值</div>
                       </div>
                       <div class="containBottom ">
                         <p>选择期间平均值</p>
                         <div class="cardContainer">选择期间平均值</div>
                       </div>
                       <div class="containBottom ">
                         <p>选择期间平均值</p>
                         <div class="cardContainer">选择期间平均值</div>
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
        rawdata:[],
        data1:[],
        data2:[],
        maxvalue:10,
        averagevalue:0,
        comparevalue:0,
        dataIndex:0,
        comparetime:'2020-04-18',
      }
    },
    mounted(){
        this.getAsidemenu()
    },
    watch:{

    },
    computed:{ //计算属性

    },
    methods: {
      drawLine(data1,data2){
        var myChart = echarts.init(document.getElementById('main'));
        var option = {
              backgroundColor: '#3D4048',
              color:['#2db7f5','#ff6600'], 
              legend: {
                  data: ['MA5', 'MA10'],
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
                  name: 'MA5',
                  type: 'line',
                  data: data1,
                  smooth: true,
                  showSymbol: false,
                  lineStyle: {
                      width: 1
                  }
              },
              {
                  name: 'MA10',
                  type: 'line',
                  data: data2,
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
                    { coord: [this.dates[0],42000000] },
                    { coord: [this.dates[0],52000000] }
                ]]
            }
              }
          ]
      };
    var j = 0; 
    var max = Math.max.apply(Math, this.data1); //数据的最大值
    option.series[0].data = this.data1;
    option.visualMap.pieces[0] = {gte: 42742569, lte: max, color: 'yellow'} //数据大于42742569显示黄色

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
          var arr=that.data1.slice(that.dataIndex,index)
          var index1=index-that.dataIndex
        }else{
          var arr=that.data1.slice(index, that.dataIndex)
          var index1=that.dataIndex-index
        }
        var num=0
        for(var i=0;i<arr.length;i++){
            num=num+arr[i]
         }
         that.averagevalue=num/index1
        //  console.log(that.averagevalue)
        //  console.log(that.dates[index])//当前的日期
        //  console.log(that.data1[index])//当前的第一个值
        //  console.log(that.comparevalue)//对比天的值
        //  console.log(that.data2[index])//当前的第二个值
       }
     })

    // var xAxisInfo=event.axesInfo //echarts官方样例
    // if (xAxisInfo) {
    //         var dimension = xAxisInfo.value + 1;
    //         myChart.setOption({
    //             series: {
    //                 id: 'pie',
    //                 label: {
    //                     formatter: '{b}: {@[' + dimension + ']} ({d}%)'
    //                 },
    //                 encode: {
    //                     value: dimension,
    //                     tooltip: dimension
    //                 }
    //             }
    //         });
    //     }

    //  });

    myChart.off("click");//解绑事件处理函数（可根据情况而定是否需要，这里我这边会重绘几次表，所以需要解绑事件处理函数）。
    myChart.on('click', renderBrushed);
    function renderBrushed(params) {
      var time=params.name
      var datas=params.data
      var index=params.dataIndex
      that.dataIndex=params.dataIndex
      that.comparetime=params.name
      that.comparevalue=that.data1[index]
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
                    { coord: [that.comparetime,42000000] },
                    { coord: [that.comparetime,52000000] }
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
        var params1={
          TagCodes:'MB2TCP3.A_ACR_10.Ep_total'+','+'MB2TCP3.A_ACR_13.Ep_total',
          begin:'2020-06-20 00:00:00',
          end:'2020-06-20 08:00:00',
          TagFlag:'first'
        }
        var params2={
          tableName:'TagMaintain',
          ParentTagCode:'LQ4',
          limit:100,
          offset:0
        }
         this.axios.get('/api/CUID',{params}).then((res) => {
           var arr=JSON.parse(res.data).rows
           console.log(arr)
           this.treedata=arr.map((item, index) => {
              return { id: index+1,label: item.ParentTagName,children:[{id:index+12,label:'Tag1'},{id:index+23,label:'Tag2'}]}
            })
            this.axios.get('/api/CUID',{params:params2}).then((value) => {
              console.log('---------------')
              var arr=JSON.parse(value.data)
                console.log(arr)
            })
            this.axios.get('/api/energytrendtu',{params:params1}).then((res) => {
              var rows=res.data
              this.rawdata=res.data
              this.dates = rows.map(function (item) {
                return item[0];
              });
              this.data1 = rows.map(function (item) {
                return +item[1];
              });
              this.data2 = rows.map(function (item) {
                return +item[2];
              });
              this.drawLine(this.data1,this.data2)
                })
         })
      },
      getChecked(){
        console.log(this.$refs.tree.getCheckedNodes());
      },
      getSelectDate(){
        console.log(this.valuedate)
        for(let i of this.valuedate){
          if(i===false){
            console.log('请选择你的日期')
            return;
          }
          console.log(moment(i).format('YYYY-MM-DD 23:59:00'))
        }
      }
    
    }
  }
</script>
<style scoped>
.ivu-date-picker-focused{
  width: 469px!important;
}
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
</style>