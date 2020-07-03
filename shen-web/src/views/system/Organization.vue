<template>
  <el-row :gutter="10">
    <el-col :span="24">
      <div class="page-title">
        <i v-if="showTypeValue === '看板视图'" class="el-icon-share" style="color: #FB3A06"></i>
        <i v-if="showTypeValue === '表格视图'" class="el-icon-s-grid" style="color: #FB3A06"></i>
        <span style="margin-left: 10px;" class="text-size-normol">组织结构</span>
        <el-radio-group v-model="showTypeValue" size="mini" class="page-title-radio" :border="false" fill="#00CAFA">
          <el-radio-button v-for="(item,index) in showType" :key="index" :label="item.label"></el-radio-button>
        </el-radio-group>
      </div>
      <el-form :inline="true" v-if="showTypeValue === '看板视图'">
        <el-form-item>
          <el-radio-group v-model="layoutValue" size="mini" @change="changeSettings">
            <el-radio-button v-for="item in layoutSettings" :key="item.label" :label="item.label"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-radio-group v-model="orientValue" size="mini" @change="changeSettings">
            <el-radio-button v-for="item in orientSettings" :key="item.label" :label="item.label"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-radio-group v-model="positionValue" size="mini" @change="changeSettings">
            <el-radio-button v-for="item in positionSettings" :key="item.label" :label="item.label"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-radio-group v-model="roamValue" size="mini" @change="changeSettings">
            <el-radio-button v-for="item in roamSettings" :key="item.label" :label="item.label"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-radio-group v-model="DepthValue" size="mini" @change="changeSettings">
            <el-radio-button v-for="item in DepthSettings" :key="item.label" :label="item.label"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="曲度：" style="">
          <div style="width: 100px;">
            <el-slider v-model="sliderValue" :max="1" :min="0" :step="0.1" @input="changeSettings"></el-slider>
          </div>
        </el-form-item>
        <el-form-item>
          <el-radio-group v-model="modeValue" size="mini" @change="changeSettings">
            <el-radio-button v-for="item in modeSettings" :key="item.label" :label="item.label"></el-radio-button>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <div class="platformContainer" v-if="showTypeValue === '看板视图'">
        <ve-tree :data="chartData" :settings="chartSettings" :events="events" height="600px"></ve-tree>
      </div>
      <el-col :span="24" v-else-if="showTypeValue === '表格视图'">
        <div class="platformContainer" style="margin-bottom: 10px;">
          <tableView class="blackComponents" :tableData="DepartmentTableData" @getTableData="getDepartmentTable" :relatedTableData="RoleTableData"></tableView>
        </div>
        <div class="platformContainer" style="margin-bottom: 10px;">
          <tableView class="blackComponents" :tableData="RoleTableData" @getTableData="getRoleTable"></tableView>
        </div>
      </el-col>

      <el-drawer :visible.sync="departmentDrawer" :with-header="false">
        <div style="padding: 20px;">
          <h3>{{ drawerTitle }}</h3>
          <el-form :model="departmentForm" label-width="80px" :rules="rules" ref="ruleForm">
            <el-form-item label="所属厂区">
              <el-input v-model="departmentForm.factory_name" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="部门名称" prop="department_name">
              <el-input v-model="departmentForm.department_name"></el-input>
            </el-form-item>
            <el-form-item label="部门编码" prop="department_code">
              <el-input v-model="departmentForm.department_code"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="departmentSave('ruleForm')">保存</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-drawer>
      <el-drawer :visible.sync="roleDrawer" :with-header="false">
        <div style="padding: 20px;">
          <h3>{{ drawerTitle }}</h3>
          <el-form :model="roleForm" label-width="80px" :rules="roleRules" ref="roleRuleForm">
            <el-form-item label="所属部门">
              <el-input v-model="roleForm.department_name" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="角色名称" prop="role_name">
              <el-input v-model="roleForm.role_name"></el-input>
            </el-form-item>
            <el-form-item label="角色编码" prop="role_code">
              <el-input v-model="roleForm.role_code"></el-input>
            </el-form-item>
            <el-form-item label="角色描述" prop="role_description">
              <el-input v-model="roleForm.role_description"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="roleSave('roleRuleForm')">保存</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-drawer>
      <el-dialog title="选择操作" :visible.sync="handleDialogVisible" width="30%" >
        <el-form>
          <el-form-item>
            <el-radio-group v-model="handleValue" fill="#082F4C" size="small" @change="handleChange">
              <el-radio-button v-for="item in handleSettings" :key="item.label" :label="item.label"></el-radio-button>
            </el-radio-group>
          </el-form-item>
        </el-form>
      </el-dialog>
    </el-col>
  </el-row>
