<template>
  <el-row :gutter="15">
    <el-col :span="24">
      <TabControl :TabControl="TabControl"></TabControl>
      <el-row v-if="TabControl.TabControlCurrent === '冷却塔运行策略'">
        <el-col :span="24">
          <div class="platformContainer blackComponents">
            <tableView :tableData="EnergyStrategyTableData" @getTableData="getScheduleTableData" @getSchedulelqtTableData="getSchedulelqtTableData"></tableView>
          </div>
          <div class="platformContainer blackComponents">
            <el-row :gutter="15">
              <el-col :span="20">
                <el-form :inline="true" class="blackComponents">
                  <el-form-item>
                    <el-button type="primary" size="small" @click="add">添加</el-button>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="warning" size="small" @click="edit">修改</el-button>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="danger" size="small" @click="del">删除</el-button>
                  </el-form-item>
                </el-form>
                <tableView :tableData="SchedulelqtTableData" @getTableData="getSchedulelqtTableData"></tableView>
                <el-dialog :title="SchedulelqtTableData.dialogTitleSchedule" :visible.sync="SchedulelqtTableData.dialogVisibleSchedule" :close-on-click-modal="false" :append-to-body="true" width="40%">
                  <el-form :model="SchedulelqtTableData.form" label-width="110px">
                    <el-form-item label="ID">
                      <el-input v-model="SchedulelqtTableData.form.ID" :disabled="true"></el-input>
                    </el-form-item>
                    <el-form-item label="编号">
                      <el-input v-model="SchedulelqtTableData.form.energystrategyCode" :disabled="true"></el-input>
                    </el-form-item>
                    <el-form-item label="开始时间">
                      <el-time-picker v-model="SchedulelqtTableData.form.enablestarttime" value-format="HH:mm:ss"></el-time-picker>
                    </el-form-item>
                    <el-form-item label="结束时间">
                      <el-time-picker v-model="SchedulelqtTableData.form.enableendtime" value-format="HH:mm:ss"></el-time-picker>
                    </el-form-item>
                    <el-form-item label="冷却塔1">
                      <el-select v-model="SchedulelqtTableData.form.lqt1_allowrun">
                        <el-option label="开启" value="1"></el-option>
                        <el-option label="关闭" value="0"></el-option>
                      </el-select>
                    </el-form-item>
                    <el-form-item label="冷却塔2">
                      <el-select v-model="SchedulelqtTableData.form.lqt2_allowrun">
                        <el-option label="开启" value="1"></el-option>
                        <el-option label="关闭" value="0"></el-option>
                      </el-select>
                    </el-form-item>
                    <el-form-item label="说明">
                      <el-input v-model="SchedulelqtTableData.form.comment" placeholder="请输入内容"></el-input>
                    </el-form-item>
                  </el-form>
                  <span slot="footer" class="dialog-footer">
                    <el-button @click="SchedulelqtTableData.dialogVisible = false">取 消</el-button>
                    <el-button type="primary" @click="saveSchedulelqt">保存</el-button>
                  </span>
                </el-dialog>
              </el-col>
              <el-col :span="4">
                <el-timeline>
                  <el-timeline-item v-for="(activity, index) in SchedulelqtTimeLine" :key="index" :timestamp="activity.time" placement="top">
                    <p>{{ activity.label }}</p>
                    <p>
                      <span v-if="activity.lqt1 === '1'">冷却塔1<span class="color-success">开启</span></span>
                      <span v-if="activity.lqt1 === '0'">冷却塔1<span class="color-grayblack">关闭</span></span>
                      <span v-if="activity.lqt2 === '1'">冷却塔2<span class="color-success">开启</span></span>
                      <span v-if="activity.lqt2 === '0'">冷却塔2<span class="color-grayblack">关闭</span></span>
                    </p>
                  </el-timeline-item>
                </el-timeline>
              </el-col>
            </el-row>
          </div>
        </el-col>
      </el-row>
    </el-col>
  </el-row>
</template>

