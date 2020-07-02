<template>
  <el-row :gutter="20">
    <el-col :span="24">
      <el-col :span="24">
        <div class="page-title">
          <span style="margin-left: 10px;" class="text-size-normol">工作日历</span>
        </div>
      </el-col>
      <el-col :span="5">
        <div class="scheduleContainer" style="height: 730px;">
          <div id='external-events' class="itemMarginBottom">
            <h4>可拖放的日程</h4>
            <div id="fcEvent">
              <draggable v-model="scheduleTableData.data" :move="getdata" >
                <transition-group>
                  <a class='fc-event' v-for="item in scheduleTableData.data" style="padding: 5px;margin: 10px 0;cursor: pointer;" :style="{ background:item.color }">{{item.DateTypeName}}</a>
                </transition-group>
              </draggable>
            </div>
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
        <div class="platformContainer">
          <FullCalendar :plugins="calendarPlugins"
            locale="zh-cn"
            :header="header"
            :events="events"
            :editable="true"
            :selectable="true"
            :button-text="buttonText"
            @dateClick="handleDateClick"
            @eventClick="handleEventClick"
            @eventDrop="handleEventDrop"
            @eventResize="handleEventResize"
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
  import interactionPlugin from "@fullcalendar/interaction";
  import '@fullcalendar/core/main.css';
  import '@fullcalendar/daygrid/main.css';
  import '@fullcalendar/timegrid/main.css';
  import draggable from 'vuedraggable'
  var moment = require('moment');
  export default {
    name: "Calendar",
    components:{tableView,FullCalendar,draggable},
    data(){
      return {
        scheduleTableData:{
          tableName:"scheduledatetype",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {label:"类型编码",prop:"DateTypeCode",type:"input",value:"",showField:true,searchProp:true},
            {label:"类型名称",prop:"DateTypeName",type:"input",value:"",showField:true,searchProp:true},
            {label:"注释",prop:"Desc",type:"input",value:"",showField:true,searchProp:true},
            {label:"颜色",prop:"color",type:"input",value:"",showField:true,searchProp:false},
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
            {type:"primary",label:"添加"},
            {type:"warning",label:"修改"},
            {type:"danger",label:"删除"},
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
      }
    },
    created(){

    },
    mounted() {
      this.getScheduleTableData()
      this.getScheduling()
    },
    methods:{
      getdata(e){
        console.log(e)
      },
      getScheduleTableData(){ //渲染
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
      getScheduling(){
        this.axios.get("/api/CUID",{
          params: {
            tableName: "scheduledate",
            limit:100000000,
            offset:0
          }
        }).then(res =>{
          var data = JSON.parse(res.data)
          this.events = data.rows
        })
          // $("#fcEvent").html("")
          // that.scheduleTableData.data.forEach(item =>{
          //   $("#fcEvent").append(`<a class='fc-event' style="padding: 5px;border:1px solid ${item.color};background:${item.color};margin: 10px 0;cursor: pointer;">${item.DateTypeName}</a>`)
          // })
          // $('#fcEvent .fc-event').each(function () {
          //   $(this).data('event', {
          //     title: $.trim($(this).text()), // use the element's text as the event title
          //     stick: false // 拖动后不固定显示在日历上
          //   });
          //   // 使事件可拖放
          //   $(this).draggable({
          //     zIndex: 999,
          //     revert: true,
          //     revertDuration: 0  //拖动后的原始位置
          //   });
          // });
        //   $('#fullcalendar').fullCalendar({
        //     header: {
        //       right: 'prev,next today',
        //       center: 'title',
        //       left: 'month,agendaWeek,agendaDay,listMonth'
        //     },
        //     buttonText: {
        //       today: '今天',
        //       month: '月',
        //       week: '周',
        //       day: '日',
        //       list:'日程'
        //     },
        //     monthNames: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
        //     monthNamesShort: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
        //     dayNames: ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"],
        //     dayNamesShort: ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"],
        //     editable: true, //支持拖动换位
        //     navLinks: true, //是否可以单击日/周名称来导航视图
        //     weekNumbers: true, //是否在日历中显示第几周
        //     droppable: true, // 允许将事件放在日历上
        //     height: 700,
        //     //初始化数据
        //     events:function(start,end,timezone,callback){
        //       var dataList= []
        //       var params = {
        //         tableName: "scheduledate",
        //         limit:100000000,
        //         offset:0
        //       }
        //       that.axios.get("/api/CUID",{params: params}).then(res =>{
        //         var resData = JSON.parse(res.data)
        //         console.log(resData)
        //         resData.rows.forEach(item =>{
        //           dataList.push({
        //             ID:item.ID,
        //             title:item.DateType,
        //             start:item.WorkDate,
        //             color:item.color
        //           })
        //         })
        //         callback(dataList)
        //       })
        //     },
        //     drop: function(date, allDay) {
        //       console.log(date)
        //       var color = ""
        //       that.scheduleTableData.data.forEach(item =>{
        //         if(allDay.target.innerHTML === item.DateTypeName){
        //           color = item.color
        //         }
        //       })
        //       var params = {
        //         tableName: "scheduledate",
        //         DateType:allDay.target.innerHTML,
        //         WorkDate:moment(date._d).format("YYYY-MM-DD"),
        //         color:color
        //       }
        //       that.axios.post("/api/CUID",that.qs.stringify(params)).then(res =>{
        //         if(res.data == "OK"){
        //           that.$message({
        //             showClose: true,
        //             type: 'success',
        //             message: "添加成功"
        //           });
        //           $('#fullcalendar').fullCalendar('refetchEvents');
        //         }else{
        //           that.$message({
        //             type: 'info',
        //             message: res.data
        //           });
        //         }
        //       })
        //     },
        //     //拖拽换位事件
        //     eventDrop:function(event,dayDelta,minuteDelta,allDay,revertFund){
        //       var params = {
        //         tableName: "scheduledate",
        //         ID:event.ID,
        //         DateType:event.title,
        //         WorkDate:moment(event.start._d).format("YYYY-MM-DD"),
        //         color:event.color
        //       }
        //       that.axios.put("/api/CUID",that.qs.stringify(params)).then(res =>{
        //         if(res.data == "OK"){
        //           that.$message({
        //             showClose: true,
        //             type: 'success',
        //             message: '修改成功'
        //           });
        //           $('#fullcalendar').fullCalendar('refetchEvents');
        //         }else{
        //           that.$message({
        //             type: 'info',
        //             message: res.data
        //           });
        //         }
        //       })
        //     },
        //     //点击日程事件进行删除
        //     eventClick:function(event){
        //       var mulId = [{
        //         ID:event.ID
        //       }]
        //       that.axios.delete("/api/CUID",{
        //         params: {
        //           tableName:"scheduledate",
        //           delete_data:JSON.stringify(mulId)
        //         }
        //       }).then(res =>{
        //         if(res.data == "OK"){
        //           that.$message({
        //             showClose: true,
        //             type: 'success',
        //             message: '删除成功'
        //           });
        //           $('#fullcalendar').fullCalendar('refetchEvents');
        //         }
        //       },res =>{
        //         console.log("请求错误")
        //       })
        //     },
        //     dayClick:function(date, allDay, jsEvent, view){  //点击日期
        //
        //     }
        //   })
        // },res =>{
        //   console.log("请求错误")
        // })
      },
      handleDateClick(arg) {  //点击日期 添加休息日

      },
      handleEventClick(e){

      },
      handleEventDrop(e){

      },
      handleEventResize(e){

      }
    }
  }
</script>

<style scoped>
  .fc-unthemed td.fc-today {
    background: #727786;
  }
</style>
