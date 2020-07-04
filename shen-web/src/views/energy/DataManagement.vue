<template>
  <el-row :gutter="15">
      <el-col :span="24">
       <div class="navOptionsItem">
        <ul>
          <li v-for="item in navOptions" @click="showPage(item.value)"><a href="javascript:;" :class="{ active:item.value===navOptionsCurrent }" v-html="item.name"></a></li>
        </ul>
      </div>
      </el-col>
      <el-col :span="24">
        <div class="mainShow">
            <el-container style="height: 887px;">
                <el-aside width="290px" style="background-color:rgba(52, 56, 62, 1)">
                  <el-menu :default-openeds="['1']">
                    <el-submenu  v-for="item in menuTagName" :key="item.ID" :index="1">
                      <template slot="title"><i class="el-icon-price-tag"></i>{{item.ParentTagName}}</template>
                      <el-menu-item-group>
                        <el-menu-item index="1-1">
                           <el-checkbox v-model="checked1" label="备选项1" :border="false" @change=selectChange()></el-checkbox>
                        </el-menu-item>
                      </el-menu-item-group>
                      <el-menu-item-group>
                        <el-menu-item index="1-1">
                           <el-checkbox v-model="checked2" label="备选项2" :border="false"></el-checkbox>
                        </el-menu-item>
                      </el-menu-item-group>
                    </el-submenu>
                  </el-menu>
                </el-aside>
  
            <el-container>
              <el-header style="text-align: right; font-size: 12px; height:100px;">                  
               <el-row v-if="controldate">
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
                <el-row v-if="!controldate">
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
var moment = require('moment');
import echarts from '@/assets/js/echarts.js'

  export default {
    name: "Home",
    data(){
      return {
        //时间绑定数值
        value1:'',
        value2:'',
        value3:'',
        value4:'',
        value5:'',
        menuTagName:[],
        controldate:true,
        checked1:true,
        checked2:true,//多选框的值绑定
        navOptionsCurrent:1,
        navOptions:[
            {name:"趋势分析",value:1},
            {name:"数据录入",value:2}
        ],
        TagCode:''
      }
    },
    created(){
      this.getValue()
    },
    mounted(){
      this.drawLine()
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
      drawLine(){
      var myChart = echarts.init(document.getElementById('mainechart'));
      // 绘制图表
      var option = {
          backgroundColor: '#21202D',//整个图的背景颜色
          legend: {
          data: ['xxx','xxx','xxx','xxx'],
          inactiveColor: '#777',
          textStyle: {
            color: '#fff'
        }
      },
          tooltip: { //提示框配置
          trigger: 'axis',
          axisPointer: {
          animation: false, //是否开启平移线颜色
          type: 'cross',//指示器类型，十字准星
          lineStyle: {  //提示框竖直线颜色
              color: '#555',
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
            data: dates,
            axisLine: { lineStyle: { color: '#8392A5' } } // x轴颜色
        },
          yAxis: {
          scale: true,
          axisLine: { lineStyle: { color: '#8392A5' } },
          splitLine: { show: false }
        },
          grid: { //图形界面距离上下左右的设置
            bottom: 80,
            top:20
        },
          dataZoom: [{
          textStyle: {
            color: '#fff'
        },
          handleSize: '60%',
          dataBackground: {
            areaStyle: {
                color: '#fff'//底部滑动条背景颜色
            },
            lineStyle: {
                opacity: 0.8,
                color: '#8392A5'//滑动栏内部线条颜色
            }
        },
          handleStyle: {
            color: '#fff',
            shadowBlur: 1,
            shadowColor: '#fff',
            shadowOffsetX: 2,
            shadowOffsetY: 2
        }
    }, {
        type: 'slider',  //slider表示有滑动块的，inside表示内置的
        dataBackground:'#fff',

    }],
    animation: false,
    series: [ // 驱动图表生成的数据内容数组，几条折现，数组中就会有几个对应对象，来表示对应的折线
        {
            name: name1,
            type: 'line', // pie->饼状图  line->折线图  bar->柱状图
            data: this.calculateMA(5, data),//5天内的收盘价之和/5  红线
            smooth: true,
            showSymbol: false,
            lineStyle: {
                width: 1
            }
        },
        {
            name: name2,
            type: 'line',
            data: this.calculateMA(10, data),//10天内的收盘价之和/10  灰线
            showSymbol: false,
            lineStyle: {
                width: 1
            }
        },
        {
            name: name3,
            type: 'line',
            data: this.calculateMA(20, data),//20天内的收盘价之和/20 蓝线
            smooth: true, 
            showSymbol: false,
            lineStyle: {
                width: 1
            }
        },
        {
            name: name4,
            type: 'line',
            data: this.calculateMA(30, data),//30天内的收盘价之和/30 橙线
            smooth: true,
            showSymbol: false,
            lineStyle: {
                width: 1
            }
        },
         {
            name: name5,
            type: 'line',
            data: this.calculateMA(40, data),//30天内的收盘价之和/30 橙线
            smooth: true,
            showSymbol: false,
            lineStyle: {
                width: 1
            }
        }
    ]
};
      myChart.setOption(option)
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
        this.axios.get('/api/CUID',{params}).then((res) => {
          console.log(JSON.parse(res.data))
          this.menuTagName=JSON.parse(res.data).rows

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
  background-color: #ccc;
}
.main  .el-aside {
  background-color: #34383E;
  color: #333;
  line-height: 60px;
}
.mainShow .el-main{
  overflow: hidden;
  padding: 0px;
}
.myechart{
  width: 100%;
  height: 100%;
  background-color: #666;
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
  width: 180px;
}
.confirmButton{
  width: 100%;
  height: 100%;
  padding-top: 16px;
  padding-left: 17px;
}
</style>
