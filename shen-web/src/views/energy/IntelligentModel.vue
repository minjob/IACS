<template>
  <el-row :gutter="15">
    <el-col :span="24">
      <TabControl :TabControl="TabControl"></TabControl>
      <div class="platformContainer blackComponents" v-if="TabControl.TabControlCurrent === '冷却塔运行策略'">
        <tableView :tableData="scheduleTableData" @getTableData="getScheduleTableData" @row-click="handlescheduledateRowClick"></tableView>
      </div>
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
        scheduleTableData:{
          tableName:"scheduledatetype",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {label:"类型编码",prop:"DateTypeCode",type:"input",value:""},
            {label:"类型名称",prop:"DateTypeName",type:"input",value:""},
            {label:"注释",prop:"Desc",type:"input",value:""},
            {label:"颜色",prop:"color",type:"input",value:"",showField:false,searchProp:false},
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
      }
    },
    created(){
      this.getScheduleTableData()
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
          tableName: this.scheduleTableData.tableName,
          limit:this.scheduleTableData.limit,
          offset:this.scheduleTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          var data = JSON.parse(res.data)
          that.scheduleTableData.data = data.rows
          that.scheduleTableData.total = data.total
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
