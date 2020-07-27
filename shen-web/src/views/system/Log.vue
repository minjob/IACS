<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-normol">系统日志</span>
      </div>
      <div class="platformContainer blackComponents">
        <el-form :inline="true" :model="formParameters">
          <el-form-item label="选择查询时间">
            <el-date-picker type="date" v-model="formParameters.searchDate" size="mini" format="yyyy-MM-dd" style="width: 140px;" :clearable="false" @change="searchLogDate"></el-date-picker>
          </el-form-item>
        </el-form>
        <tableView class="blackComponents" :tableData="TableData" @getTableData="searchLogDate"></tableView>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  import tableView from '@/components/CommonTable'
  var moment = require('moment');
  export default {
    name: "Log",
    components:{tableView},
    data(){
      return{
        TableData:{
          tableName:"SysLog",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"IP",label:"IP",showField:true,searchProp:true},
            {prop:"ComputerName",label:"计算机名称",showField:true,searchProp:false},
            {prop:"UserName",label:"操作用户",showField:true,searchProp:true},
            {prop:"OperationDate",width:"160",label:"操作日期",showField:true,searchProp:true},
            {prop:"OperationContent",width:"600",label:"操作内容",showField:true,searchProp:false},
            {prop:"OperationType",width:"80",label:"类型",showField:true,searchProp:true},
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
        },
        formParameters:{
          searchDate:moment().format("YYYY-MM-DD")
        }
      }
    },
    mounted() {
      this.searchLogDate()
    },
    methods:{
      searchLogDate(){
        var that = this
        var params = {
          tableName: this.TableData.tableName,
          field:"OperationDate",
          fieldvalue:moment(this.formParameters.searchDate).format("YYYY-MM-DD"),
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
      }
    }
  }
</script>

<style scoped>

</style>
