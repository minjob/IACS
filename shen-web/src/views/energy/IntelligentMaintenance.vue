<template>
  <el-row :gutter="15">
    <el-col :span="24">
      <TabControl :TabControl="TabControl"></TabControl>
      <el-row :gutter="15" v-if="TabControl.TabControlCurrent === '设备台账'">
        <el-col :span="24" v-if="!showRepairsForm && !showMaintainForm && !showKeepPlanForm">
          <div class="platformContainer">
            <tableView class="blackComponents" :tableData="TableData" @getTableData="getEQTable" @repairs="repairs" @handleEQRowClick="handleEQRowClick" @drawUpKeepPlan="drawUpKeepPlan" @seeKeepPlan="seeKeepPlan"></tableView>
          </div>
          <el-dialog :title="TableData.rowClickData.EquipmentCode + '保养计划'" :visible.sync="keepPlandialogVisible" width="70%">
            <el-table :data="KeepPlanTableData.data" border>
              <el-table-column v-for="(item,index) in KeepPlanTableData.column" :key="index" :prop="item.prop" :label="item.label"></el-table-column>
            </el-table>
            <span slot="footer" class="dialog-footer">
              <el-button @click="keepPlandialogVisible = false">取 消</el-button>
            </span>
          </el-dialog>
          <el-form :inline="true" class="marginBottom">
            <el-radio-group v-model="showLogTypeValue" size="mini" :border="false">
              <el-radio-button v-for="item in showLogType" :key="item.label" :label="item.label"></el-radio-button>
            </el-radio-group>
          </el-form>
          <div class="platformContainer blackComponents" v-if="showLogTypeValue === '维修记录'">
            <el-form :inline="true">
              <el-form-item>
                <el-button type="primary" icon="el-icon-s-claim" size="small" @click="seeMaintainForm">查看维修单</el-button>
              </el-form-item>
            </el-form>
            <el-table :data="repairsLogTableData.data" border ref="multipleTableRepairsLog" @selection-change="handleRepairsLogSelectionChange" @row-click="handleRepairsLogRowClick">
              <el-table-column type="selection"></el-table-column>
              <el-table-column v-for="(item,index) in repairsLogTableData.column" :key="index" :prop="item.prop" :label="item.label"></el-table-column>
            </el-table>
            <div class="paginationClass">
              <el-pagination background  layout="total, sizes, prev, pager, next, jumper"
               :total="repairsLogTableData.total"
               :current-page="repairsLogTableData.offset"
               :page-sizes="[5,10,20]"
               :page-size="repairsLogTableData.limit"
               @size-change="handleRepairsLogSizeChange"
               @current-change="handleRepairsLogCurrentChange">
              </el-pagination>
            </div>
          </div>
          <div class="platformContainer blackComponents" v-if="showLogTypeValue === '保养记录'">
            <el-table :data="keepLogTableData.data" border ref="multipleTableKeepLog" @selection-change="handleKeepLogSelectionChange" @row-click="handleKeepLogRowClick">
              <el-table-column type="selection"></el-table-column>
              <el-table-column v-for="(item,index) in keepLogTableData.column" :key="index" :prop="item.prop" :label="item.label"></el-table-column>
            </el-table>
            <div class="paginationClass">
              <el-pagination background  layout="total, sizes, prev, pager, next, jumper"
               :total="keepLogTableData.total"
               :current-page="keepLogTableData.offset"
               :page-sizes="[5,10,20]"
               :page-size="keepLogTableData.limit"
               @size-change="handleKeepLogSizeChange"
               @current-change="handleKeepLogCurrentChange">
              </el-pagination>
            </div>
          </div>
        </el-col>
        <el-col :span="24" v-if="showRepairsForm">
          <el-button @click="showRepairsForm = false" icon="el-icon-back" size="small" class="marginBottom">返回列表</el-button>
          <div class="platformContainer blackComponents">
            <el-divider>设备报修信息</el-divider>
            <table class="elementTable marginBottom">
              <tr>
                <td>设备编码：{{ TableData.multipleSelection[0].EquipmentCode }}</td>
              </tr>
              <tr>
                <td colspan="4"><p class="marginBottom">故障阐述：</p><el-input type="textarea" v-model="faultCondition"></el-input></td>
              </tr>
            </table>
            <el-button @click="submitRepairs" type="primary" size="small">提交报修信息</el-button>
          </div>
        </el-col>
        <el-col :span="24" v-if="showMaintainForm">
          <el-button @click="showMaintainForm = false" icon="el-icon-back" size="small" class="marginBottom">返回列表</el-button>
          <div class="platformContainer blackComponents">
            <el-divider>设备维修记录单</el-divider>
            <table class="elementTable marginBottom">
              <tr>
                <td>工单号：{{ repairsLogTableData.multipleSelection[0].No }}</td>
                <td>设备编码：{{ repairsLogTableData.multipleSelection[0].EquipmentCode }}</td>
              </tr>
              <tr>
                <td>报修人：{{ repairsLogTableData.multipleSelection[0].Worker }}</td>
                <td>报修时间：{{ repairsLogTableData.multipleSelection[0].ApplyTime }}</td>
              </tr>
              <tr>
                <td>维修人（接单人）：{{ repairsLogTableData.multipleSelection[0].ReceiveWorker }}</td>
                <td>接单时间：{{ repairsLogTableData.multipleSelection[0].ReceiveTime }}</td>
              </tr>
              <tr>
                <td>维修内容：{{ repairsLogTableData.multipleSelection[0].Content }}</td>
                <td>完成时间：{{ repairsLogTableData.multipleSelection[0].EndTime }}</td>
              </tr>
            </table>
          </div>
        </el-col>
        <el-col :span="24" v-if="showKeepPlanForm">
          <el-button @click="showKeepPlanForm = false" icon="el-icon-back" size="small" class="marginBottom">返回列表</el-button>
          <div class="platformContainer blackComponents">
            <el-divider>制定保养计划</el-divider>
            <table class="elementTable marginBottom">
              <tr>
                <td colspan="2">设备编码：{{ KeepPlanEquipmentCode.join() }}</td>
              </tr>
              <tr>
                <td>
                  任务开始时间：<el-date-picker v-model="keepTaskStartTime" type="datetime" size="mini" :clearable="false" :editable="false"></el-date-picker>
                </td>
                <td>
                  制定类型：
                  <el-radio-group v-model="KeepTypeRadio">
                    <el-radio label="单次">单次制定</el-radio>
                    <el-radio label="周期">周期制定</el-radio>
                  </el-radio-group>
                </td>
              </tr>
              <tr>
                <td>
                  <el-form :inline="true">
                    <el-form-item label="保养周期：" style="margin-bottom: 0;">
                      <el-select v-model="weekNumber" placeholder="请选择">
                        <el-option label="1" value="1"></el-option>
                        <el-option label="2" value="2"></el-option>
                        <el-option label="3" value="3"></el-option>
                        <el-option label="4" value="4"></el-option>
                        <el-option label="5" value="5"></el-option>
                        <el-option label="6" value="6"></el-option>
                        <el-option label="7" value="7"></el-option>
                        <el-option label="8" value="8"></el-option>
                        <el-option label="9" value="9"></el-option>
                        <el-option label="10" value="10"></el-option>
                        <el-option label="11" value="11"></el-option>
                      </el-select>
                    </el-form-item>
                    <el-form-item style="margin-bottom: 0;">
                      <el-select v-model="weekTime" placeholder="请选择">
                        <el-option v-for="item in weekTimeType" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                      </el-select>
                    </el-form-item>
                  </el-form>
                </td>
                <td>
                  <el-form>
                    <el-form-item label="计划描述：" style="margin-bottom: 0;">
                      <el-input type="textarea" v-model="KeekPlanContent"></el-input>
                    </el-form-item>
                  </el-form>
                </td>
              </tr>
            </table>
            <el-button @click="submitKeekPlan" type="primary" size="small">提交保养计划</el-button>
          </div>
        </el-col>
      </el-row>
      <el-row :gutter="15" v-if="TabControl.TabControlCurrent === '设备维修任务'">
        <el-col :span="24">
          <div class="platformContainer">
            <tableView class="blackComponents" :tableData="RepairTableData" @getTableData="getRepairTable" @takeOrder="takeOrder" @maintainOK="maintainOK"></tableView>
          </div>
        </el-col>
      </el-row>
      <el-row :gutter="15" v-if="TabControl.TabControlCurrent === '设备保养任务'">
        <el-col :span="24">
          <div class="platformContainer blackComponents">
            <el-form :inline="true">
              <el-form-item>
                <el-button type="primary" size="small" @click="KeepOK" v-has="['设备保养工作']">保养完成</el-button>
              </el-form-item>
            </el-form>
            <el-table :data="KeepTaskTableData.data" border ref="multipleTableKeepTask" @selection-change="handleKeepTaskSelectionChange" @row-click="handleKeepTaskRowClick">
              <el-table-column type="selection"></el-table-column>
              <el-table-column v-for="(item,index) in KeepTaskTableData.column" :key="index" :prop="item.prop" :label="item.label"></el-table-column>
            </el-table>
            <div class="paginationClass">
              <el-pagination background  layout="total, sizes, prev, pager, next, jumper"
               :total="KeepTaskTableData.total"
               :current-page="KeepTaskTableData.offset"
               :page-sizes="[5,10,20]"
               :page-size="KeepTaskTableData.limit"
               @size-change="handleKeepTaskSizeChange"
               @current-change="handleKeepTaskCurrentChange">
              </el-pagination>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-col>
  </el-row>
