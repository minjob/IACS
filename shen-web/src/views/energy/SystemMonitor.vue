<template>
  <el-row :gutter="15">
      <el-col :span="24">
        <TabControl :TabControl="TabControl"></TabControl>
        <el-col :span="24" style="background: #34383E;overflow: hidden;position: relative;" v-if="TabControl.TabControlCurrent === '大系统'">
          <div class="MainContain BorderRadius4 SysMonbg" @mousedown="move" data-move>
            <div class="hf-6 color-boxbgc" style="top:55px;left: 53px;">
                <div class='smalllbox color-white'>{{ websockVarData['SCADA.AI.E119HTS_HF1AIWD'] }}°C</div>
                <div class='smalllbox color-lightgreen'>{{ websockVarData['SCADA.AI.E119HTS_HF1AISD'] }}%</div>
            </div>
            <div class="hf-6 color-boxbgc" style="left:162px;top:96px;">
                <div class='smalllbox color-white'></div>
                <div class='smalllbox color-lightgreen'></div>
            </div>
            <div class="hf-6 color-boxbgc" style="left: 429px;top:149px;">
                <div class='smalllbox color-white'></div>
                <div class='smalllbox color-lightgreen'></div>
            </div>
            <div class="hf-6 color-boxbgc" style="left:339px;top:212px;">
                <div class='smalllbox color-white'>{{ websockVarData['SCADA.AI.E119KT__KT1AIFR'] }}HZ</div>
            </div>
            <div class="hf-6 color-boxbgc" style="left:339px;top:287px;">
                <div class='smalllbox color-white'></div>
                <div class='smalllbox color-lightgreen'></div>
            </div>
            <div class="hf-6 color-boxbgc" style="left:343px;top:586px;">
                <div class='smalllbox color-white'></div>
                <div class='smalllbox color-lightgreen'></div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 573px;top: 94px;">
                <div class='smalllbox color-white'>{{ websockVarData['SCADA.AI.E119HTS_HN11AIWD'] }}°C</div>
                <div class='smalllbox color-lightgreen'>{{ websockVarData['SCADA.AI.E119HTS_HN11AISD'] }}%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 802px;top: 94px;">
                <div class='smalllbox color-white'>{{ websockVarData['SCADA.AI.E119HTS_HN10AIWD'] }}°C</div>
                <div class='smalllbox color-lightgreen'>{{ websockVarData['SCADA.AI.E119HTS_HN10AISD'] }}%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 799px;top: 249px;">
                <div class='smalllbox color-white'>{{ websockVarData['SCADA.AI.E119HTS_HN9AIWD'] }}°C</div>
                <div class='smalllbox color-lightgreen'>{{ websockVarData['SCADA.AI.E119HTS_HN9AISD'] }}%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 685px;top: 191px;">
                <div class='smalllbox color-white'>{{ websockVarData['ZT02_TEMP_AVG'] }}°C</div>
                <div class='smalllbox color-lightgreen'>{{ websockVarData['ZT02_SD_AVG'] }}%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 573px;top: 249px;">
                <div class='smalllbox color-white'>{{ websockVarData['SCADA.AI.E119HTS_HN12AIWD'] }}°C</div>
                <div class='smalllbox color-lightgreen'>{{ websockVarData['SCADA.AI.E119HTS_HN12AISD'] }}%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 573px;top: 572px;">
                <div class='smalllbox color-white'>{{ websockVarData['SCADA.AI.E119HTS_HN21AIWD'] }}°C</div>
                <div class='smalllbox color-lightgreen'>{{ websockVarData['SCADA.AI.E119HTS_HN21AISD'] }}%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 802px;top: 572px;">
                <div class='smalllbox color-white'>{{ websockVarData['SCADA.AI.E119HTS_HN19AIWD'] }}°C</div>
                <div class='smalllbox color-lightgreen'>{{ websockVarData['SCADA.AI.E119HTS_HN19AISD'] }}%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 685px;top: 630px;">
                <div class='smalllbox color-white'>{{ websockVarData['ZT01_TEMP_AVG'] }}°C</div>
                <div class='smalllbox color-lightgreen'>{{ websockVarData['ZT01_SD_AVG'] }}%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 573px;top: 771px;">
                <div class='smalllbox color-white'>{{ websockVarData['SCADA.AI.E119HTS_HN20AIWD'] }}°C</div>
                <div class='smalllbox color-lightgreen'>{{ websockVarData['SCADA.AI.E119HTS_HN20AISD'] }}%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 799px;top: 771px;">
                <div class='smalllbox color-white'>{{ websockVarData['SCADA.AI.E119HTS_HN18AIWD'] }}°C</div>
                <div class='smalllbox color-lightgreen'>{{ websockVarData['SCADA.AI.E119HTS_HN18AISD'] }}%</div>
            </div>
            <div class="hf-6 color-boxbgc" style="left: 946px;top: 149px;">
                <div class='smalllbox color-white'></div>
                <div class='smalllbox color-lightgreen'></div>
            </div>
            <div class="hf-6 color-boxbgc" style="left: 1038px;top: 586px;">
                <div class='smalllbox color-white'></div>
                <div class='smalllbox color-lightgreen'></div>
            </div>
            <div class="hf-6 color-boxbgc" style="left: 1214px;top: 96px;">
                <div class='smalllbox color-white'>{{ websockVarData['SCADA.AI.E119HTS_HF8AIWD'] }} 27.6°C</div>
                <div class='smalllbox color-lightgreen'>{{ websockVarData['SCADA.AI.E119HTS_HF8AISD'] }} 66%</div>
            </div>
            <div class="hf-6 color-boxbgc" style="left: 1038px;top: 212px;">
                <div class='smalllbox color-white'>{{ websockVarData['SCADA.AI.E119KT__KT2AIFR'] }}HZ</div>
            </div>
            <div class="hf-6 color-boxbgc" style="left: 1038px;top: 287px;">
                <div class='smalllbox color-white'></div>
                <div class='smalllbox color-lightgreen'></div>
            </div>
            <div class="hf-6 color-boxbgc" style="top:56px;left:1323px;">
                <div class='smalllbox color-white'></div>
                <div class='smalllbox color-lightgreen'></div>
            </div>
            <div class="BorderRadius4 color-lightbluebgc sfs" style="top:95px;left:260px;">湿风室</div>
            <div class="BorderRadius4 color-lightbluebgc sfs" style="top:95px;left:1142px;">湿风室</div>
            <div class="text-box color-mainbgc" style="top:118px;left:53px;">新风亭</div>
            <div class="text-box color-mainbgc" style="top:581px;left:53px;">排风亭</div>
            <div class="text-box color-mainbgc" style="top:118px;left:1322px;">新风亭</div>
            <div class="text-box color-mainbgc" style="top:581px;left:1322px;">排风亭</div>
         </div>
        </el-col>
        <el-col :span="24" style="background: #34383E;overflow: hidden;position: relative;" v-if="TabControl.TabControlCurrent === '小系统'">
          <div class="MainContain BorderRadius4 smallSysMonbg" @mousedown="move" data-move>

          </div>
        </el-col>
        <el-row :gutter="15" style="overflow: hidden;" v-if="TabControl.TabControlCurrent === '冷却系统'">
          <el-col :span="6">
            <div class="platformContainer">
              <p class="text-size-18 marginBottom">冷水机组1<span class="floatRight text-size-24"><svg-icon icon-class="jingshideng" className="color-lightgreen"></svg-icon></span></p>
              <el-row class="marginBottom">
                <el-col :span="12"><span>故障状态：正常</span></el-col>
                <el-col :span="12"><span>本地/远程：本地</span></el-col>
              </el-row>
              <el-row>
                <el-col :span="12"><span>手/自动：手动</span></el-col>
                <el-col :span="12"><span>心跳检测位：</span></el-col>
              </el-row>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="platformContainer">
              <p class="text-size-18 marginBottom">冷水机组2<span class="floatRight text-size-24"><svg-icon icon-class="jingshideng" className="color-color-grayblack"></svg-icon></span></p>
              <el-row class="marginBottom">
                <el-col :span="12"><span>故障状态：正常</span></el-col>
                <el-col :span="12"><span>本地/远程：本地</span></el-col>
              </el-row>
              <el-row>
                <el-col :span="12"><span>手/自动：手动</span></el-col>
                <el-col :span="12"><span>心跳检测位：</span></el-col>
              </el-row>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="platformContainer">
              <p class="text-size-18 marginBottom">冷水塔水阀1</p>
              <el-row class="marginBottom">
                <el-col :span="24"> <span>水阀关到位：</span></el-col>
              </el-row>
              <el-row>
                <el-col :span="24"><span>水阀关到位</span></el-col>
              </el-row>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="platformContainer">
              <p class="text-size-18 marginBottom">冷水塔水阀2</p>
              <el-row class="marginBottom">
                <el-col :span="24"><span>水阀关到位：</span></el-col>
              </el-row>
              <el-row>
                <el-col :span="24"><span>水阀关到位</span></el-col>
              </el-row>
            </div>
          </el-col>
        </el-row>
        <el-col :span="24" style="background: #34383E;overflow: hidden;position: relative;" v-if="TabControl.TabControlCurrent === '冷却系统'">

          <div class="MainContain BorderRadius4 coolingSysMonbg" style="width: 1500px;" @mousedown="move" data-move >
            <el-popover placement="bottom" title="冷却塔1" width="200" trigger="click">
              <el-button type="success" icon="el-icon-success" size="small" @click="runControl('LQT1','RUN')">开启</el-button>
              <el-button type="info" icon="el-icon-error" size="small" @click="runControl('LQT1','STOP')">关闭</el-button>
              <div slot="reference" class="lqt" style="top: 75px;left: 165px;"></div>
            </el-popover>
            <el-popover placement="bottom" title="冷却塔2" width="200" trigger="click">
              <el-button type="success" icon="el-icon-success" size="small" @click="runControl('LQT2','RUN')">开启</el-button>
              <el-button type="info" icon="el-icon-error" size="small" @click="runControl('LQT2','STOP')">关闭</el-button>
              <div slot="reference" class="lqt" style="top: 75px;left: 355px;"></div>
            </el-popover>
            <el-popover placement="right" title="冷水机组1" width="200" trigger="click">
              <el-button type="success" icon="el-icon-success" size="small" @click="runControl('LS1','RUN')">开启</el-button>
              <el-button type="info" icon="el-icon-error" size="small" @click="runControl('LS1','STOP')">关闭</el-button>
              <div slot="reference" class="jz" style="top: 425px;left: 55px;"></div>
            </el-popover>
            <el-popover placement="right" title="冷水机组2" width="200" trigger="click">
              <el-button type="success" icon="el-icon-success" size="small" @click="runControl('LS2','RUN')">开启</el-button>
              <el-button type="info" icon="el-icon-error" size="small" @click="runControl('LS2','STOP')">关闭</el-button>
              <div slot="reference" class="jz" style="top: 625px;left: 55px;"></div>
            </el-popover>
            <el-popover placement="right" title="冷却泵1" width="225" trigger="click">
              <el-form :inline="true" :model="formParameters">
                <el-form-item label="频率(HZ)">
                  <el-input v-model="formParameters.HZLQ1" size="mini" style="width: 58px;"></el-input>
                  <el-button type="primary" @click="editHZ('LQ1',formParameters.HZLQ1)" size="mini">保存</el-button>
                </el-form-item>
              </el-form>
              <el-button type="success" icon="el-icon-success" size="small" @click="runControl('LQ1','RUN')">开启</el-button>
              <el-button type="info" icon="el-icon-error" size="small" @click="runControl('LQ1','STOP')">关闭</el-button>
              <div slot="reference" class="lqb" style="top: 305px;left: 450px;"></div>
            </el-popover>
            <el-popover placement="right" title="冷却泵2" width="225" trigger="click">
              <el-form :inline="true" :model="formParameters">
                <el-form-item label="频率(HZ)">
                  <el-input v-model="formParameters.HZLQ2" size="mini" style="width: 58px;"></el-input>
                  <el-button type="primary" @click="editHZ('LQ2',formParameters.HZLQ2)" size="mini">保存</el-button>
                </el-form-item>
              </el-form>
              <el-button type="success" icon="el-icon-success" size="small" @click="runControl('LQ2','RUN')">开启</el-button>
              <el-button type="info" icon="el-icon-error" size="small" @click="runControl('LQ2','STOP')">关闭</el-button>
              <div slot="reference" class="lqb" style="top: 395px;left: 450px;"></div>
            </el-popover>
            <el-popover placement="right" title="冷冻泵1" width="225" trigger="click">
              <el-form :inline="true" :model="formParameters">
                <el-form-item label="频率(HZ)">
                  <el-input v-model="formParameters.HZLD1" size="mini" style="width: 58px;"></el-input>
                  <el-button type="primary" @click="editHZ('LD1',formParameters.HZLD1)" size="mini">保存</el-button>
                </el-form-item>
              </el-form>
              <el-button type="success" icon="el-icon-success" size="small" @click="runControl('LD1','RUN')">开启</el-button>
              <el-button type="info" icon="el-icon-error" size="small" @click="runControl('LD1','STOP')">关闭</el-button>
              <div slot="reference" class="lqb" style="top: 715px;left: 470px;"></div>
            </el-popover>
            <el-popover placement="right" title="冷冻泵2" width="225" trigger="click">
              <el-form :inline="true" :model="formParameters">
                <el-form-item label="频率(HZ)">
                  <el-input v-model="formParameters.HZLD2" size="mini" style="width: 58px;"></el-input>
                  <el-button type="primary" @click="editHZ('LD2',formParameters.HZLD2)" size="mini">保存</el-button>
                </el-form-item>
              </el-form>
              <el-button type="success" icon="el-icon-success" size="small" @click="runControl('LD2','RUN')">开启</el-button>
              <el-button type="info" icon="el-icon-error" size="small" @click="runControl('LD2','STOP')">关闭</el-button>
              <div slot="reference" class="lqb" style="top: 805px;left: 470px;"></div>
            </el-popover>
            <div class="wd" style="top: 368px;left: 148px;">{{ websockVarData['SCADA.AI.E119LS__LS1AI08'] }}°C</div>
            <div class="wd" style="top: 362px;left: 267px;">{{ websockVarData['SCADA.AI.E119LS__LS1AI09'] }}°C</div>
            <div class="wd" style="top: 450px;left: 293px;">{{ websockVarData['SCADA.AI.E119LS__LS2AI09'] }}°C</div>
            <div class="wd" style="top: 568px;left: 148px;">{{ websockVarData['SCADA.AI.E119LS__LS2AI08'] }}°C</div>
            <div class="wd" style="top: 580px;left: 349px;">{{ websockVarData['SCADA.AI.E119LS__LS1AI01'] }}°C</div>
            <div class="wd" style="top: 748px;left: 188px;">{{ websockVarData['SCADA.AI.E119LS__LS2AI01'] }}°C</div>
            <div class="wd" style="top: 788px;left: 352px;">{{ websockVarData['SCADA.AI.E119LS__LS1AI07'] }}°C</div>
            <div class="wd" style="top: 855px;left: 292px;">{{ websockVarData['SCADA.AI.E119LS__LS2AI07'] }}°C</div>
            <div class="wd" style="top: 342px;left: 512px;">{{ websockVarData['SCADA.AI.E119LQ__LQ1AIFR'] }}°C</div>
            <div class="wd" style="top: 430px;left: 512px;">{{ websockVarData['SCADA.AI.E119LQ__LQ2AIFR'] }}°C</div>
            <div class="wd" style="top: 755px;left: 538px;">{{ websockVarData['SCADA.AI.E119LD__LD1AIFR'] }}°C</div>
            <div class="wd" style="top: 845px;left: 538px;">{{ websockVarData['SCADA.AI.E119LD__LD2AIFR'] }}°C</div>

            <div class="wd" style="top: 125px;left: 960px;">{{ websockVarData['SCADA.AI.E119SDF_SDF1AIOC'] }}%</div>
            <div class="wd" style="top: 242px;left: 960px;">{{ websockVarData['SCADA.AI.E119KT__KT1AIFR'] }}HZ</div>
            <div class="wd" style="top: 125px;left: 1050px;">{{ websockVarData['SCADA.AI.E119SDF_SDF2AIOC'] }}%</div>
            <div class="wd" style="top: 242px;left: 1050px;">{{ websockVarData['SCADA.AI.E119KT__KT2AIFR'] }}HZ</div>
          </div>
        </el-col>
        <el-col :span="24" style="background: #34383E;overflow: hidden;position: relative;" v-if="TabControl.TabControlCurrent === '设备房温度'">
          <div class="MainContain BorderRadius4 eqSysMonbg" @mousedown="move" data-move>
            <div class="eqhouse" style="top: 250px;left: 59px;">{{ websockVarData['SCADA.AI.E119HTS_HN1AIWD'] }}°C</div>
            <div class="eqhouse" style="top: 250px;left: 420px;">{{ websockVarData['SCADA.AI.E119HTS_HN14AIWD'] }}°C</div>
            <div class="eqhouse" style="top: 250px;left: 775px;">{{ websockVarData['SCADA.AI.E119HTS_HN3AIWD'] }}°C</div>
            <div class="eqhouse" style="top: 250px;left: 1138px;">{{ websockVarData['SCADA.AI.E119HTS_HN5AIWD'] }}°C</div>
            <div class="eqhouse" style="top: 624px;left: 59px;">{{ websockVarData['SCADA.AI.E119HTS_HN13AIWD'] }}°C</div>
            <div class="eqhouse" style="top: 624px;left: 420px;">{{ websockVarData['SCADA.AI.E119HTS_HN4AIWD'] }}°C</div>
            <div class="eqhouse" style="top: 624px;left: 775px;">{{ websockVarData['SCADA.AI.E119HTS_HN6AIWD'] }}°C</div>
            <div class="eqhouse" style="top: 624px;left: 1138px;">{{ websockVarData['SCADA.AI.E119HTS_HN7AIWD'] }}°C</div>
          </div>
        </el-col>
      </el-col>
  </el-row>
