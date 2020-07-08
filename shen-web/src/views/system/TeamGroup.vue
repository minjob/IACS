<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-normol">班组管理</span>
      </div>
      <div class="platformContainer">
        <tableView class="blackComponents" :tableData="TableData" @getTableData="getRoleTable"></tableView>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  import tableView from '@/components/CommonTable'
  export default {
    name: "TeamGroup",
    components:{tableView},
    data(){
      return {
        TableData:{
          tableName:"ShiftsGroup",
          column:[
            {prop:"ID",label:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"ShiftsGroupCode",label:"班组号",type:"input",value:""},
            {prop:"ShiftsGroupName",label:"班组名称",type:"input",value:""},
            {prop:"ShiftsGroupType",label:"班组类型",type:"input",value:""},
            {prop:"Description",label:"描述",type:"input",value:"",showField:false,searchProp:false},
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          searchProp:"",
          tableSelection:true, //是否在第一列添加复选框
          tableSelectionRadio:false, //是否需要单选
          searchVal:"",
          multipleSelection: [],
          dialogVisible: false,
          dialogTitle:'',
          handleType:[
            {type:"primary",label:"添加"},
            {type:"warning",label:"修改"},
            {type:"danger",label:"删除"},
          ],
        },
      }
    },
    created(){
      this.getRoleTable()
    },
    methods:{
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
      }
    }
  }
</script>

<style scoped>

</style>
