<template>
  <el-row :gutter="20">
    <el-col :span="24">
      <el-col :span="24">
        <div class="page-title">
          <span style="margin-left: 10px;" class="text-size-normol">工作日历</span>
        </div>
      </el-col>
      <el-col :span="24">
        <el-form :inline="true" class="blackComponents" v-has="['管理工作日历']">
          <el-form-item label="选择月份：">
            <el-date-picker type="month" v-model="scheduleMonth" size="mini" style="width: 180px;" :clearable="false"></el-date-picker>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="mini" @click="addscheduledates">生成计划日程</el-button>
          </el-form-item>
        </el-form>
      </el-col>
      <el-col :span="5">
        <div class="scheduleContainer" style="height: 730px;">
          <div id='external-events' class="marginBottom">
            <h4>可拖放的日程</h4>
            <a class='fc-event' v-for="item in scheduleTableData.data" style="padding: 5px;margin: 10px 0;cursor: pointer;" :color="item.color" :style="{ background:item.color,border:'1px solid ' +item.color }">{{item.DateTypeName}}</a>
          </div>
          <el-popover
            placement="right"
            width="800"
            trigger="click">
            <tableView :tableData="scheduleTableData" @getTableData="getScheduleTableData"></tableView>
            <el-button slot="reference" size="mini" class="floatRight">日程管理</el-button>
          </el-popover>
        </div>
      </el-col>
      <el-col :span="19">
        <div class="platformContainer blackComponents">
          <FullCalendar :plugins="calendarPlugins"
                        :droppable="true"
                        locale="zh-cn"
                        :header="header"
                        :events="events"
                        :editable="true"
                        :selectable="true"
                        :button-text="buttonText"
                        @dateClick="handleDateClick"
                        @eventClick="handleEventClick"
                        @eventDrop="handleEventDrop"
                        @drop="drop"
          />
        </div>
      </el-col>
    </el-col>
  </el-row>
</template>

<script>
  import tableView from '@/components/CommonTable'
  import FullCalendar from '@fullcalendar/vue'
  import dayGridPlugin from "@fullcalendar/daygrid";
  import timeGridPlugin from "@fullcalendar/timegrid";
  import interactionPlugin, { Draggable } from "@fullcalendar/interaction";
  import '@fullcalendar/core/main.css';
  import '@fullcalendar/daygrid/main.css';
  import '@fullcalendar/timegrid/main.css';
  var moment = require('moment');
  export default {
    components:{tableView,FullCalendar},
    name: "IntelligentOperation",
    data(){
      return {
        scheduleTableData:{
          tableName:"scheduledatetype",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {label:"类型编码",prop:"DateTypeCode",type:"input",value:""},
            {label:"类型名称",prop:"DateTypeName",type:"input",value:""},
            {label:"注释",prop:"Desc",type:"input",value:""},
            {label:"颜色",prop:"color",type:"input",value:"",searchProp:false},
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          searchProp:"",
          tableSelection:true, //是否在第一列添加复选框
          tableSelectionRadio:false, //是否需要单选
          searchVal:"",
          multipleSelection: [],
          dialogVisible: false,
          dialogTitle:'',
          handleType:[
            {type:"primary",label:"添加",hasPermissions:['管理工作日历']},
            {type:"warning",label:"修改",hasPermissions:['管理工作日历']},
            {type:"danger",label:"删除",hasPermissions:['管理工作日历']},
          ],
        },
        calendarPlugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
        events:[],
        buttonText:{
          today:'今天',
          month: '月',
          week: '周',
          day: '天'
        },
        header:{
          left:'prev,next today',
          center:'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        scheduleMonth:moment().format("YYYY-MM"),

      }
    },
    created(){

    },
    mounted(){
      this.getScheduleTableData()
      this.getScheduling()
      new Draggable(document.getElementById("external-events"), {
        itemSelector: '.fc-event',
        eventData: function(eventEl) {
          return {
            title: eventEl.innerText,
            duration: '02:00'
          };
        }
      });

    },
    watch:{

    },
    computed:{

    },
    methods: {
      getScheduleTableData(){ //获取日程表
        var that = this
        var params = {
          tableName: this.scheduleTableData.tableName,
          limit:this.scheduleTableData.limit,
          offset:this.scheduleTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          var data = JSON.parse(res.data)
          that.scheduleTableData.data = data.rows
          that.scheduleTableData.total = data.total
        })
      },
      getScheduling(){  //获取日历所有日程
        let that = this
        that.axios.get("/api/CUID",{
          params: {
            tableName: "scheduledate",
            limit:100000000,
            offset:0
          }
        }).then(res =>{
          var data = JSON.parse(res.data)
          that.events = []
          data.rows.forEach(item =>{
            that.events.push({
              ID:item.ID,
              title:item.DateType,
              color:item.color,
              start:item.WorkDate
            })
          })
        })
      },
      drop(e){
        let that = this
        var params = {
          tableName: "scheduledate",
          DateType:e.draggedEl.innerText,
          WorkDate:e.dateStr,
          color:e.draggedEl.attributes.color.value
        }
        that.axios.post("/api/CUID",that.qs.stringify(params)).then(res =>{
          if(res.data == "OK"){
            that.$message({
              showClose: true,
              type: 'success',
              message: "添加成功"
            });
            that.getScheduling()
          }else{
            that.$message({
              type: 'info',
              message: res.data
            });
          }
        })
      },
      handleDateClick(e) {  //点击日期

      },
      handleEventClick(e){  //点击日历里的日程 进行删除
        let that = this
        var ID = {
          id:e.event.extendedProps.ID
        }
        that.$confirm('此操作将永久删除该日程, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          that.axios.delete("/api/CUID",{
            params: {
              tableName: "scheduledate",
              delete_data:JSON.stringify(ID),
            }
          }).then(res =>{
            if(res.data == "OK"){
              that.$message({
                type: 'success',
                message: '删除成功!'
              });
              that.getScheduling()
            }
          },res =>{
            console.log("请求错误")
          })
        }).catch(() => {
          that.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      },
      handleEventDrop(e){ //日历里拖拽换位日程 进行修改
        let that = this
        var startDate = moment(e.event.start).format('YYYY-MM-DD')
        var params = {
          tableName: "scheduledate",
          ID:e.event.extendedProps.ID,
          DateType:e.event.title,
          WorkDate:startDate,
          color:e.event.backgroundColor
        }
        that.axios.put("/api/CUID",that.qs.stringify(params)).then(res =>{
          if(res.data == "OK"){
            that.$message({
              showClose: true,
              type: 'success',
              message: '修改成功'
            });
            that.getScheduling()
          }else{
            that.$message({
              type: 'info',
              message: res.data
            });
          }
        })
      },
      addscheduledates(){
        let that = this
        that.$confirm('此操作将一次生成'+ moment(that.scheduleMonth).format("YYYY-MM") +'的工作日程, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          that.axios.get("/api/addscheduledates",{
            params: {
              month: moment(that.scheduleMonth).format("YYYY-MM"),
            }
          }).then(res =>{
            if(res.data == "OK"){
              that.$message({
                type: 'success',
                message: '生成成功'
              });
              that.getScheduling()
            }
          },res =>{
            console.log("请求错误")
          })
        }).catch(() => {
          that.$message({
            type: 'info',
            message: '已取消生成'
          });
        });
      }
    }
  }
</script>
<style>

</style>
