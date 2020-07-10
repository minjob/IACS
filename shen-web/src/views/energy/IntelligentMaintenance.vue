<template>
  <el-row :gutter="15">
    <el-col :span="24">
      <TabControl :TabControl="TabControl"></TabControl>
      <el-row :gutter="15" v-if="TabControl.TabControlCurrent === '设备台账'">
        <el-col :span="24" v-if="!showRepairsForm && !showMaintainForm">
          <div class="platformContainer">
            <tableView class="blackComponents" :tableData="TableData" @getTableData="getEQTable" @repairs="repairs" @handleEQRowClick="handleEQRowClick"></tableView>
          </div>
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
          <div class="platformContainer" v-if="showLogTypeValue === '保养记录'">

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
      </el-row>
      <el-row :gutter="15" v-if="TabControl.TabControlCurrent === '设备维修任务'">
        <el-col :span="24">
          <div class="platformContainer">
            <tableView class="blackComponents" :tableData="RepairTableData" @getTableData="getRepairTable" @takeOrder="takeOrder" @maintainOK="maintainOK"></tableView>
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
            {prop:"Comment",label:"描述",type:"input",value:""},
            {prop:"Status",label:"设备状态",type:"input",value:"",dataJudge:[{value:"维修中",color:"#228AD5"},{value:"待接单",color:"#FA7D00"},{value:"运行中",color:"#00FAE7"}]},
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
            {type:"warning",label:"快速报修",clickEvent:"repairs"},
            {type:"primary",label:"下发保养任务"},
            {type:"primary",label:"制定保养计划"},
          ],
          rowClick:"handleEQRowClick"
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
            {type:"primary",label:"我要接单",clickEvent:"takeOrder"},
            {type:"success",label:"维修完成",clickEvent:"maintainOK"},
          ],
        },
        showRepairsForm:false,
        faultCondition:"", //故障阐述内容
        showMaintainForm:false,
      }
    },
    created(){
      this.getEQTable()
      this.getRepairTable()
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
          offset:this.repairsLogTableData.offset - 1
        }
        this.axios.get("/api/record/"+this.TableData.multipleSelection[0].EquipmentCode,{
          params: params
        }).then(res =>{
          if(res.data.code === "10001"){
            this.repairsLogTableData.data = res.data.data.rows
            this.repairsLogTableData.total = res.data.data.total
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
      },
      handleRepairsLogCurrentChange(offset){
        this.repairsLogTableData.offset = offset
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
        this.axios.post("/api/repair",{
          params: params
        }).then(res =>{
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
              this.axios.patch("/api/repair_task/jiedan",{
                params: {
                  No:this.RepairTableData.multipleSelection[0].No,
                  Time:moment().format("YYYY-MM-DD HH:mm:ss"),
                  EquipmentCode:this.RepairTableData.multipleSelection[0].EquipmentCode
                }
              }).then(res =>{
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
              this.axios.patch("/api/repair_task/over",{
                params: {
                  EquipmentCode:this.RepairTableData.multipleSelection[0].EquipmentCode,
                  No:this.RepairTableData.multipleSelection[0].No,
                  EndTime:moment().format("YYYY-MM-DD HH:mm:ss"),
                  Content:value
                }
              }).then(res =>{
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
      }
    }
  }
</script>
<style>
 .second-header{
    background-color: skyblue;
    height: 57px;
    width:100%;
    background:rgba(52,56,62,1);
    border-radius:4px;
  }
.home-container{
  background-color: #1B1E27;
}
.mainshow{
    width: 100%;
    height: 100%;
}
.mainshow img{
    width: 100%;
    height: 100%;
}
</style>