</template>

<script>
  var moment = require('moment');
  import TabControl from '@/components/TabControl'
  export default {
    name: "SystemMonitor",
    components:{TabControl},
    data(){
      return {
        TabControl:{
          TabControlCurrent:"",
          TabControlOptions:[
            {name:"大系统"},
            {name:"小系统"},
            {name:"冷却系统"},
            {name:"设备房温度"},
          ],
        },
        websock:null,
        websockVarData:{},
        formParameters:{
          HZLQ1:"",
          HZLQ2:"",
          HZLD1:"",
          HZLD2:"",
        },
      }
    },
    created(){
      this.initWebSocket()
    },
    mounted(){

    },
    watch:{

    },
    computed:{ //计算属性

    },
    destroyed() {
      if(this.websock){
        this.websock.close() //离开路由之后断开websocket连接
      }
    },
    methods: {
      move(e){
        let odiv = e.target; //获取目标元素
        if(odiv.attributes.hasOwnProperty("data-move")){
          //算出鼠标相对元素的位置
          let disX = e.clientX - odiv.offsetLeft;
          let disY = e.clientY - odiv.offsetTop;
          document.onmousemove = (e)=>{ //鼠标按下并移动的事件
            //用鼠标的位置减去鼠标相对元素的位置，得到元素的位置
            let left = e.clientX - disX - 8;
            let top = e.clientY - disY;
            //绑定元素位置到positionX和positionY上面
            this.positionX = top;
            this.positionY = left;
            //移动当前元素
            odiv.style.left = left + 'px';
            odiv.style.top = top + 'px';
          };
          document.onmouseup = (e) => {
            document.onmousemove = null;
            document.onmouseup = null;
          };
        }
      },
      initWebSocket(){ //初始化weosocket
        // this.websock = new WebSocket('ws://' + location.host + '/socket');
        this.websock = new WebSocket('ws://127.0.0.1:5002/socket');
        this.websock.onmessage = this.websocketonmessage;
        this.websock.onopen = this.websocketonopen;
        this.websock.onerror = this.websocketonerror;
        this.websock.onclose = this.websocketclose;
      },
      websocketonopen(){ //连接建立之后执行send方法发送数据
        this.websocketsend();
      },
      websocketonerror(){//连接建立失败重连
        console.log("websocket连接失败")
      },
      websocketonmessage(e){ //数据接收
        var resdata = JSON.parse(e.data);
        this.websockVarData = resdata
      },
      websocketsend(Data){//数据发送
        this.websock.send(Data);
      },
      websocketclose(e){  //关闭
        console.log("websocket关闭")
      },
      closesocket(){
        this.websock.close()
      },
      runControl(value,type){
        this.axios.post("/api/run",{
          params: {
            EquipmentCode:value,
            Status:type,
          }
        }).then(res =>{
          if(res.data.code === "20001"){
            this.$message({
              showClose: true,
              type: 'success',
              message: res.data.message
            });
          }
        },res =>{
          console.log("请求错误")
        })
      },
      editHZ(value,HZ){
        this.axios.post("/api/status",{
          params: {
            EquipmentCode:value,
            HZ:HZ,
          }
        }).then(res =>{
          if(res.data.code === "20001"){
            this.$message({
              showClose: true,
              type: 'success',
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

</style>