<script>
  import TabControl from '@/components/TabControl'
  import tableView from '@/components/CommonTable'
  var moment = require('moment');
  export default {
    name: "IntelligentModel",
    components:{TabControl,tableView},
    data(){
      return {
        TabControl:{
          TabControlCurrent:"",
          TabControlOptions:[
            {name:"冷却塔运行策略"},
          ],
        },
        EnergyStrategyTableData:{
          tableName:"EnergyStrategy",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {label:"编号",prop:"Code",type:"input",value:""},
            {label:"启用标志",prop:"UseFlag",type:"input",value:""},
            {label:"类型",prop:"type",type:"input",value:""},
            {label:"说明",prop:"Comment",type:"input",value:"",showField:false,searchProp:false},
            {label:"创建时间",prop:"CreateTime",type:"input",value:"",searchProp:false},
            {label:"创建人",prop:"CreatePerson",type:"input",value:"",searchProp:false},
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          searchProp:"",
          tableSelection:true, //是否在第一列添加复选框
          tableSelectionRadio:true, //是否需要单选
          searchVal:"",
          multipleSelection: [],
          dialogVisible: false,
          dialogTitle:'',
          handleType:[
            // {type:"primary",label:"启用",hasPermissions:['管理工作日历']},
            // {type:"primary",label:"不启用",hasPermissions:['管理工作日历']},
          ],
          rowClick:"getSchedulelqtTableData",
          rowClickData:{},
        },
        SchedulelqtTableData:{
          tableName:"Schedulelqt",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {label:"开始时间",prop:"enablestarttime",type:"input",value:""},
            {label:"结束时间",prop:"enableendtime",type:"input",value:""},
            {label:"编号",prop:"energystrategyCode",type:"input",value:""},
            {label:"冷却塔1",prop:"lqt1_allowrun",type:"input",value:"",dataJudge:[{value:"1",change:"开启"},{value:"0",change:"关闭"}]},
            {label:"冷却塔2",prop:"lqt2_allowrun",type:"input",value:"",dataJudge:[{value:"1",change:"开启"},{value:"0",change:"关闭"}]},
            {label:"说明",prop:"comment",type:"input",value:"",searchProp:false},
          ],
          data:[],
          tableSelection:true, //是否在第一列添加复选框
          tableSelectionRadio:true, //是否需要单选
          multipleSelection: [],
          dialogVisibleSchedule: false,
          dialogTitleSchedule:'',
          form:{
            tableName:"Schedulelqt",
            energystrategyCode:"",
            enablestarttime:"",
            enableendtime:"",
            lqt1_allowrun:"",
            lqt2_allowrun:"",
            comment:"",
          },
          handleType:[

          ],
        },
        SchedulelqtTimeLine:[],
      }
    },
    created(){
      this.getScheduleTableData()
    },
    mounted(){

    },
    watch:{

    },
    computed:{

    },
    methods: {
      getScheduleTableData(){
        var that = this
        var params = {
          tableName: this.EnergyStrategyTableData.tableName,
          limit:this.EnergyStrategyTableData.limit,
          offset:this.EnergyStrategyTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          var data = JSON.parse(res.data)
          that.EnergyStrategyTableData.data = data.rows
          that.EnergyStrategyTableData.total = data.total
        })
      },
      getSchedulelqtTableData(){
        var that = this
        var params = {
          code:this.EnergyStrategyTableData.rowClickData.Code,
        }
        this.axios.get("/api/schedule_lqt",{
          params: params
        }).then(res =>{
          that.SchedulelqtTableData.data = res.data.data
          that.SchedulelqtTimeLine = []
          that.SchedulelqtTableData.data.forEach(item =>{
            that.SchedulelqtTimeLine.push(
              {time:item.enablestarttime,label:"开始时间",lqt1:item.lqt1_allowrun,lqt2:item.lqt2_allowrun},
              {time:item.enableendtime,label:"结束时间",lqt1:item.lqt1_allowrun,lqt2:item.lqt2_allowrun},
            )
          })
        },res =>{
          console.log("请求错误")
        })
      },
      add(){
        if(this.EnergyStrategyTableData.multipleSelection.length === 1) {
          this.SchedulelqtTableData.dialogVisibleSchedule = true
          this.SchedulelqtTableData.dialogTitleSchedule = "添加"
          this.SchedulelqtTableData.form = {
            ID: "",
            energystrategyCode: this.EnergyStrategyTableData.rowClickData.Code,
            enablestarttime: moment().format("HH:mm:ss"),
            enableendtime: moment().format("HH:mm:ss"),
            lqt1_allowrun: "1",
            lqt2_allowrun: "1",
            comment: "",
          }
        }else{
          this.$message({
            type: 'info',
            message: '请单选一条日程类型 '
          })
        }
      },
      edit(){
        if(this.SchedulelqtTableData.multipleSelection.length === 1) {
          this.SchedulelqtTableData.dialogVisibleSchedule = true
          this.SchedulelqtTableData.dialogTitleSchedule = "修改"
          this.SchedulelqtTableData.form = {
            ID: this.SchedulelqtTableData.multipleSelection[0].ID,
            energystrategyCode: this.SchedulelqtTableData.multipleSelection[0].energystrategyCode,
            enablestarttime: this.SchedulelqtTableData.multipleSelection[0].enablestarttime,
            enableendtime: this.SchedulelqtTableData.multipleSelection[0].enableendtime,
            lqt1_allowrun: this.SchedulelqtTableData.multipleSelection[0].lqt1_allowrun,
            lqt2_allowrun: this.SchedulelqtTableData.multipleSelection[0].lqt2_allowrun,
            comment: this.SchedulelqtTableData.multipleSelection[0].comment,
          }
        }else{
          this.$message({
            type: 'info',
            message: '请单选一条数据 '
          })
        }
      },
      saveSchedulelqt(){
        var enablestarttime = moment().format("YYYY-MM-DD ") + this.SchedulelqtTableData.form.enablestarttime
        var enableendtime =  moment().format("YYYY-MM-DD ") + this.SchedulelqtTableData.form.enableendtime
        if(moment(enableendtime).diff(moment(enablestarttime),"hours") > 0){
          if(this.SchedulelqtTableData.dialogTitleSchedule === "添加"){
            var params = {
              start_time:this.SchedulelqtTableData.form.enablestarttime,
              end_time:this.SchedulelqtTableData.form.enableendtime,
              comment:this.SchedulelqtTableData.form.comment,
              energystrategyCode:this.SchedulelqtTableData.form.energystrategyCode,
              lqt1:this.SchedulelqtTableData.form.lqt1_allowrun,
              lqt2:this.SchedulelqtTableData.form.lqt2_allowrun,
            }
            this.axios.post("/api/schedule_lqt",this.qs.stringify(params)).then(res =>{
              if(res.data.code === "20001"){
                this.$message({
                  type: 'success',
                  message: res.data.message
                });
                this.getSchedulelqtTableData()
              }else if(res.data.code === "20003"){
                this.$message({
                  type: 'info',
                  message: res.data.message
                });
              }
              this.SchedulelqtTableData.dialogVisibleSchedule = false
            },res =>{
              console.log("请求错误")
            })
          }else if(this.SchedulelqtTableData.dialogTitleSchedule === "修改"){
            var params = {
              ID:this.SchedulelqtTableData.form.ID,
              start_time:this.SchedulelqtTableData.form.enablestarttime,
              end_time:this.SchedulelqtTableData.form.enableendtime,
              comment:this.SchedulelqtTableData.form.comment,
              energystrategyCode:this.SchedulelqtTableData.form.energystrategyCode,
              lqt1:this.SchedulelqtTableData.form.lqt1_allowrun,
              lqt2:this.SchedulelqtTableData.form.lqt2_allowrun,
            }
            this.axios.put("/api/schedule_lqt",this.qs.stringify(params)).then(res =>{
              if(res.data.code === "20001"){
                this.$message({
                  type: 'success',
                  message: res.data.message
                });
                this.SchedulelqtTableData.dialogVisibleSchedule = false
                this.getSchedulelqtTableData()
              }else if(res.data.code === "20003"){
                this.$message({
                  type: 'info',
                  message: res.data.message
                });
              }
            },res =>{
              console.log("请求错误")
            })
          }
        }else{
          this.$message({
            type: 'info',
            message: '结束时间必须比开始时间大于一小时 '
          })
        }
      },
      del(){
        if(this.SchedulelqtTableData.multipleSelection.length > 0) {
          var mulId = []
          this.SchedulelqtTableData.multipleSelection.forEach(item =>{
            mulId.push(item.ID);
          })
          var params = {
            ID:mulId.join(",")
          }
          this.$confirm('确定删除所选记录？', '提示', {
            distinguishCancelAndClose:true,
            type: 'warning'
          }).then(()  => {
            this.axios.delete("/api/schedule_lqt",{params: params}).then(res =>{
              if(res.data.code === "20001"){
                this.$message({
                  type: 'success',
                  message: res.data.message
                });
              }
              this.getSchedulelqtTableData()
            },res =>{
              console.log("请求错误")
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
            message: '请选择要删除的数据 '
          })
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
