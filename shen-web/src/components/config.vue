<template>
  <div class="configBody">
    <div class="centerContainer">
      <div class="platformContainer">
        <el-tabs v-model="activeName">
          <el-tab-pane label="数据库建表" name="tableName">
            <tableView :tableData="tableNameData" :relatedTableData="FieldSetData" @getTableData="gettableNameTable"></tableView>
            <tableView :tableData="FieldSetData" @getTableData="getFieldSetTable" @privileges="resModel"></tableView>
          </el-tab-pane>
          <el-tab-pane label="字段类型" name="FieldType">
            <tableView :tableData="FieldTypeData" @getTableData="getFieldTypeTable"></tableView>
          </el-tab-pane>
          <el-tab-pane label="字段输入类型" name="InputTypeTable">
            <tableView :tableData="InputTypeTableData" @getTableData="getInputTypeTableTable"></tableView>
          </el-tab-pane>
          <el-tab-pane label="下拉框选择判断" name="ISFlag">
            <tableView :tableData="ISFlagData" @getTableData="getISFlagTable"></tableView>
          </el-tab-pane>
          <el-tab-pane label="权限维护" name="Permission">
            <tableView :tableData="PermissionData" @getTableData="getPermissionTable"></tableView>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<script>
  import tableView from '@/components/CommonTable'
  export default {
    name: "config",
    components:{tableView},
    data(){
      return {
        activeName: 'tableName',
        tableNameData:{
          tableName:"CreateTableSet",
          column:[
            {prop:"TableName",label:"表名"},
            {prop:"TableDescrip",label:"表名描述"},
            {prop:"ISFirstCheckBox",label:"第一列显示多选"},
            {prop:"SingleSelect",label:"是否单选"},
            {prop:"IsAdd",label:"是否可添加"},
            {prop:"IsUpdate",label:"是否可修改"},
            {prop:"IsDelete",label:"是否可删除"}
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          searchProp:"",
          searchPropList:[
            {label:"表名",prop:"TableName"},
            {label:"表名描述",prop:"TableDescrip"},
          ],
          handleType:[
            {type:"primary",label:"添加"},
            {type:"warning",label:"修改"},
            {type:"danger",label:"删除"}
          ],
          handleForm:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true},
            {label:"表名",prop:"TableName",type:"input",value:""},
            {label:"表名描述",prop:"TableDescrip",type:"input",value:""},
            {label:"第一列显示多选",prop:"ISFirstCheckBox",type:"select",Downtable:"ISFlag",showDownField:"Description",value:""},
            {label:"是否单选",prop:"SingleSelect",type:"select",Downtable:"ISFlag",showDownField:"Description",value:""},
            {label:"是否可添加",prop:"IsAdd",type:"select",Downtable:"ISFlag",showDownField:"Description",value:""},
            {label:"是否可修改",prop:"IsUpdate",type:"select",Downtable:"ISFlag",showDownField:"Description",value:""},
            {label:"是否可删除",prop:"IsDelete",type:"select",Downtable:"ISFlag",showDownField:"Description",value:""},
          ],
          searchVal:"",
          tableSelection:true, //是否在第一列添加复选框
          tableSelectionRadio:true, //是否需要单选
          multipleSelection: [],
          dialogVisible: false,
          dialogTitle:'',
          relatedTableField:"TableName",  //点击行的字段
          relatedChildTableField:"TableName",  //关联子表的字段搜索值
        },
        FieldSetData:{
          tableName:"FieldSet", //表名
          column:[  //表格列头
            {prop:"TableName",label:"表名"},
            {prop:"TitleName",label:"列头名称"},
            {prop:"FieldName",label:"字段名"},
            {prop:"Isedit",label:"是否可增改"},
            {prop:"Edittype",label:"输入类型"},
            {prop:"Downtable",label:"下拉数据表"},
            {prop:"Order",label:"下拉显示字段"},
            {prop:"Sortable",label:"是否排序"},
            {prop:"Visible",label:"是否显示列头"},
            {prop:"comment",label:"字段注释"},
            {prop:"type",label:"字段类型"},
            {prop:"length",label:"VARCHAR长度"},
            {prop:"primarykey",label:"是否为主键"},
            {prop:"autoincrement",label:"是否自增"},
            {prop:"nullable",label:"是否为空"}
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          searchProp:"",  //按字段搜索的下拉框和下拉值
          searchPropList:[
            {label:"表名",prop:"TableName"},
            {label:"列头名称",prop:"TitleName"},
            {label:"字段名",prop:"FieldName"},
          ],
          searchVal:"", //搜索值
          handleType:[ //增删改及其他操作表格按钮
            {type:"primary",label:"添加"},
            {type:"warning",label:"修改"},
            {type:"danger",label:"删除"},
            {type:"primary",label:"生成并重置model",clickEvent:"resModel"},
          ],
          handleForm:[  //模态框展示的表单和提交所需的数据
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true},
            {label:"表名",prop:"TableName",type:"input",value:""},
            {label:"列头名称",prop:"TitleName",type:"input",value:""},
            {label:"字段名",prop:"FieldName",type:"input",value:""},
            {label:"可增改",prop:"Isedit",type:"select",Downtable:"ISFlag",showDownField:"Description",value:""},
            {label:"输入类型",prop:"Edittype",type:"select",Downtable:"InputTypeTable",showDownField:"Type",value:""},
            {label:"下拉数据表",prop:"Downtable",type:"select",Downtable:"CreateTableSet",showDownField:"TableName",childProp:"Order",value:""},
            {label:"下拉显示字段",prop:"Order",type:"select",Downtable:"FieldSet",showDownField:"FieldName",searchField:"TableName",value:""},
            {label:"是否排序",prop:"Sortable",type:"select",Downtable:"ISFlag",showDownField:"Description",value:""},
            {label:"是否显示列头",prop:"Visible",type:"select",Downtable:"ISFlag",showDownField:"Description",value:""},
            {label:"字段注释",prop:"comment",type:"input",value:""},
            {label:"字段类型",prop:"type",type:"select",Downtable:"ISFlag",showDownField:"Description",value:""},
            {label:"VARCHAR长度",prop:"length",type:"input",value:""},
            {label:"是否为主键",prop:"primarykey",type:"select",Downtable:"ISFlag",showDownField:"Description",value:""},
            {label:"是否自增",prop:"autoincrement",type:"select",Downtable:"ISFlag",showDownField:"Description",value:""},
            {label:"是否为空",prop:"nullable",type:"select",Downtable:"ISFlag",showDownField:"Description",value:""},
          ],
          tableSelection:true, //是否在第一列添加复选框
          tableSelectionRadio:false, //是否需要单选
          multipleSelection: [],  //表格选中条的数据
          dialogVisible: false, //装载表单的模态框 开关
          dialogTitle:'', //模态框标题

        },
        FieldTypeData: {
          tableName: "FieldType",
          column: [
            {prop: "Type", label: "类型"},
            {prop: "Description", label: "描述"}
          ],
          data: [],
          limit: 5,
          offset: 1,
          total: 0,
          searchProp: "",
          searchPropList: [
            {label: "类型", prop: "Type"},
            {label: "描述", prop: "Description"}
          ],
          handleType: [
            {type: "primary", label: "添加"},
            {type: "warning", label: "修改"},
            {type: "danger", label: "删除"}
          ],
          handleForm: [
            {label: "ID", prop: "ID", type: "input", value: "", disabled: true},
            {label: "类型", prop: "Type", type: "input", value: ""},
            {label: "描述", prop: "Description", type: "input", value: ""}
          ],
          searchVal: "",
          tableSelection: true, //是否在第一列添加复选框
          tableSelectionRadio: false, //是否需要单选
          multipleSelection: [],
          dialogVisible: false,
          dialogTitle: '',
        },
        InputTypeTableData: {
          tableName: "InputTypeTable",
          column: [
            {prop: "Type", label: "类型"},
            {prop: "Title", label: "描述"}
          ],
          data: [],
          limit: 5,
          offset: 1,
          total: 0,
          searchProp: "",
          searchPropList: [
            {label: "类型", prop: "Type"},
            {label: "名称", prop: "Title"}
          ],
          handleType: [
            {type: "primary", label: "添加"},
            {type: "warning", label: "修改"},
            {type: "danger", label: "删除"}
          ],
          handleForm: [
            {label: "ID", prop: "ID", type: "input", value: "", disabled: true},
            {label: "类型", prop: "Type", type: "input", value: ""},
            {label: "名称", prop: "Title", type: "input", value: ""}
          ],
          searchVal: "",
          tableSelection: true, //是否在第一列添加复选框
          tableSelectionRadio: false, //是否需要单选
          multipleSelection: [],
          dialogVisible: false,
          dialogTitle: '',
        },
        ISFlagData: {
          tableName: "ISFlag",
          column: [
            {prop: "Flag", label: "标识"},
            {prop: "Description", label: "描述"}
          ],
          data: [],
          limit: 5,
          offset: 1,
          total: 0,
          searchProp: "",
          searchPropList: [
            {label: "标识", prop: "Flag"},
            {label: "描述", prop: "Description"}
          ],
          handleType: [
            {type: "primary", label: "添加"},
            {type: "warning", label: "修改"},
            {type: "danger", label: "删除"}
          ],
          handleForm: [
            {label: "ID", prop: "ID", type: "input", value: "", disabled: true},
            {label: "标识", prop: "Flag", type: "input", value: ""},
            {label: "描述", prop: "Description", type: "input", value: ""}
          ],
          searchVal: "",
          tableSelection: true, //是否在第一列添加复选框
          tableSelectionRadio: false, //是否需要单选
          multipleSelection: [],
          dialogVisible: false,
          dialogTitle: '',
        },
        PermissionData: {
          tableName: "Permission",
          column: [
            {prop: "PermissionName", label: "权限名字"},
            {prop: "PermissionType", label: "权限类型"},
            {prop: "Description", label: "描述"},
            {prop: "CreateData", label: "创建时间"},
          ],
          data: [],
          limit: 5,
          offset: 1,
          total: 0,
          searchProp: "",
          searchPropList: [
            {label: "权限名字", prop: "PermissionName"},
          ],
          handleType: [
            {type: "primary", label: "添加"},
            {type: "warning", label: "修改"},
            {type: "danger", label: "删除"}
          ],
          handleForm: [
            {label: "ID", prop: "ID", type: "input", value: "", disabled: true},
            {label: "权限名字", prop: "PermissionName", type: "input", value: ""},
            {label: "权限类型", prop: "PermissionType", type: "input", value: ""},
            {label: "描述", prop: "Description", type: "input", value: ""},
          ],
          searchVal: "",
          tableSelection: true, //是否在第一列添加复选框
          tableSelectionRadio: false, //是否需要单选
          multipleSelection: [],
          dialogVisible: false,
          dialogTitle: '',
        },
      }
    },
    created(){
      this.gettableNameTable()
      this.getFieldSetTable()
      this.getFieldTypeTable()
      this.getInputTypeTableTable()
      this.getISFlagTable()
      this.getPermissionTable()
    },
    methods:{
      gettableNameTable(){
        var that = this
        var params = {
          tableName: this.tableNameData.tableName,
          limit:this.tableNameData.limit,
          offset:this.tableNameData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          var data = JSON.parse(res.data)
          that.tableNameData.data = data.rows
          that.tableNameData.total = data.total
        },res =>{
          console.log("请求错误")
        })
      },
      getFieldSetTable(){
        var that = this
        var params = {
          tableName: this.FieldSetData.tableName,
          field:this.FieldSetData.searchProp,
          fieldvalue:this.FieldSetData.searchVal,
          limit:this.FieldSetData.limit,
          offset:this.FieldSetData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          var data = JSON.parse(res.data)
          that.FieldSetData.data = data.rows
          that.FieldSetData.total = data.total
        },res =>{
          console.log("请求错误")
        })
      },
      getFieldTypeTable(){
        var that = this
        var params = {
          tableName: this.FieldTypeData.tableName,
          limit:this.FieldTypeData.limit,
          offset:this.FieldTypeData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          var data = JSON.parse(res.data)
          that.FieldTypeData.data = data.rows
          that.FieldTypeData.total = data.total
        },res =>{
          console.log("请求错误")
        })
      },
      getInputTypeTableTable(){
        var that = this
        var params = {
          tableName: this.InputTypeTableData.tableName,
          limit:this.InputTypeTableData.limit,
          offset:this.InputTypeTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          var data = JSON.parse(res.data)
          that.InputTypeTableData.data = data.rows
          that.InputTypeTableData.total = data.total
        },res =>{
          console.log("请求错误")
        })
      },
      getISFlagTable(){
        var that = this
        var params = {
          tableName: this.ISFlagData.tableName,
          limit:this.ISFlagData.limit,
          offset:this.ISFlagData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          var data = JSON.parse(res.data)
          that.ISFlagData.data = data.rows
          that.ISFlagData.total = data.total
        },res =>{
          console.log("请求错误")
        })
      },
      getPermissionTable(){
        var that = this
        var params = {
          tableName: this.PermissionData.tableName,
          limit:this.PermissionData.limit,
          offset:this.PermissionData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          var data = JSON.parse(res.data)
          that.PermissionData.data = data.rows
          that.PermissionData.total = data.total
        },res =>{
          console.log("请求错误")
        })
      },
      resModel(){ //重置model
        if(this.FieldSetData.multipleSelection.length === 1){
          this.$confirm('确定删除所选记录？', '提示', {
            distinguishCancelAndClose:true,
            type: 'warning'
          }).then(()  => {
            this.axios.post("/api/system_set/make_model",{
              params: {

              }
            }).then(res =>{
              if(res === "OK"){
                this.$message({
                  type: 'success',
                  message: '重置成功'
                });
              }
            },res =>{
              console.log("请求失败")
            })
          }).catch(() => {
            this.$message({
              type: 'info',
              message: '已取消删除'
            });
          });
        }else{
          this.$message({
            type: 'info',
            message: '请选择一条角色进行分配'
          });
        }
      }
    }
  }
</script>

<style scoped>
  .configBody{
    width: 100%;
    height: 100%;
    overflow: auto;
  }
  .centerContainer{
    width: 1200px;
    height: 100%;
    margin: 0 auto;
  }
</style>
