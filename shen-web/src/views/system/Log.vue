<template>
  <el-row>
    <el-col :span="24">
      <div class="card-head">
        <span style="margin-left: 10px;" class="text-size-normol">系统日志</span>
      </div>
      <div class="platformContainer">
        <tableView class="blackComponents" :tableData="TableData" @getTableData="getTableData"></tableView>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  import tableView from '@/components/CommonTable'
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
            {prop:"OperationDate",label:"操作日期",showField:true,searchProp:true},
            {prop:"OperationContent",label:"操作内容",showField:true,searchProp:false},
            {prop:"OperationType",label:"类型",showField:true,searchProp:true},
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          searchProp:"",
          searchVal:"",
        },
      }
    },
    mounted() {
      this.getTableData()
    },
    methods:{
      getTableData(){
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

<style scoped>

</style>
