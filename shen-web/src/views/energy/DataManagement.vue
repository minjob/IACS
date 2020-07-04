<template>
  <el-row :gutter="15">
      <el-col :span="24">
        <TabControl :TabControl="TabControl"></TabControl>
        <div class="platformContainer" v-if="TabControl.TabControlCurrent === '能耗分析'">
          <span class="color-lightgreen">趋势分析</span>
        </div>
        <div class="platformContainer" v-if="TabControl.TabControlCurrent === '设备效率分析'">
          <span class="color-lightgreen">数据录入</span>
        </div>
      </el-col>
      <el-col :span="24">
        <div class="mainShow">
            <el-container style="height: 887px;">
                <el-aside width="290px" style="background-color:#3D4048">
                  <el-menu :default-openeds="['L4']">
                    <el-submenu  v-for="item in menuTagName" :key="item.ID" :index="item.ParentTagCode">
                      <template slot="title"><i class="el-icon-price-tag"></i>{{item.ParentTagName}}</template>
                      <el-menu-item-group>
                        <el-menu-item index="1-1">
                           <el-checkbox v-model="checked1" label="Tag1" :border="false" @change=selectChange()></el-checkbox>
                        </el-menu-item>
                      </el-menu-item-group>
                      <el-menu-item-group>
                        <el-menu-item index="1-2">
                           <el-checkbox v-model="checked2" label="Tag2" :border="false" @change=selectChange()></el-checkbox>
                        </el-menu-item>
                      </el-menu-item-group>
                    </el-submenu>
                  </el-menu>
                </el-aside>
  
            <el-container>
              <el-header style="text-align: right; font-size: 12px; height:100px;">                  
               <el-row v-if="this.controldate===false">
                  <el-col :span="4">
                    <div class="block">
                        <span class="demonstration">设置时间1</span>
                        <el-date-picker
                          v-model="value1"
                          type="datetime"
                          placeholder="选择日期时间"
                          default-time="12:00:00">
                        </el-date-picker>
                    </div>
                  </el-col>
                  <el-col :span="4">
                    <div class="block">
                        <span class="demonstration">设置时间2</span>
                        <el-date-picker
                          v-model="value2"
                          type="datetime"
                          placeholder="选择日期时间"
                          default-time="12:00:00">
                        </el-date-picker>
                    </div>
                  </el-col>
                  <el-col :span="4">
                     <div class="block">
                        <span class="demonstration">设置时间3</span>
                        <el-date-picker
                          v-model="value3"
                          type="datetime"
                          placeholder="选择日期时间"
                          default-time="12:00:00">
                        </el-date-picker>
                    </div>
                  </el-col>
                  <el-col :span="4">
                     <div class="block">
                        <span class="demonstration">设置时间4</span>
                        <el-date-picker
                          v-model="value4"
                          type="datetime"
                          placeholder="选择日期时间"
                          default-time="12:00:00">
                        </el-date-picker>
                    </div>
                  </el-col>
                  <el-col :span="4">
                     <div class="block">
                        <span class="demonstration">设置时间5</span>
                        <el-date-picker
                          v-model="value5"
                          type="datetime"
                          placeholder="选择日期时间"
                          default-time="12:00:00">
                        </el-date-picker>
                    </div>
                  </el-col>
                  <el-col :span="2">
                    <div class="confirmButton">
                      <el-button type="primary">确认选择</el-button>
                    </div>
                  </el-col>
                </el-row>
                <el-row v-if="this.controldate===true">
                  <el-col :span="4">
                    <div class="block">
                        <span class="demonstration">设置时间1</span>
                        <el-date-picker
                          v-model="value1"
                          type="datetime"
                          placeholder="选择日期时间"
                          default-time="12:00:00">
                        </el-date-picker>
                    </div>
                  </el-col>
                  <el-col :span="2">
                    <div class="confirmButton">
                      <el-button type="primary">确认选择</el-button>
                    </div>
                  </el-col>
                  </el-row>
              </el-header>
              
              <el-main>
                <div class="myechart">
                  <div id="mainechart" style="width:100%;height:100%;">

                  </div>
                </div>
              </el-main>
            </el-container>
        </el-container>
        </div>
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
          ],
        },
        //时间绑定数值
        value1:'',
        value2:'',
        value3:'',
        value4:'',
        value5:'',
        value6:'',
        menuTagName:[],
        controldate:true,
        checked1:true,
        checked2:true,//多选框的值绑定
        navOptionsCurrent:1,
        navOptions:[
            {name:"趋势分析",value:1},
            {name:"数据录入",value:2}
        ],
        TagCode:'',
        data1:[],
        data2:[],
        dates:[]
      }
    },
    mounted(){
      this.getValue()
    },
    watch:{

    },
    computed:{ //计算属性

    },
    methods: {
      selectChange(){
        if(this.checked1 && this.checked2){
          this.controldate=true
        }else{
          this.controldate=false
        }
      },
      drawLine(data1,data2){
      var myChart = echarts.init(document.getElementById('mainechart'));
      var option = {
          backgroundColor: '#21202D',
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
              }
          ]
      };
    myChart.setOption(option);
      },
      showPage(index) {
        this.navOptionsCurrent = index
},
      getValue(){
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
        this.axios.get('/api/CUID',{params}).then((res) => {
          this.menuTagName=JSON.parse(res.data).rows
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
       
      }
    }
  }
</script>
<style scoped>
 .second-header{
    background-color: #fff;
    height: 57px;
    width:100%;
    background:rgba(52,56,62,1);
    border-radius:4px;
  }
.home-container{
  background-color: #34383E;
}
.mainshow{
    width: 100%;
    height: 100%;
    background-color: #3D4048;
}
.mainshow img{
    width: 800px;
    height:800px;
}
#main{
  background-color: #fff;
}
.tree{
  height: 887px;
  background-color: #fff;
}
.mainShow .el-header{
  background-color: #3D4048;
}
.main  .el-aside {
  background-color: rgba(27, 30, 39, 1);
  color: #333;
  line-height: 60px;
}
.mainShow .el-main{
  overflow: hidden;
  padding: 0px;
  background-color:#21202D;
}
.myechart{
  padding-top: 20px;
  width: 100%;
  height: 100%;
  background-color: #21202D;
}
.row-bg{
  background-color: #ccc;
}
.mainShow .el-submenu__title, .el-submenu__title:hover {
  background: #34383E;
  color: #fff;
  font-size: 18px;
}
.el-date-editor.el-input{
  width: 170px;
}
.mainShow .el-row{
  padding-top: 10px;
  text-align: left;
}
.mainShow .block .demonstration{
  display: block;
  margin-bottom: 6px;
}
.confirmButton{
  width: 100%;
  height: 100%;
  padding-top: 22px;
  padding-left: 17px;
}

</style>