</template>

<script>
  import tableView from '@/components/CommonTable'
  import TabControl from '@/components/TabControl'
  var moment = require('moment');
  export default {
    name: "IntelligentMaintenance",
    components:{tableView,TabControl},
    data(){
      return {
        TabControl:{
          TabControlCurrent:"",
          TabControlOptions:[
            {name:"设备台账"},
            {name:"设备维修任务"},
            {name:"设备保养任务"},
          ],
        },
        TableData:{
          tableName:"Equipment",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"EquipmentCode",label:"设备编码",type:"input",value:""},
            {prop:"Quantity",label:"数量",type:"input",value:""},
            {prop:"Power",label:"功率",type:"input",value:""},
            {prop:"Comment",label:"描述",type:"input",value:"",dataJudge:[]},
            {prop:"Status",label:"设备状态",type:"input",value:"",dataJudge:[{value:"维修中",color:"#228AD5"},{value:"待接单",color:"#FA7D00"},{value:"运行中",color:"#00FAE7"}]},
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          multipleSelection:[],
          tableSelection:true, //是否在第一列添加复选框
          tableSelectionRadio:false, //是否需要单选
          searchProp:"",
          searchVal:"",
          handleType:[
            {type:"warning",label:"快速报修",clickEvent:"repairs",hasPermissions:['设备报修']},
            {type:"primary",label:"制定保养计划",clickEvent:"drawUpKeepPlan",hasPermissions:['设备制定保养计划']},
            {type:"primary",label:"查看保养计划",clickEvent:"seeKeepPlan"},
          ],
          rowClick:"handleEQRowClick",
          rowClickData:{},
        },
        showLogTypeValue:"维修记录",
        showLogType:[
          {label:"维修记录"},
          {label:"保养记录"},
        ],
        repairsLogTableData:{ //维修记录表参数
          column:[
            {prop:"No",label:"工单号"},
            {prop:"EquipmentCode",label:"设备编码"},
            {prop:"ReceiveWorker",label:"维修人"},
            {prop:"Status",label:"工单状态"},
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          multipleSelection:[],
          tableSelection:true, //是否在第一列添加复选框
          tableSelectionRadio:true, //是否需要单选
        },
        RepairTableData:{  //维修任务表
          tableName:"repair",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"Status",label:"工单状态",type:"input",value:"",dataJudge:[{value:"待接单",color:"#FA7D00"},{value:"维修中",color:"#228AD5"}]},
            {prop:"No",label:"工单号",type:"input",value:""},
            {prop:"EquipmentCode",label:"设备编码",type:"input",value:""},
            {prop:"FaultExpound",label:"故障阐述",type:"input",value:"",searchProp:false},
            {prop:"Worker",label:"报修人",type:"input",value:""},
            {prop:"ApplyTime",label:"报修时间",type:"input",value:"",searchProp:false},
            {prop:"ReceiveWorker",label:"接单人",type:"input",value:"",searchProp:false},
            {prop:"ReceiveTime",label:"接单时间",type:"input",value:"",searchProp:false},
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
            {type:"primary",label:"我要接单",clickEvent:"takeOrder",hasPermissions:['设备维修工作']},
            {type:"success",label:"维修完成",clickEvent:"maintainOK",hasPermissions:['设备维修工作']},
          ],
        },
        showRepairsForm:false,
        faultCondition:"", //故障阐述内容
        showMaintainForm:false,
        showKeepPlanForm:false,
        KeepPlanEquipmentCode:"",
        KeepTaskTableData:{ //保养任务表参数
          column:[
            {prop:"Status",label:"工单状态"},
            {prop:"No",label:"工单号"},
            {prop:"EquipmentCode",label:"设备编码"},
            {prop:"Worker",label:"制定计划人"},
            {prop:"ApplyTime",label:"制定计划时间"},
            {prop:"StartTime",label:"任务开始时间"},
            {prop:"WorkTime",label:"工作截止时间"},
            {prop:"Describe",label:"计划描述"},
            {prop:"Content",label:"保养内容"},
            {prop:"WeekTime",label:"工作周期"},
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          multipleSelection:[],
        },
        keepTaskStartTime:moment().format("YYYY-MM-DD HH:ss:mm"),
        KeepTypeRadio:"周期",
        weekNumber:"",
        weekTime:"周",
        weekTimeType:[
          {label:"周",value:"周"},
          {label:"月",value:"月"},
          {label:"年",value:"年"},
        ],
        KeekPlanContent:"",
        keepLogTableData:{
          column:[
            {prop:"No",label:"工单号"},
            {prop:"EquipmentCode",label:"设备编码"},
            {prop:"Worker",label:"制定计划人"},
            {prop:"ApplyTime",label:"制定计划时间"},
            {prop:"StartTime",label:"任务开始时间"},
            {prop:"EndTime",label:"完成工作时间"},
            {prop:"Describe",label:"计划描述"},
            {prop:"Content",label:"保养内容"},
            {prop:"WeekTime",label:"工作周期"},
            {prop:"Status",label:"工单状态"},
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          multipleSelection:[],
        },
        KeepPlanTableData:{ //保养计划表参数
          column:[
            {prop:"No",label:"工单号"},
            {prop:"EquipmentCode",label:"设备编码"},
            {prop:"Worker",label:"制定计划人"},
            {prop:"ApplyTime",label:"制定计划时间"},
            {prop:"StartTime",label:"任务开始时间"},
            {prop:"WorkTime",label:"工作截止时间"},
            {prop:"Describe",label:"计划描述"},
            {prop:"WeekTime",label:"工作周期"},
          ],
          data:[],
        },
        keepPlandialogVisible:false,
      }
    },
    created(){
      this.getEQTable()
      this.getRepairTable()
      this.getKeepTaskTable()
    },
    mounted(){

    },
    watch:{

    },
    computed:{

    },
    methods: {
      getEQTable(){
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
      handleEQRowClick(){ //台账点击行事件
        var that = this
        var params = {
          limit:this.repairsLogTableData.limit,
          offset:this.repairsLogTableData.offset
        }
        this.axios.get("/api/record/"+this.TableData.rowClickData.EquipmentCode,{
          params: params
        }).then(res =>{
          if(res.data.code === "10001"){
            this.repairsLogTableData.data = res.data.data.rows
            this.repairsLogTableData.total = res.data.data.total
          }
        },res =>{
          console.log("请求错误")
        })
        var params1 = {
          limit:this.keepLogTableData.limit,
          offset:this.keepLogTableData.offset
        }
        this.axios.get("/api/keep_record/"+this.TableData.rowClickData.EquipmentCode,{
          params: params1
        }).then(res =>{
          if(res.data.code === "10001"){
            this.keepLogTableData.data = res.data.data.rows
            this.keepLogTableData.total = res.data.data.total
          }
        },res =>{
          console.log("请求错误")
        })
      },
      handleRepairsLogSelectionChange(val){ //选中维修记录
        this.repairsLogTableData.multipleSelection = val;
      },
      handleRepairsLogRowClick(row){ //点击维修记录行
        this.$refs.multipleTableRepairsLog.clearSelection();
        this.$refs.multipleTableRepairsLog.toggleRowSelection(row)
      },
      handleRepairsLogSizeChange(limit){
        this.repairsLogTableData.limit = limit
        this.getKeepTaskTable()
      },
      handleRepairsLogCurrentChange(offset){
        this.repairsLogTableData.offset = offset
        this.getKeepTaskTable()
      },
      seeMaintainForm(){ //查看维修单
        if(this.repairsLogTableData.multipleSelection.length === 1){
          this.showMaintainForm = true
        }else{
          this.$message({
            type: 'info',
            message: '请选择一项维修记录单'
          });
        }
      },
      repairs(){  //报修
        if(this.TableData.multipleSelection.length === 1){
          if(this.TableData.multipleSelection[0].Status === "运行中"){
            this.showRepairsForm = true
          }else{
            this.$message({
              type: 'info',
              message: '此设备已在维修流程中'
            });
          }
        }else{
          this.$message({
            type: 'info',
            message: '请选择一项需要报修的设备'
          });
        }
      },
      submitRepairs(){ //提交报修
        var that = this
        var params = {
          EquipmentCode: this.TableData.multipleSelection[0].EquipmentCode,
          FaultExpound:this.faultCondition,
          ApplyTime:moment().format("YYYY-MM-DD HH:mm:ss")
        }
        this.axios.post("/api/repair",this.qs.stringify(params)).then(res =>{
          if(res.data.code == 10000){
            this.$message({
              type: 'success',
              message: res.data.message
            });
            this.showRepairsForm = false
            this.getEQTable()
            this.getRepairTable()
          }else{
            this.$message({
              type: 'info',
              message: res.data.message
            });
          }
        },res =>{
          console.log("请求错误")
        })
      },
      drawUpKeepPlan(){ //制定保养计划
        if(this.TableData.multipleSelection.length != 0){
          this.showKeepPlanForm = true
          var EquipmentCodeArr = []
          this.TableData.multipleSelection.forEach(item =>{
            EquipmentCodeArr.push(item.EquipmentCode)
          })
          this.KeepPlanEquipmentCode = EquipmentCodeArr
        }else{
          this.$message({
            type: 'info',
            message: '请选择设备来制定保养计划'
          });
        }
      },
      submitKeekPlan(){ //提交保养计划
        var that = this
        var params = {
          EquipmentCode: this.KeepPlanEquipmentCode,
          StartTime:moment(this.keepTaskStartTime).format("YYYY-MM-DD HH:ss:mm"),
          ApplyTime:moment().format("YYYY-MM-DD HH:ss:mm"),
          Type:this.KeepTypeRadio,
          WeekTime:this.weekNumber + this.weekTime,
          Describe:this.KeekPlanContent
        }
        this.axios.post("/api/keep_plan",params).then(res =>{
          if(res.data.code == 10001){
            this.$message({
              type: 'success',
              message: res.data.message
            });
            this.showKeepPlanForm = false
            this.getEQTable()
            this.getKeepTaskTable()
          }else{
            this.$message({
              type: 'info',
              message: res.data.message
            });
          }
        },res =>{
          console.log("请求错误")
        })
      },
      seeKeepPlan(){  //查看设备保养计划
        if(this.TableData.multipleSelection.length === 1){
          this.KeepPlanTableData.data = []
          this.keepPlandialogVisible = true
          this.axios.get("/api/get_keep_plan/"+this.TableData.multipleSelection[0].EquipmentCode).then(res =>{
            if(res.data.code === "10001"){
              this.KeepPlanTableData.data = res.data.data
            }
          },res =>{
            console.log("请求错误")
          })
        }else{
          this.$message({
            type: 'info',
            message: '请选择一项设备查看保养计划'
          });
        }
      },
      getRepairTable(){ //获取维修任务表
        var that = this
        var params = {
          tableName: this.RepairTableData.tableName,
          limit:this.RepairTableData.limit,
          offset:this.RepairTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          var data = JSON.parse(res.data)
          that.RepairTableData.data = data.rows
          that.RepairTableData.total = data.total
        },res =>{
          console.log("请求错误")
        })
      },
      takeOrder(){ //接单
        if(this.RepairTableData.multipleSelection.length === 1){
          if(this.RepairTableData.multipleSelection[0].Status === "待接单"){
            this.$confirm('确定接收此维修任务？', '提示', {
              distinguishCancelAndClose:true,
              type: 'warning'
            }).then(()  => {
              var params =  {
                No:this.RepairTableData.multipleSelection[0].No,
                Time:moment().format("YYYY-MM-DD HH:mm:ss"),
                EquipmentCode:this.RepairTableData.multipleSelection[0].EquipmentCode
              }
              this.axios.patch("/api/repair_task/jiedan",this.qs.stringify(params)).then(res =>{
                if(res.data.code === "10001"){
                  this.$message({
                    type: 'success',
                    message: res.data.message
                  });
                  this.getEQTable()
                  this.getRepairTable()
                }else{
                  this.$message({
                    type: 'info',
                    message: res.data.message
                  });
                }
              },res =>{
                console.log("请求错误")
              })
            }).catch(() => {
              this.$message({
                type: 'info',
                message: '已取消接单'
              });
            });
          }else{
            this.$message({
              type: 'info',
              message: '此设备已在维修中'
            });
          }
        }else{
          this.$message({
            type: 'info',
            message: '请选择一条任务接单'
          });
        }
      },
      maintainOK(){
        if(this.RepairTableData.multipleSelection.length === 1){
          if(this.RepairTableData.multipleSelection[0].Status === "维修中"){
            this.$prompt('确定完成此维修任务？请输入维修内容', '提示', {
              confirmButtonText: '确定',
              cancelButtonText: '取消',
            }).then(({value})  => {
              var params = {
                  EquipmentCode:this.RepairTableData.multipleSelection[0].EquipmentCode,
                  No:this.RepairTableData.multipleSelection[0].No,
                  EndTime:moment().format("YYYY-MM-DD HH:mm:ss"),
                  Content:value
                }
              this.axios.patch("/api/repair_task/over",this.qs.stringify(params)).then(res =>{
                if(res.data.code === "10001"){
                  this.$message({
                    type: 'success',
                    message: res.data.message
                  });
                  this.getEQTable()
                  this.getRepairTable()
                }else{
                  this.$message({
                    type: 'info',
                    message: res.data.message
                  });
                }
              },res =>{
                console.log("请求错误")
              })
            }).catch(() => {
              this.$message({
                type: 'info',
                message: '已取消完成操作'
              });
            });
          }else{
            this.$message({
              type: 'info',
              message: '此项报修申请还未接单'
            });
          }
        }else{
          this.$message({
            type: 'info',
            message: '请选择一项任务完成维修'
          });
        }
      },
      getKeepTaskTable(){ //获取保养任务表
        var that = this
        var params = {
          limit:this.KeepTaskTableData.limit,
          offset:this.KeepTaskTableData.offset
        }
        this.axios.get("/api/keep_task",{
          params: params
        }).then(res =>{
          if(res.data.code === "10001"){
            this.KeepTaskTableData.data = res.data.data.rows
            this.KeepTaskTableData.total = res.data.data.total
          }
        },res =>{
          console.log("请求错误")
        })
      },
      handleKeepTaskSelectionChange(val){ //选中保养任务
        this.KeepTaskTableData.multipleSelection = val;
      },
      handleKeepTaskRowClick(row){ //点击保养任务行
        this.$refs.multipleTableKeepTask.clearSelection();
        this.$refs.multipleTableKeepTask.toggleRowSelection(row)
      },
      handleKeepTaskSizeChange(limit){
        this.KeepTaskTableData.limit = limit
        this.getKeepTaskTable()
      },
      handleKeepTaskCurrentChange(offset){
        this.KeepTaskTableData.offset = offset
        this.getKeepTaskTable()
      },
      KeepOK(){ //保养完成
        if(this.KeepTaskTableData.multipleSelection.length === 1){
          this.$prompt('确定完成此保养任务？请输入保养内容', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
          }).then(({value})  => {
            var params = {
                No:this.KeepTaskTableData.multipleSelection[0].No,
                EndTime:moment().format("YYYY-MM-DD HH:mm:ss"),
                Content:value
              }
            this.axios.post("/api/keep_task",this.qs.stringify(params)).then(res =>{
              if(res.data.code === "10001"){
                this.$message({
                  type: 'success',
                  message: res.data.message
                });
                this.getEQTable()
                this.getKeepTaskTable()
              }else{
                this.$message({
                  type: 'info',
                  message: res.data.message
                });
              }
            },res =>{
              console.log("请求错误")
            })
          }).catch(() => {
            this.$message({
              type: 'info',
              message: '已取消完成操作'
            });
          });
        }else{
          this.$message({
            type: 'info',
            message: '请选择一项保养任务'
          });
        }
      },
      getKeepLogTable(){ //点击保养记录表

      },
      handleKeepLogSelectionChange(val){ //选中保养记录
        this.keepLogTableData.multipleSelection = val;
      },
      handleKeepLogRowClick(row){ //点击保养记录行
        this.$refs.multipleTableKeepLog.clearSelection();
        this.$refs.multipleTableKeepLog.toggleRowSelection(row)
      },
      handleKeepLogSizeChange(limit){
        this.keepLogTableData.limit = limit
        this.getKeepLogTable()
      },
      handleKeepLogCurrentChange(offset){
        this.keepLogTableData.offset = offset
        this.getKeepLogTable()
      },
    }
  }
</script>
<style>

</style>
