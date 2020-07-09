<template>
  <el-row :gutter="15">
    <el-col :span="24">
      <TabControl :TabControl="TabControl"></TabControl>
      <el-row :gutter="15" v-if="TabControl.TabControlCurrent === '设备台账'">
        <el-col :span="24" v-if="!showRepairsForm">
          <div class="platformContainer">
            <tableView class="blackComponents" :tableData="TableData" @getTableData="getRoleTable" @repairs="repairs"></tableView>
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
                <td>设备型号：{{ TableData.multipleSelection[0].Model }}</td>
                <td>区域：{{ TableData.multipleSelection[0].区域 }}</td>
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
            {name:"维修记录"},
            {name:"设备保养任务"},
            {name:"保养记录"},
          ],
        },
        TableData:{
          tableName:"Equipment",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"EquipmentCode",label:"设备编码",type:"input",value:""},
            {prop:"name",label:"设备名称",type:"input",value:""},
            {prop:"model",label:"设备型号",type:"input",value:""},
            {prop:"Quantity",label:"数量",type:"input",value:""},
            {prop:"Power",label:"功率",type:"input",value:""},
            {prop:"Area",label:"区域",type:"input",value:""},
            {prop:"Manufacturer",label:"生产商",type:"input",value:""},
            {prop:"Sap",label:"SAP号",type:"input",value:""},
            {prop:"FixedAssetsNo",label:"固定资产编号",type:"input",value:""},
            {prop:"FixedAssetsName",label:"固定资产名称",type:"input",value:""},
            {prop:"IntoTime",label:"开始运行日期",type:"input",value:""},
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
        showRepairsForm:false,
        faultCondition:"", //故障阐述内容
      }
    },
    created(){
      this.getRoleTable()
    },
    mounted(){

    },
    watch:{

    },
    computed:{

    },
    methods: {
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
          EquipmentCode: this.TableData.multipleSelection.EquipmentCode,
          Name:this.TableData.multipleSelection.Name,
          Model:this.TableData.multipleSelection.Model,
          Area:this.TableData.multipleSelection.Area,
          FaultExpound:this.faultCondition,
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
          }else{
            this.$message({
              type: 'info',
              message: res.data.message
            });
          }
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
