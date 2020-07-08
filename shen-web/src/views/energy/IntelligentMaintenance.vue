<template>
  <el-row :gutter="15">
    <el-col :span="24">
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-normol">智能维保</span>
      </div>
      <div class="platformContainer">
        <tableView class="blackComponents" :tableData="TableData" @getTableData="getRoleTable"></tableView>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  import tableView from '@/components/CommonTable'
  var moment = require('moment');
  export default {
    name: "IntelligentMaintenance",
    components:{tableView},
    data(){
      return {
        TableData:{
          tableName:"Equipment",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"EquipmentCode",label:"设备编码",type:"input",value:""},
            {prop:"name",label:"设备名称",type:"input",value:""},
            {prop:"model",label:"设备型号",type:"input",value:""},
            {prop:"Quantity",label:"数量",type:"input",value:""},
            {prop:"Power",label:"功率",type:"input",value:""},
            {prop:"Area",label:"区域",type:"input",value:""},
            {prop:"Manufacturer",label:"生产商",type:"input",value:""},
            {prop:"Sap",label:"SAP号",type:"input",value:""},
            {prop:"FixedAssetsNo",label:"固定资产编号",type:"input",value:""},
            {prop:"FixedAssetsName",label:"固定资产名称",type:"input",value:""},
            {prop:"IntoTime",label:"开始运行日期",type:"input",value:""},
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          multipleSelection:[],
          tableSelection:true, //是否在第一列添加复选框
          tableSelectionRadio:true, //是否需要单选
          searchProp:"",
          searchVal:"",
          handleType:[
            {type:"warning",label:"快速保修"},
            {type:"primary",label:"下发保养任务"},
            {type:"primary",label:"制定保养计划"},
          ],
        },
      }
    },
    created(){
      this.getRoleTable()
    },
    mounted(){

    },
    watch:{

    },
    computed:{

    },
    methods: {
      getRoleTable(){
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
