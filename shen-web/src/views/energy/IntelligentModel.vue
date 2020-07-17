<template>
  <el-row :gutter="15">
    <el-col :span="24">
      <TabControl :TabControl="TabControl"></TabControl>
      <el-row v-if="TabControl.TabControlCurrent === '冷却塔运行策略'">
        <el-col :span="24">
          <div class="platformContainer blackComponents">
            <tableView :tableData="EnergyStrategyTableData" @getTableData="getScheduleTableData" @row-click="handlescheduledateRowClick"></tableView>
          </div>
          <div class="platformContainer blackComponents">
            <el-row :gutter="15">
              <el-col :span="18">
                <tableView :tableData="SchedulelqtTableData" @getTableData="getSchedulelqtTableData" @row-click="handlescheduledateRowClick"></tableView>
              </el-col>
              <el-col :span="6">
                <el-timeline>
                  <el-timeline-item
                    v-for="(activity, index) in SchedulelqtTimeLine"
                    :key="index"
                    :timestamp="activity.time">
                    {{ activity.label }}
                  </el-timeline-item>
                </el-timeline>
              </el-col>
            </el-row>
          </div>
        </el-col>
      </el-row>
    </el-col>
  </el-row>
</template>

<script>
  import TabControl from '@/components/TabControl'
  import tableView from '@/components/CommonTable'
  var moment = require('moment');
  export default {
    name: "IntelligentModel",
    components:{TabControl,tableView},
    data(){
      return {
        TabControl:{
          TabControlCurrent:"",
          TabControlOptions:[
            {name:"冷却塔运行策略"},
          ],
        },
        EnergyStrategyTableData:{
          tableName:"EnergyStrategy",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {label:"编号",prop:"Code",type:"input",value:""},
            {label:"启用标志",prop:"UseFlag",type:"input",value:""},
            {label:"类型",prop:"type",type:"input",value:""},
            {label:"说明",prop:"Comment",type:"input",value:"",showField:false,searchProp:false},
            {label:"创建时间",prop:"CreateTime",type:"input",value:"",searchProp:false},
            {label:"创建人",prop:"CreatePerson",type:"input",value:"",searchProp:false},
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          searchProp:"",
          tableSelection:true, //是否在第一列添加复选框
          tableSelectionRadio:true, //是否需要单选
          searchVal:"",
          multipleSelection: [],
          dialogVisible: false,
          dialogTitle:'',
          handleType:[
            // {type:"primary",label:"启用",hasPermissions:['管理工作日历']},
            // {type:"primary",label:"不启用",hasPermissions:['管理工作日历']},
          ],
          rowClick:"handlescheduledateRowClick",
          rowClickData:{},
        },
        SchedulelqtTableData:{
          tableName:"Schedulelqt",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {label:"开始时间",prop:"enablestarttime",type:"input",value:""},
            {label:"结束时间",prop:"enableendtime",type:"input",value:""},
            {label:"编码",prop:"energystrategyCode",type:"input",value:""},
            {label:"冷却塔1",prop:"lqt1_allowrun",type:"input",value:""},
            {label:"冷却塔2",prop:"lqt2_allowrun",type:"input",value:""},
            {label:"说明",prop:"comment",type:"input",value:"",searchProp:false},
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          tableSelection:true, //是否在第一列添加复选框
          tableSelectionRadio:true, //是否需要单选
          multipleSelection: [],
          handleType:[
            // {type:"primary",label:"启用",hasPermissions:['管理工作日历']},
            // {type:"primary",label:"不启用",hasPermissions:['管理工作日历']},
          ],
        },
        SchedulelqtTimeLine:[],
      }
    },
    created(){
      this.getScheduleTableData()
      this.getSchedulelqtTableData()
    },
    mounted(){

    },
    watch:{

    },
    computed:{

    },
    methods: {
      getScheduleTableData(){
        var that = this
        var params = {
          tableName: this.EnergyStrategyTableData.tableName,
          limit:this.EnergyStrategyTableData.limit,
          offset:this.EnergyStrategyTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          var data = JSON.parse(res.data)
          that.EnergyStrategyTableData.data = data.rows
          that.EnergyStrategyTableData.total = data.total
        })
      },
      getSchedulelqtTableData(){
        var that = this
        var params = {
          tableName: this.SchedulelqtTableData.tableName,
          limit:this.SchedulelqtTableData.limit,
          offset:this.SchedulelqtTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          var data = JSON.parse(res.data)
          that.SchedulelqtTableData.data = data.rows
          that.SchedulelqtTableData.total = data.total
          that.SchedulelqtTimeLine = []
          that.SchedulelqtTableData.data.forEach(item =>{
            that.SchedulelqtTimeLine.push(
              {time:item.enablestarttime,label:"开始时间"},
              {time:item.enableendtime,label:"结束时间"},
            )
          })
        })
      },
      handlescheduledateRowClick(){

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
