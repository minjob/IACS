<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-normol">权限维护</span>
      </div>
      <div class="platformContainer">
        <tableView class="blackComponents" :tableData="PermissionTableData" @getTableData="getPermissionTable"></tableView>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  import tableView from '@/components/CommonTable'
  export default {
    name: "Permission",
    components:{tableView},
    data(){
      return {
        PermissionTableData:{
          tableName:"Permission",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"PermissionName",label:"权限名字",type:"input",value:""},
            {prop:"PermissionType",label:"权限类型",type:"input",value:""},
            {prop:"Description",label:"描述",type:"input",value:"",searchProp:false},
            {prop:"CreateData",label:"创建时间",type:"input",value:"",showField:false,searchProp:false,canSubmit:false},
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          tableSelection:true, //是否在第一列添加复选框
          searchProp:"",
          searchVal:"",
          multipleSelection: [],
          dialogVisible: false,
          dialogTitle:'',
          handleType:[
            {type:"primary",label:"添加",hasPermissions:['权限维护']},
            {type:"warning",label:"修改",hasPermissions:['权限维护']},
            {type:"danger",label:"删除",hasPermissions:['权限维护']},
          ],
        },
      }
    },
    created(){
      this.getPermissionTable()
    },
    methods:{
      getPermissionTable(){
        var that = this
        var params = {
          tableName: this.PermissionTableData.tableName,
          limit:this.PermissionTableData.limit,
          offset:this.PermissionTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          var data = JSON.parse(res.data)
          that.PermissionTableData.data = data.rows
          that.PermissionTableData.total = data.total
        },res =>{
          console.log("请求错误")
        })
      },
    }
  }
</script>

<style scoped>

</style>
