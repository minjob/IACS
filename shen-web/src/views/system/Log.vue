<template>
  <el-row>
    <el-col :span="24">
      <div class="card-head">
        <span style="margin-left: 10px;" class="text-size-normol">系统日志</span>
      </div>
      <div class="platformContainer">
        <tableView :tableData="TableData" @getTableData="getTableData"></tableView>
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
            {prop:"IP",label:"IP"},
            {prop:"ComputerName",label:"计算机名称"},
            {prop:"UserName",label:"操作用户"},
            {prop:"OperationDate",label:"操作日期"},
            {prop:"OperationContent",label:"操作内容"},
            {prop:"OperationType",label:"类型"},
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          searchProp:"",
          searchPropList:[
            {label:"操作用户",value:"UserName"},
            {label:"操作日期",value:"OperationDate"}
          ],
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
