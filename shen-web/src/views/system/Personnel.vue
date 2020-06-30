<template>
  <el-row>
    <el-col :span="24">
      <div class="card-head">
        <span style="margin-left: 10px;" class="text-size-normol">人员管理</span>
      </div>
      <div class="platformContainer">
        <tableView :tableData="TableData" @getTableData="getTableData" @privileges="privileges"></tableView>
      </div>
      <el-dialog :title="selectPersonnelName" :visible.sync="dialogVisible" width="50%">
        <el-transfer :titles="['未拥有角色', '已分配角色']" :button-texts="['收回', '分配']" v-model="transferValue" :data="transferData"></el-transfer>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="savePrivileges">保存</el-button>
        </span>
      </el-dialog>
    </el-col>
  </el-row>
</template>

<script>
  var moment = require('moment');
  import tableView from '@/components/CommonTable'
  export default {
    name: "Personnel",
    components:{tableView},
    data(){
      return {
        TableData:{
          tableName:"User",
          column:[
            {prop:"Name",label:"用户名"},
            {prop:"WorkNumber",label:"工号"},
            {prop:"Creater",label:"创建人"},
            {prop:"CreateTime",label:"创建时间"},
            {prop:"LastLoginTime",label:"最近在线时间"},
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          searchProp:"",
          searchPropList:[
            {label:"用户名",prop:"Name"},
            {label:"工号",prop:"WorkNumber"}
          ],
          tableSelection:true, //是否在第一列添加复选框
          tableSelectionRadio:false, //是否需要单选
          searchVal:"",
          multipleSelection: [],
          dialogVisible: false,
          dialogTitle:'',
          rules:{
            Name:[
              {required: true, message: '请输入用户名', trigger: 'blur'}
            ],
            Password:[
              {required: true, message: '请输入密码', trigger: 'blur'}
            ],
            WorkNumber:[
              {required: true, message: '请输入工号', trigger: 'blur'}
            ]
          },
          handleType:[],
          handleForm:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true},
            {label:"用户名",prop:"Name",type:"input",value:""},
            {label:"密码",prop:"Password",type:"input",value:""},
            {label:"工号",prop:"WorkNumber",type:"input",value:"",reg:"/^[0-9]+$/"}
          ],
        },
        selectPersonnelName:"",
        dialogVisible:false,
        transferValue:[],
        transferData:[],
      }
    },
    created(){
      this.WhetherHavePermission()
    },
    mounted() {
      this.getTableData()
    },
    methods:{
      WhetherHavePermission(){
        let that = this
        this.axios.get("/api/permission/selectpermissionbyuser",{
          params: {PermissionName:"人员管理"}
        }).then(res =>{
          if(res.data === "OK"){
            var arr = [
              {type:"primary",label:"添加"},
              {type:"warning",label:"修改"},
              {type:"danger",label:"删除"},
              {type:"primary",label:"分配角色",clickEvent:"privileges"},
            ]
            that.TableData.handleType = arr
          }
        })
      },
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
      privileges(){
        if(this.TableData.multipleSelection.length === 1){
          this.dialogVisible = true
          this.selectPersonnelName = '为 '+this.TableData.multipleSelection[0].Name+' 分配角色'
          this.transferData = []
          this.transferValue = []
          var that = this
          var params = {
            UserID:this.TableData.multipleSelection[0].ID
          }
          this.axios.get("/api/role_management/selectrolebyuser",{
            params: params
          }).then(res =>{
            res.data.notHaveRows.forEach(item =>{
              that.transferData.push({
                key:item.ID,
                label:item.RoleName
              })
            })
            res.data.existingRows.forEach(item =>{
              that.transferValue.push(item.ID)
            })
          },res =>{
            console.log("获取角色时请求错误")
          })
        }else{
          this.$message({
            type: 'info',
            message: '请选择一位人员进行分配'
          });
        }
      },
      savePrivileges(){
        var selectPermissionArr = []
        this.transferValue.forEach(item =>{
          selectPermissionArr.push(item)
        })
        var params = {
          UserID: this.TableData.multipleSelection[0].ID,
          RoleIDs:JSON.stringify(selectPermissionArr)
        }
        this.axios.post("/api/role_management/saveroleuser",this.qs.stringify(params)).then(res =>{
          if(res.data === "OK"){
            this.$message({
              type: 'success',
              message: '分配成功'
            });
            this.dialogVisible = false
          }
        },res =>{
          console.log("保存角色时请求错误")
        })
      }
    }
  }
</script>

<style scoped>

</style>