</template>

<script>
  import tableView from '@/components/CommonTable'
  export default {
    name: "Organization",
    components:{tableView},
    data(){
      var self = this
      this.events = {
        click:function(e){
          self.clickTree(e)
        }
      }
      return {
        showTypeValue:"看板视图",
        showType:[
          {label:"看板视图"},
          {label:"表格视图"}
        ],
        orientValue:'向右',
        orientSettings: [
          {label:'向右'},
          {label:'向下'},
          {label:'向左'},
          {label:'向上'},
        ],
        positionValue:'标签靠右',
        positionSettings: [
          {label:'标签靠右'},
          {label:'靠下'},
          {label:'靠左'},
          {label:'靠上'},
        ],
        roamValue:'关闭',
        roamSettings: [
          {label:'关闭'},
          {label:'缩放'},
          {label:'平移'},
          {label:'缩放和平移'},
        ],
        layoutValue:'正交布局',
        layoutSettings: [
          {label:'正交布局'},
          {label:'径向布局'}
        ],
        DepthValue:'展示全部',
        DepthSettings: [
          {label:'展示全部'},
          {label:'3层'},
          {label:'2层'},
          {label:'1层'}
        ],
        modeValue:'查看模式',
        modeSettings: [
          {label:'查看模式'},
          {label:'编辑模式'}
        ],
        handleValue:'',
        handleSettings: [
          {label:'添加子节点'},
          {label:'修改'},
          {label:'删除'},
        ],
        sliderValue:0.5,
        chartSettings: {
          seriesMap:{
            tree: {
              orient: 'LR',
              lineStyle:{
                curveness:0.5,
                width: 1.5,
                color: "#ffffff"
              },
              roam:false,
              layout:"orthogonal",
              expandAndCollapse:true,
              initialTreeDepth:-1,
              symbolSize: 8,
              label:{
                position: 'right',
                color:"#ffffff"
              },
              itemStyle:{
                color:"#ffffff",
                borderColor:"#082F4C"
              }
            }
          },
        },
        chartData: {
          columns: ['name', 'value'],
          rows: [
            {name:"tree",value: []}
          ]
        },
        handleDialogVisible:false,
        departmentDrawer:false,
        drawerTitle:"",
        clicktype:"",
        clickTreeData:{},
        departmentForm:{
          did:"",
          factory_name:"",
          department_name:"",
          department_code:""
        },
        delDepartmentCode:"",
        delDepartmentName:"",
        rules:{
          department_name:[
            {required: true, message: '请输入部门名称', trigger: 'blur'}
          ],
          department_code:[
            {required: true, message: '请输入部门编码', trigger: 'blur'}
          ]
        },
        roleDrawer:false,
        roleForm:{
          did:"",
          department_name:"",
          rid:"",
          role_code:"",
          role_name:"",
          role_description:"",
        },
        roleRules:{
          role_name:[
            {required: true, message: '请输入角色名称', trigger: 'blur'}
          ],
          role_code:[
            {required: true, message: '请输入角色编码', trigger: 'blur'}
          ]
        },
        DepartmentTableData:{
          tableName:"DepartmentManager",
          column:[
            {prop:"DepartName",label:"部门名称"},
            {prop:"DepartCode",label:"部门编码"},
            {prop:"DepartLoad",label:"所属厂区"}
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          searchProp:"",
          searchPropList:[
            {label:"部门名称",prop:"DepartName"},
            {label:"部门编码",prop:"DepartCode"}
          ],
          searchVal:"",
          tableSelection:true, //是否在第一列添加复选框
          tableSelectionRadio:true, //是否需要单选
          multipleSelection: [],  //表格选中条的数据
          relatedTableField:"DepartCode",  //点击行的字段
          relatedChildTableField:"ParentNode",  //关联子表的字段搜索值
        },
        RoleTableData:{
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
          searchProp:"",
          searchPropList:[
            {label:"角色名称",prop:"RoleName"},
            {label:"角色编码",prop:"RoleCode"},
            {label:"所属部门",prop:"ParentNode"},
          ],
          searchVal:"",
        },
      }
    },
    created(){
      this.getTreeData()
      this.getDepartmentTable()
      this.getRoleTable()
    },
    methods: {
      getTreeData(){
        var that = this
        this.axios.get("/api/system_tree").then(res => {
          that.chartData.rows[0].value = [res.data]
        })
      },
      changeSettings(a){
        this.chartSettings.seriesMap.tree.lineStyle.curveness = this.sliderValue
        if(a === "向下"){
          this.chartSettings.seriesMap.tree.orient="TB"
        }else if(a === "向右"){
          this.chartSettings.seriesMap.tree.orient="LR"
        }else if(a === "向左"){
          this.chartSettings.seriesMap.tree.orient="RL"
        }else if(a === "向上"){
          this.chartSettings.seriesMap.tree.orient="BT"
        }else if(a === "关闭"){
          this.chartSettings.seriesMap.tree.roam=false
        }else if(a === "缩放"){
          this.chartSettings.seriesMap.tree.roam="scale"
        }else if(a === "平移"){
          this.chartSettings.seriesMap.tree.roam="move"
        }else if(a === "缩放和平移"){
          this.chartSettings.seriesMap.tree.roam=true
        }else if(a === "正交布局"){
          this.chartSettings.seriesMap.tree.layout="orthogonal"
        }else if(a === "径向布局"){
          this.chartSettings.seriesMap.tree.layout="radial"
        }else if(a === "展示全部"){
          this.chartSettings.seriesMap.tree.initialTreeDepth=-1
        }else if(a === "1层"){
          this.chartSettings.seriesMap.tree.initialTreeDepth=0
        }else if(a === "2层"){
          this.chartSettings.seriesMap.tree.initialTreeDepth=1
        }else if(a === "3层"){
          this.chartSettings.seriesMap.tree.initialTreeDepth=2
        }else if(a === "标签靠右"){
          this.chartSettings.seriesMap.tree.label.position="right"
        }else if(a === "靠下"){
          this.chartSettings.seriesMap.tree.label.position="bottom"
        }else if(a === "靠左"){
          this.chartSettings.seriesMap.tree.label.position="left"
        }else if(a === "靠上"){
          this.chartSettings.seriesMap.tree.label.position="top"
        }else if(a === "查看模式"){
          this.chartSettings.seriesMap.tree.expandAndCollapse=true
        }else if(a === "编辑模式"){
          this.chartSettings.seriesMap.tree.expandAndCollapse=false
        }
      },
      clickTree(e){
        if(this.modeValue === "编辑模式"){
          this.chartSettings.seriesMap.tree.expandAndCollapse=false
          this.getTreeData()
          this.handleValue = ''
          this.handleDialogVisible = true
          this.clickTreeData = e.data
        }
      },
      handleChange(){
        var clickType = this.clickTreeData.type
        this.drawerTitle = this.handleValue
        if(this.handleValue === "添加子节点"){
          if(clickType === "factory"){
            this.handleDialogVisible = false
            this.departmentDrawer = true
            this.departmentForm = {
              factory_name:this.clickTreeData.name,
              department_name:"",
              department_code:""
            }
          }else if(clickType === "department"){
            this.handleDialogVisible = false
            this.roleDrawer = true
            this.roleForm = {
              department_name:this.clickTreeData.name,
              did:this.clickTreeData.did,
              role_name:"",
              role_code:"",
              role_description:""
            }
          }else if(clickType === "role"){

          }else if(clickType === "user"){

          }
        }else if(this.handleValue === "修改"){
          if(clickType === "factory"){
            this.$message({
              type: 'info',
              message: "当前节点不可修改"
            });
          }else if(clickType === "department"){
            this.handleDialogVisible = false
            this.departmentDrawer = true
            this.departmentForm = {
              factory_name:this.clickTreeData.factory_name,
              did:this.clickTreeData.did,
              department_name:this.clickTreeData.name,
              department_code:this.clickTreeData.value
            }
          }else if(clickType === "role"){
            this.handleDialogVisible = false
            this.roleDrawer = true
            this.roleForm = {
              department_name:this.clickTreeData.department_name,
              rid:this.clickTreeData.rid,
              role_name:this.clickTreeData.name,
              role_code:this.clickTreeData.value,
              role_description:this.clickTreeData.role_description
            }
          }else if(clickType === "user"){

          }
        }else if(this.handleValue === "删除"){
          if(clickType === "factory"){
            this.$message({
              type: 'info',
              message: "当前节点不可删除"
            });
          }else if(clickType === "department"){
            this.handleDialogVisible = false
            this.$confirm('此操作将永久删除'+ this.clickTreeData.name +'节点, 是否继续?', '删除节点'+this.clickTreeData.name, {
              confirmButtonText: '确定',
              cancelButtonText: '取消',
              type: 'warning'
            }).then(() => {
              var headers = {
                department_code:this.clickTreeData.value
              }
              this.axios.delete("/api/system_tree/delete_department",{headers:headers}).then(res => {
                if(res.data.code === 10001){
                  this.$message({
                    type: 'success',
                    message: res.data.msg
                  });
                  this.departmentDrawer = false
                  this.getTreeData()
                  this.getDepartmentTable()
                  this.getRoleTable()
                }else{
                  this.$message({
                    type: 'info',
                    message: "新增失败"
                  });
                }
              })
            }).catch(() => {
              this.$message({
                type: 'info',
                message: '已取消删除'
              });
            });
          }else if(clickType === "role"){
            this.handleDialogVisible = false
            this.$confirm('此操作将永久删除'+ this.clickTreeData.name +'节点, 是否继续?', '删除节点'+this.clickTreeData.name, {
              confirmButtonText: '确定',
              cancelButtonText: '取消',
              type: 'warning'
            }).then(() => {
              var rid = {
                rid:this.clickTreeData.rid
              }
              this.axios.delete("/api/system_tree/delete_role",{headers:rid}).then(res => {
                if(res.data.code === 10004){
                  this.$message({
                    type: 'success',
                    message: res.data.msg
                  });
                  this.departmentDrawer = false
                  this.getTreeData()
                  this.getDepartmentTable()
                  this.getRoleTable()
                }else{
                  this.$message({
                    type: 'info',
                    message: "新增失败"
                  });
                }
              })
            }).catch(() => {
              this.$message({
                type: 'info',
                message: '已取消删除'
              });
            });
          }
        }
      },
      departmentSave(formName){
        this.$refs[formName].validate((valid) => {
          if (valid) {
            if(this.drawerTitle === "添加子节点"){
              this.axios.post("/api/system_tree/add_department",this.departmentForm).then(res => {
                if(res.data.code === 10000){
                  this.$message({
                    type: 'success',
                    message: res.data.msg
                  });
                  this.departmentDrawer = false
                  this.getTreeData()
                  this.getDepartmentTable()
                  this.getRoleTable()
                }else{
                  this.$message({
                    type: 'info',
                    message: "新增失败"
                  });
                }
              })
            }else if(this.drawerTitle === "修改"){
              this.axios.patch("/api/system_tree/update_department",this.departmentForm).then(res => {
                if(res.data.code === 10002){
                  this.$message({
                    type: 'success',
                    message: res.data.msg
                  });
                  this.departmentDrawer = false
                  this.getTreeData()
                  this.getDepartmentTable()
                  this.getRoleTable()
                }else{
                  this.$message({
                    type: 'info',
                    message: "修改失败"
                  });
                }
              })
            }
          } else {
            return false;
          }
        });
      },
      roleSave(formName){
        this.$refs[formName].validate((valid) => {
          if (valid) {
            if(this.drawerTitle === "添加子节点"){
              this.axios.post("/api/system_tree/add_role",this.roleForm).then(res => {
                if(res.data.code === 10003){
                  this.$message({
                    type: 'success',
                    message: res.data.msg
                  });
                  this.roleDrawer = false
                  this.getTreeData()
                  this.getDepartmentTable()
                  this.getRoleTable()
                }else{
                  this.$message({
                    type: 'info',
                    message: "新增失败"
                  });
                }
              })
            }else if(this.drawerTitle === "修改"){
              this.axios.patch("/api/system_tree/update_role",this.roleForm).then(res => {
                if(res.data.code === 10005){
                  this.$message({
                    type: 'success',
                    message: res.data.msg
                  });
                  this.roleDrawer = false
                  this.getTreeData()
                  this.getDepartmentTable()
                  this.getRoleTable()
                }else{
                  this.$message({
                    type: 'info',
                    message: "修改失败"
                  });
                }
              })
            }
          } else {
            return false;
          }
        });
      },
      getDepartmentTable(){
        var that = this
        var params = {
          tableName: "DepartmentManager",
            limit:this.DepartmentTableData.limit,
            offset:this.DepartmentTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          var data = JSON.parse(res.data)
          that.DepartmentTableData.data = data.rows
          that.DepartmentTableData.total = data.total
        },res =>{
          console.log("请求错误")
        })
      },
      getRoleTable(){
        var that = this
        var params = {
          tableName: "Role",
            limit:this.RoleTableData.limit,
            offset:this.RoleTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          var data = JSON.parse(res.data)
          that.RoleTableData.data = data.rows
          that.RoleTableData.total = data.total
        },res =>{
          console.log("请求错误")
        })
      },
    }
  }
</script>

<style scoped>

</style>
