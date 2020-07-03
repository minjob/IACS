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
                <el-aside width="200px" style="background-color:rgba(52, 56, 62, 1)">
                  <el-menu :default-openeds="['1']">
                    <el-submenu index="1">
                      <template slot="title"><i class="el-icon-message"></i>导航一</template>
                      <el-menu-item-group>
                        <template slot="title">分组一</template>
                        <el-menu-item index="1-1">选项1</el-menu-item>
                        <el-menu-item index="1-2">选项2</el-menu-item>
                      </el-menu-item-group>
                      <el-menu-item-group title="分组2">
                        <el-menu-item index="1-3">选项3</el-menu-item>
                      </el-menu-item-group>
                    </el-submenu>
                    <el-submenu index="2">
                      <template slot="title"><i class="el-icon-menu"></i>导航二</template>
                      <el-menu-item-group>
                        <template slot="title">分组一</template>
                        <el-menu-item index="2-1">选项1</el-menu-item>
                        <el-menu-item index="2-2">选项2</el-menu-item>
                      </el-menu-item-group>
                      <el-menu-item-group title="分组2">
                        <el-menu-item index="2-3">选项3</el-menu-item>
                      </el-menu-item-group>
                    </el-submenu>
                    <el-submenu index="3">
                      <template slot="title"><i class="el-icon-setting"></i>导航三</template>
                      <el-menu-item-group>
                        <template slot="title">分组一</template>
                        <el-menu-item index="3-1">选项1</el-menu-item>
                        <el-menu-item index="3-2">选项2</el-menu-item>
                      </el-menu-item-group>
                      <el-menu-item-group title="分组2">
                        <el-menu-item index="3-3">选项3</el-menu-item>
                      </el-menu-item-group>
                    </el-submenu>
                  </el-menu>
                </el-aside>
  
            <el-container>
              <el-header style="text-align: right; font-size: 12px; height:100px;">                  
               <el-row :gutter="30">
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
        value1:'',
        value2:'',
        value3:'',
        value4:'',
        value5:'',
        navOptionsCurrent:1,
        navOptions:[
            {name:"趋势分析",value:1},
            {name:"数据录入",value:2}
        ],
        TagCode:''
      }
    },
    mounted(){
      this.getValue()
      this.drawLine()
    },
    watch:{

    },
    computed:{ //计算属性

    },
    methods: {
      drawLine(){
      var myChart = echarts.init(document.getElementById('mainechart'));
      // 绘制图表
      var option={
        title: {
        text: 'ECharts 入门示例'
    },
    tooltip: {},
    xAxis: {
        data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
    },
    yAxis: {},
    series: [{
        name: '销量',
        type: 'bar',
        data: [5, 20, 36, 10, 10, 20]
    }]
      }
      myChart.setOption(option)
      },
      showPage(index) {
        this.navOptionsCurrent = index
      },
      getValue(){
        var params = {
          tableName:'TagMaintain',
          limit:1000,
          offset:0
        }
        var params1={
          begin:'2020-06-15 00:00:00',
          end:'2020-06-15 16:00:00',
          TagCode:this.TagCode
        }
        this.axios.get('/api/CUID',{params}).then((res) => {
          var alldata=JSON.parse(res.data).rows[0].TagCode
          console.log(alldata)
          this.TagCode=alldata
        })
        this.axios.get('/api/energytrendtu',{params:{params1}}).then((value) => {
          console.log(value)
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
  padding: 0;
}
.myechart{
  width: 100%;
  height: 100%;
  background-color: #666;
}
.row-bg{
  background-color: #ccc;
}

.el-col,.el-col-4{
  margin-right: 10px;
  padding-left: 0px;
  padding-right: 0px;
}
.mainShow .el-submenu__title, .el-submenu__title:hover {
  background: #34383E;
  color: #fff;
  font-size: 18px;
}

</style>
