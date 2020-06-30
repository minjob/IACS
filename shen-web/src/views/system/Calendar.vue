<template>
  <el-row :gutter="20">
    <el-col :span="24">
      <el-col :span="5">
        <div class="platformContainer" style="height: 730px;">
          <div id='external-events' class="itemMarginBottom">
            <h4>可拖放的日程</h4>
            <a class='fc-event' style="background: #00c3db;border: 1px solid #00c3db;">维保</a>
            <a class='fc-event' style="background: #f7d013;border: 1px solid #f7d013;">休息</a>
            <a class='fc-event' style="background: #e73b3b;border: 1px solid #e73b3b;">其他</a>
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
          <div id="fullcalendar" style="color: #fff;"></div>
        </div>
      </el-col>
    </el-col>
  </el-row>
</template>

<script>
  import tableView from '@/components/CommonTable'
  var moment = require('moment');
  export default {
    name: "Calendar",
    components:{tableView},
    data(){
      return {
        scheduleTableData:{
          tableName:"scheduleDateType",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showHeader:false,searchProp:false},
            {label:"类型编码",prop:"DateTypeCode",type:"input",value:"",showHeader:true,searchProp:true},
            {label:"类型名称",prop:"DateTypeName",type:"input",value:"",showHeader:true,searchProp:true},
            {label:"注释",prop:"Desc",type:"input",value:"",showHeader:true,searchProp:true},
            {label:"颜色",prop:"color",type:"input",value:"",showHeader:true,searchProp:false},
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
      }
    },
    mounted() {
      this.renderScheduling()
      this.getScheduleTableData()
    },
    methods:{
      renderScheduling(){ //渲染
        $('#external-events .fc-event').each(function() {
          $(this).data('event', {
              title: $.trim($(this).text()), // use the element's text as the event title
              stick: false // 拖动后不固定显示在日历上
          });
          // make the event draggable using jQuery UI
          $(this).draggable({
              zIndex: 999,
              revert: true,      // will cause the event to go back to its
              revertDuration: 0  //  original position after the drag
          });
        });
        $('#fullcalendar').fullCalendar({
          header: {
            right: 'prev,next today',
            center: 'title',
            left: 'month,agendaWeek,agendaDay,listMonth'
          },
          buttonText: {
            today: '今天',
            month: '月',
            week: '周',
            day: '日',
            list:'日程'
          },
          monthNames: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
          monthNamesShort: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
          dayNames: ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"],
          dayNamesShort: ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"],
          editable: true, //支持拖动换位
          navLinks: true, //是否可以单击日/周名称来导航视图
          weekNumbers: true, //是否在日历中显示第几周
          droppable: true, // 允许将事件放在日历上
          height: 700,
          //初始化数据
          events:function(start,end,timezone,callback){
            console.log(start)
          },
          drop: function(date, allDay) {
            console.log(date)
          },
          //拖拽换位事件
          eventDrop:function(event,dayDelta,minuteDelta,allDay,revertFund){

          },
          //点击日程事件进行删除
          eventClick:function(event){

          },
          dayClick:function(date, allDay, jsEvent, view){

          }
        })
      },
      getScheduleTableData(){
        var that = this
        var params = {
          tableName: this.scheduleTableData.tableName,
          limit:this.scheduleTableData.limit,
          offset:this.scheduleTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          var data = JSON.parse(res.data)
          that.scheduleTableData.data = data.rows
          that.scheduleTableData.total = data.total
        },res =>{
          console.log("请求错误")
        })
      },
      getData() {
        this.axios.get("/api/CUID",{
          params: {
            tableName: "plantCalendarScheduling",
            limit:100000000,
            offset:0
          }
        }).then(res =>{
          var data = JSON.parse(res.data)
          this.events = data.rows
        })
      },
      handleDateClick(arg){  //点击日期 添加休息日
        this.start = arg.dateStr
        this.$confirm('是否要把'+ this.start + '设置为休息日？', '提示', {
          distinguishCancelAndClose:true,
          type: 'warning'
        }).then(()  => {
          var params = {
            tableName: "plantCalendarScheduling",
            title:"休息",
            start:this.start,
            color:"#00c3db"
          }
          this.axios.post("/api/CUID",this.qs.stringify(params)).then(res =>{
            if(res.data == "OK"){
              this.getData()
              this.dialogTableVisible = false
              this.$message({
                type: 'success',
                message: "添加成功"
              });
            }else{
              this.$message({
                type: 'info',
                message: res.data
              });
            }
          })
        }).catch(()   => {
          this.$message({
            type: 'info',
            message: '已取消添加'
          });
        });
      },
      handleEventClick(e) {  //点击日程删除
        var ID = {
          id:e.event.extendedProps.ID
        }
        this.$confirm('此操作将永久删除该日程, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.axios.delete("/api/CUID",{
            params: {
              tableName: "plantCalendarScheduling",
              delete_data:JSON.stringify(ID),
            }
          }).then(res =>{
            if(res.data == "OK"){
              this.getData()
              this.$message({
                type: 'success',
                message: '删除成功!'
              });
            }
          },res =>{
            console.log("请求错误")
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      },
      handleEventDrop(e){   //拖动日程
        var startDate = moment(e.event.start).format('YYYY-MM-DD')
        var EndDate = moment(e.event.end).format('YYYY-MM-DD')
        var params = {
          tableName: "plantCalendarScheduling",
          ID:e.event.extendedProps.ID,
          title:e.event.title,
          start:startDate,
          end:EndDate,
          color:e.event.backgroundColor
        }
        this.axios.put("/api/CUID",this.qs.stringify(params)).then(res =>{
          if(res.data == "OK"){
            this.getData()
            this.$message({
              type: 'success',
              message: "修改成功"
            });
          }else{
            this.$message({
              type: 'info',
              message: res.data
            });
          }
        },res =>{
          console.log("请求错误")
        })
      },
      handleEventResize(e){  //拖动改变日程长度
        var startDate = moment(e.event.start).format('YYYY-MM-DD')
        var EndDate = moment(e.event.end).format('YYYY-MM-DD')
        var params = {
          tableName: "plantCalendarScheduling",
          ID:e.event.extendedProps.ID,
          title:e.event.title,
          start:startDate,
          end:EndDate,
          color:e.event.backgroundColor
        }
        this.axios.put("/api/CUID",this.qs.stringify(params)).then(res =>{
          if(res.data == "OK"){
            this.getData()
            this.$message({
              type: 'success',
              message: "修改成功"
            });
          }else{
            this.$message({
              type: 'info',
              message: res.data
            });
            this.getData()
          }
        },res =>{
          console.log("请求错误")
        })
      }
    }
  }
</script>

<style scoped>
  #external-events h4 {
    font-size: 16px;
    margin-top: 0;
    padding-top: 1em;
  }
  #external-events .fc-event {
    margin: 10px 0;
    cursor: pointer;
  }
  #external-events p {
    margin: 1.5em 0;
    font-size: 11px;
    color: #666;
  }
</style>
