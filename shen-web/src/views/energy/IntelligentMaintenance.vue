<template>
  <el-row :gutter="15">
    <el-col :span="24">
      <TabControl :TabControl="TabControl"></TabControl>
      <el-row :gutter="15" v-if="TabControl.TabControlCurrent === '设备台账'">
        <el-col :span="24" v-if="!showRepairsForm">
          <div class="platformContainer">
            <tableView class="blackComponents" :tableData="TableData" @getTableData="getEQTable" @repairs="repairs"></tableView>
          </div>
          <el-form :inline="true" class="marginBottom">
            <el-radio-group v-model="showLogTypeValue" size="mini" :border="false" fill="#00CAFA">
              <el-radio-button v-for="item in showLogType" :key="item.label" :label="item.label"></el-radio-button>
            </el-radio-group>
          </el-form>
          <div class="platformContainer" v-if="showLogTypeValue === '维修记录'">
            <tableView class="blackComponents" :tableData="repairsLogTableData" @getTableData="getRepairsLogTable"></tableView>
          </div>
        </el-col>
        <el-col :span="24" v-if="showRepairsForm">
          <el-button @click="showRepairsForm = false" icon="el-icon-back" size="small" class="marginBottom">返回列表</el-button>
          <div class="platformContainer blackComponents">
            <el-divider>设备报修信息</el-divider>
            <table class="elementTable marginBottom">
              <tr>
                <td>设备编码：{{ TableData.multipleSelection[0].EquipmentCode }}</td>
                <td>设备名称：{{ TableData.multipleSelection[0].name }}</td>
              </tr>
              <tr>
                <td colspan="4"><p class="marginBottom">故障阐述：</p><el-input type="textarea" v-model="faultCondition"></el-input></td>
              </tr>
            </table>
            <el-button @click="submitRepairs" type="primary" size="small">提交报修信息</el-button>
          </div>
        </el-col>
      </el-row>
      <el-row :gutter="15" v-if="TabControl.TabControlCurrent === '设备维修任务'">
        <el-col :span="24">
          <div class="platformContainer">
            <tableView class="blackComponents" :tableData="RepairTableData" @getTableData="getRepairTable"></tableView>
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
            {prop:"name",label:"设备名称",type:"input",value:""},
            {prop:"Quantity",label:"数量",type:"input",value:""},
            {prop:"Power",label:"功率",type:"input",value:""},
            {prop:"Comment",label:"描述",type:"input",value:""},
            {prop:"Status",label:"设备状态",type:"input",value:""},
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
        },
        showLogTypeValue:"维修记录",
        showLogType:[
          {label:"维修记录"},
          {label:"保养记录"},
        ],
        repairsLogTableData:{
          tableName:"Equipment",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"EquipmentCode",label:"设备编码",type:"input",value:""},
            {prop:"name",label:"设备名称",type:"input",value:""},
            {prop:"Quantity",label:"数量",type:"input",value:""},
            {prop:"Power",label:"功率",type:"input",value:""},
            {prop:"Comment",label:"描述",type:"input",value:""},
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

          ],
          relatedTableField:"TableName",  //点击行的字段
          relatedChildTableField:"TableName",  //关联子表的字段搜索值
        },
        RepairTableData:{
          tableName:"Repair",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"Status",label:"工单状态",type:"input",value:"",dataJudge:[{value:"待接单",color:"#FA7D00"},{value:"维修中",color:"#00FAE7"}]},
            {prop:"No",label:"工单号",type:"input",value:""},
            {prop:"EquipmentCode",label:"设备编码",type:"input",value:""},
            {prop:"name",label:"设备名称",type:"input",value:""},
            {prop:"model",label:"设备型号",type:"input",value:""},
            {prop:"Area",label:"区域",type:"input",value:""},
            {prop:"FaultExpound",label:"故障阐述",type:"input",value:"",searchProp:false},
            {prop:"Worker",label:"报修人",type:"input",value:""},
            {prop:"ApplyTime",label:"报修时间",type:"input",value:"",searchProp:false},
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
            {type:"warning",label:"我要接单"},
          ],
        },
        showRepairsForm:false,
        faultCondition:"", //故障阐述内容
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
      getRepairsLogTable(){ //根据台账搜索维修记录表
        var that = this
        var params = {
          tableName: this.repairsLogTableData.tableName,
          limit:this.repairsLogTableData.limit,
          offset:this.repairsLogTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          var data = JSON.parse(res.data)
          that.repairsLogTableData.data = data.rows
          that.repairsLogTableData.total = data.total
        },res =>{
          console.log("请求错误")
        })
      },
      repairs(){  //报修
        if(this.TableData.multipleSelection.length === 1){
          this.showRepairsForm = true
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
          Name:this.TableData.multipleSelection[0].Name,
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
