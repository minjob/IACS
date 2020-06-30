<template>
  <el-row>
    <el-col :span="24">
      <div class="card-head">
        <span style="margin-left: 10px;" class="text-size-normol">角色管理</span>
      </div>
      <div class="platformContainer">
        <tableView :tableData="TableData" @getTableData="getRoleTable" @privileges="privileges"></tableView>
      </div>
      <el-dialog :title="selectRoleName" :visible.sync="dialogVisible" width="50%">
        <el-transfer :titles="['未拥有权限', '已分配权限']" :button-texts="['收回', '分配']" v-model="transferValue" :data="transferData"></el-transfer>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="savePrivileges">保存</el-button>
        </span>
      </el-dialog>
    </el-col>
  </el-row>
</template>

<script>
  import tableView from '@/components/CommonTable'
  export default {
    name: "Role",
    components:{tableView},
    data(){
      return {
        TableData:{
          tableName:"Role",
          column:[
            {prop:"RoleName",label:"角色名称"},
            {prop:"RoleCode",label:"角色编码"},
            {prop:"Description",label:"描述"},
            {prop:"ParentNode",label:"所属部门"},
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          multipleSelection:[],
          tableSelection:true, //是否在第一列添加复选框
          searchProp:"",
          searchPropList:[
            {label:"角色名称",prop:"RoleName"},
            {label:"角色编码",prop:"RoleCode"},
          ],
          searchVal:"",
          handleType:[
            {type:"primary",label:"分配权限",clickEvent:"privileges"},
          ],
        },
        dialogVisible:false,
        selectRoleName:"",
        transferValue:[],
        transferData:[],
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
      },
      privileges(){
        if(this.TableData.multipleSelection.length === 1){
          this.dialogVisible = true
          this.selectRoleName = '为 '+this.TableData.multipleSelection[0].RoleName+' 分配权限'
          this.transferData = []
          this.transferValue = []
          var that = this
          var params = {
            roleID:this.TableData.multipleSelection[0].ID
          }
          this.axios.get("/api/permission/selectpermissionbyrole",{
            params: params
          }).then(res =>{
            res.data.notHaveRows.forEach(item =>{
              that.transferData.push({
                key:item.ID,
                label:item.PermissionName
              })
            })
            res.data.existingRows.forEach(item =>{
              that.transferValue.push(item.ID)
            })
          },res =>{
            console.log("获取权限时请求错误")
          })
        }else{
          this.$message({
            type: 'info',
            message: '请选择一条角色进行分配'
          });
        }
      },
      savePrivileges(){
        var selectPermissionArr = []
        this.transferValue.forEach(item =>{
          selectPermissionArr.push(item)
        })
        var params = {
          roleID: this.TableData.multipleSelection[0].ID,
          permissionIDs:JSON.stringify(selectPermissionArr)
        }
        this.axios.post("/api/permission/saverolepermission",this.qs.stringify(params)).then(res =>{
          if(res.data === "OK"){
            this.$message({
              type: 'success',
              message: '分配成功'
            });
            this.dialogVisible = false
          }
        },res =>{
          console.log("保存权限时请求错误")
        })
      }
    }
  }
</script>

<style scoped>

</style>
