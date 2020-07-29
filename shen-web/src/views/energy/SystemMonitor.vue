<template>
  <el-row :gutter="15">
      <el-col :span="24">
        <TabControl :TabControl="TabControl"></TabControl>
        <el-col :span="24" style="background: #34383E;overflow: hidden;position: relative;" v-if="TabControl.TabControlCurrent === '大系统'">
          <div class="MainContain BorderRadius4 SysMonbg" @mousedown="move" data-move>
            <div class="hf-6 color-boxbgc" style="top:55px;left: 53px;">
                <div class='smalllbox color-white'>{{ Number(websockVarData['SCADA.AI.E119HTS_HF1AIWD']) / 10 }}°C</div>
                <div class='smalllbox color-lightgreen'>{{ Number(websockVarData['SCADA.AI.E119HTS_HF1AISD']) / 10 }}%</div>
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
                <div class='smalllbox color-white'>{{ Number(websockVarData['SCADA.AI.E119KT__KT1AIFR']) / 10 }}HZ</div>
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
                <div class='smalllbox color-white'>{{ Number(websockVarData['SCADA.AI.E119HTS_HN11AIWD']) / 10 }}°C</div>
                <div class='smalllbox color-lightgreen'>{{ Number(websockVarData['SCADA.AI.E119HTS_HN11AISD']) / 10 }}%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 802px;top: 94px;">
                <div class='smalllbox color-white'>{{ Number(websockVarData['SCADA.AI.E119HTS_HN10AIWD']) / 10 }}°C</div>
                <div class='smalllbox color-lightgreen'>{{ Number(websockVarData['SCADA.AI.E119HTS_HN10AISD']) / 10 }}%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 799px;top: 249px;">
                <div class='smalllbox color-white'>{{ Number(websockVarData['SCADA.AI.E119HTS_HN9AIWD']) / 10 }}°C</div>
                <div class='smalllbox color-lightgreen'>{{ Number(websockVarData['SCADA.AI.E119HTS_HN9AISD']) / 10 }}%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 685px;top: 191px;">
                <div class='smalllbox color-white'>{{ websockVarData['ZT02_TEMP_AVG'] }}°C</div>
                <div class='smalllbox color-lightgreen'>{{ websockVarData['ZT02_SD_AVG'] }}%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 573px;top: 249px;">
                <div class='smalllbox color-white'>{{ Number(websockVarData['SCADA.AI.E119HTS_HN12AIWD']) / 10 }}°C</div>
                <div class='smalllbox color-lightgreen'>{{ Number(websockVarData['SCADA.AI.E119HTS_HN12AISD']) / 10 }}%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 573px;top: 572px;">
                <div class='smalllbox color-white'>{{Number( websockVarData['SCADA.AI.E119HTS_HN21AIWD']) / 10 }}°C</div>
                <div class='smalllbox color-lightgreen'>{{ Number(websockVarData['SCADA.AI.E119HTS_HN21AISD']) / 10 }}%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 802px;top: 572px;">
                <div class='smalllbox color-white'>{{ Number(websockVarData['SCADA.AI.E119HTS_HN19AIWD']) / 10 }}°C</div>
                <div class='smalllbox color-lightgreen'>{{ Number(websockVarData['SCADA.AI.E119HTS_HN19AISD']) / 10 }}%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 685px;top: 630px;">
                <div class='smalllbox color-white'>{{ websockVarData['ZT01_TEMP_AVG'] }}°C</div>
                <div class='smalllbox color-lightgreen'>{{ websockVarData['ZT01_SD_AVG'] }}%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 573px;top: 771px;">
                <div class='smalllbox color-white'>{{ Number(websockVarData['SCADA.AI.E119HTS_HN20AIWD']) / 10 }}°C</div>
                <div class='smalllbox color-lightgreen'>{{ Number(websockVarData['SCADA.AI.E119HTS_HN20AISD']) / 10 }}%</div>
            </div>
            <div class="hf-6 color-mainbgc" style="left: 799px;top: 771px;">
                <div class='smalllbox color-white'>{{ Number(websockVarData['SCADA.AI.E119HTS_HN18AIWD']) / 10 }}°C</div>
                <div class='smalllbox color-lightgreen'>{{ Number(websockVarData['SCADA.AI.E119HTS_HN18AISD']) / 10 }}%</div>
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
                <div class='smalllbox color-white'>{{ Number(websockVarData['SCADA.AI.E119KT__KT2AIFR']) / 10 }}HZ</div>
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
        <el-row :gutter="15" style="overflow: hidden;" v-if="TabControl.TabControlCurrent === '冷水系统'">
          <el-col :span="5">
            <div class="platformContainer">
              <p class="text-size-18 marginBottom">冷水机组1</p>
              <el-row class="marginBottom">
                <el-col :span="12">
                  <span>故障状态：<span v-if="LS1Bit[LS1Bit.length-6] === '1'">故障</span><span v-if="LS1Bit[LS1Bit.length-6] === '0'">正常</span></span>
                </el-col>
                <el-col :span="12">
                  <span>本地/远程：<span v-if="LS1Bit[LS1Bit.length-7] === '0'">本地</span><span v-if="LS1Bit[LS1Bit.length-7] === '1'">远程</span></span>
                </el-col>
              </el-row>
              <el-row>
                <el-col :span="12">
                  <span>手/自动：<span v-if="LS1Bit[LS1Bit.length-9] === '0'">手动</span><span v-if="LS1Bit[LS1Bit.length-9] === '1' || !LS1Bit[LS1Bit.length-9]">自动</span></span>
                </el-col>
              </el-row>
            </div>
          </el-col>
          <el-col :span="5">
            <div class="platformContainer">
              <p class="text-size-18 marginBottom">冷水机组2</p>
              <el-row class="marginBottom">
                <el-col :span="12">
                  <span>故障状态：<span v-if="LS2Bit[LS2Bit.length-6] === '1'">故障</span><span v-if="LS2Bit[LS2Bit.length-6] === '0'">正常</span></span>
                </el-col>
                <el-col :span="12">
                  <span>本地/远程：<span v-if="LS2Bit[LS2Bit.length-7] === '0'">本地</span><span v-if="LS2Bit[LS2Bit.length-7] === '1'">远程</span></span>
                </el-col>
              </el-row>
              <el-row>
                <el-col :span="12">
                  <span>手/自动：<span v-if="LS2Bit[LS2Bit.length-9] === '0'">手动</span><span v-if="LS2Bit[LS2Bit.length-9] === '1' || !LS2Bit[LS2Bit.length-9]">自动</span></span>
                </el-col>
              </el-row>
            </div>
          </el-col>
          <el-col :span="5">
            <div class="platformContainer">
              <p class="text-size-18 marginBottom">冷水塔水阀1</p>
              <el-row class="marginBottom">
                <el-col :span="24"><span>水阀关到位：<span v-if="LST1Bit[LST1Bit.length-1] === '1'">到位</span><span v-if="LST1Bit[LST1Bit.length-1] === '0'">未到位</span></span></el-col>
              </el-row>
              <el-row>
                <el-col :span="24"><span>水阀开到位：<span v-if="LST1Bit[LST1Bit.length-2] === '1'">到位</span><span v-if="LST1Bit[LST1Bit.length-2] === '0'">未到位</span></span></el-col>
              </el-row>
            </div>
          </el-col>
          <el-col :span="5">
            <div class="platformContainer">
              <p class="text-size-18 marginBottom">冷水塔水阀2</p>
              <el-row class="marginBottom">
                <el-col :span="24"><span>水阀关到位：<span v-if="LST2Bit[LST2Bit.length-1] === '1'">到位</span><span v-if="LST2Bit[LST2Bit.length-1] === '0'">未到位</span></span></el-col>
              </el-row>
              <el-row>
                <el-col :span="24"><span>水阀开到位：<span v-if="LST2Bit[LST2Bit.length-2] === '1'">到位</span><span v-if="LST2Bit[LST2Bit.length-2] === '0'">未到位</span></span></el-col>
              </el-row>
            </div>
          </el-col>
          <el-col :span="4">
            <div class="platformContainer">
              <el-form class="blackComponents">
                <el-form-item label="节能开关：" class="marginBottom">
                  <el-switch v-model="websockVarData['LS_JN_FLAG']" v-has="['系统监控操作控制']" active-color="#13ce66" inactive-color="#727786" active-value="1" inactive-value="0" @change="changeConservationSwitch"></el-switch>
                </el-form-item>
                <el-form-item label="复位：" style="margin-bottom: 5px;">
                  <el-button type="primary" size="small" v-has="['系统监控操作控制']" @click="startReseting">开始复位</el-button>
                </el-form-item>
              </el-form>
            </div>
          </el-col>
        </el-row>
        <el-col :span="24" style="background: #34383E;overflow: hidden;position: relative;" v-if="TabControl.TabControlCurrent === '冷水系统'">
          <div class="MainContain BorderRadius4 coolingSysMonbg" style="width: 1500px;" @mousedown="move" data-move >
            <el-popover placement="bottom" title="冷却塔1" width="240" trigger="click" v-has="['系统监控操作控制']">
              <el-button type="success" icon="el-icon-success" size="small" @click="runControl('LQT1','RUN')">开启</el-button>
              <el-button type="info" icon="el-icon-error" size="small" @click="runControl('LQT1','STOP')">关闭</el-button>
              <div slot="reference" class="lqt" style="top: 75px;left: 165px;"></div>
            </el-popover>
            <el-popover placement="bottom" title="冷却塔2" width="240" trigger="click" v-has="['系统监控操作控制']">
              <el-button type="success" icon="el-icon-success" size="small" @click="runControl('LQT2','RUN')">开启</el-button>
              <el-button type="info" icon="el-icon-error" size="small" @click="runControl('LQT2','STOP')">关闭</el-button>
              <div slot="reference" class="lqt" style="top: 75px;left: 355px;"></div>
            </el-popover>
            <el-popover placement="right" title="冷水机组1" width="400" trigger="click">
              <el-divider content-position="left">设备状态</el-divider>
              <el-row>
                <el-col :span="12">
                  <p class="marginBottomS">出水温度 <span class="color-darkblue">{{ Number(websockVarData['SCADA.AI.E119LS__LS1AI01']) / 10 }}</span> °C</p>
                  <p class="marginBottomS">吸气压力 <span class="color-darkblue">{{ Number(websockVarData['SCADA.AI.E119LS__LS1AI02']) / 10 }}</span> Kpa</p>
                  <p class="marginBottomS">排气压力 <span class="color-darkblue">{{ Number(websockVarData['SCADA.AI.E119LS__LS1AI03']) / 10 }}</span> Kpa</p>
                  <p class="marginBottomS">目标容器百分比 <span class="color-darkblue">{{ Number(websockVarData['SCADA.AI.E119LS__LS1AI10']) / 10 }}</span> %</p>
                </el-col>
                <el-col :span="12">
                  <p class="marginBottomS">蒸发器回水温度 <span class="color-darkblue">{{ Number(websockVarData['SCADA.AI.E119LS__LS1AI07']) / 10 }}</span> °C</p>
                  <p class="marginBottomS">冷凝器出水温度 <span class="color-darkblue">{{ Number(websockVarData['SCADA.AI.E119LS__LS1AI08']) / 10 }}</span> °C</p>
                  <p class="marginBottomS">冷凝器回水温度 <span class="color-darkblue">{{ Number(websockVarData['SCADA.AI.E119LS__LS1AI09']) / 10 }}</span> °C</p>
                </el-col>
                <el-col :span="24">
                  <p class="marginBottomS">一号压缩机运行电流 <span class="color-darkblue">{{ Number(websockVarData['SCADA.AI.E119LS__LS1AI05']) / 10 }}</span> A</p>
                  <p class="marginBottomS">二号压缩机运行电流 <span class="color-darkblue">{{ Number(websockVarData['SCADA.AI.E119LS__LS1AI06']) / 10 }}</span> A</p>
                  <p class="marginBottomS">一号压缩机当前容量百分比 <span class="color-darkblue">{{ Number(websockVarData['SCADA.AI.E119LS__LS1AI11']) / 10 }}</span> %</p>
                  <p class="marginBottomS">二号压缩机当前容量百分比 <span class="color-darkblue">{{ Number(websockVarData['SCADA.AI.E119LS__LS1AI12']) / 10 }}</span> %</p>
                </el-col>
              </el-row>
              <el-divider content-position="left">设备控制</el-divider>
              <el-button type="warning" icon="el-icon-refresh-left" size="small" v-has="['系统监控操作控制']" @click="faultReset('LS1')">故障复位</el-button>
              <el-button slot="reference" style="position:absolute;top: 535px;left: 65px;" size="small">机组信息</el-button>
            </el-popover>
            <el-popover placement="right" title="冷水机组1" width="240" trigger="click" v-has="['系统监控操作控制']">
              <el-button type="success" icon="el-icon-success" size="small" @click="runControl('LS1','RUN')">开启</el-button>
              <el-button type="info" icon="el-icon-error" size="small" @click="runControl('LS1','STOP')">关闭</el-button>
              <div slot="reference" class="jz" style="top: 425px;left: 55px;"></div>
            </el-popover>
            <div class="wd" style="top: 398px;left: 70px;">
              <span v-if="LS1Bit[LS1Bit.length-1] === '1'">运行中</span>
              <span v-if="LS1Bit[LS1Bit.length-1] === '0'"><span class="color-offwhite">停机</span></span>
            </div>
            <div class="wd" style="top: 600px;left: 70px;">
              <span v-if="LS2Bit[LS2Bit.length-1] === '1'">运行中</span>
              <span v-if="LS2Bit[LS2Bit.length-1] === '0'"><span class="color-offwhite">停机</span></span>
            </div>

            <el-popover placement="right" title="冷水机组2" width="400" trigger="click">
              <el-divider content-position="left">设备状态</el-divider>
              <el-row>
                <el-col :span="12">
                  <p class="marginBottomS">出水温度 <span class="color-darkblue">{{ Number(websockVarData['SCADA.AI.E119LS__LS2AI01']) / 10 }}</span> °C</p>
                  <p class="marginBottomS">吸气压力 <span class="color-darkblue">{{ Number(websockVarData['SCADA.AI.E119LS__LS2AI02']) / 10 }}</span> Kpa</p>
                  <p class="marginBottomS">排气压力 <span class="color-darkblue">{{ Number(websockVarData['SCADA.AI.E119LS__LS2AI03']) / 10 }}</span> Kpa</p>
                  <p class="marginBottomS">目标容器百分比 <span class="color-darkblue">{{ Number(websockVarData['SCADA.AI.E119LS__LS2AI10']) / 10 }}</span> %</p>
                </el-col>
                <el-col :span="12">
                  <p class="marginBottomS">蒸发器回水温度 <span class="color-darkblue">{{ Number(websockVarData['SCADA.AI.E119LS__LS2AI07']) / 10 }}</span> °C</p>
                  <p class="marginBottomS">冷凝器出水温度 <span class="color-darkblue">{{ Number(websockVarData['SCADA.AI.E119LS__LS2AI08']) / 10 }}</span> °C</p>
                  <p class="marginBottomS">冷凝器回水温度 <span class="color-darkblue">{{ Number(websockVarData['SCADA.AI.E119LS__LS2AI09']) / 10 }}</span> °C</p>
                </el-col>
                <el-col :span="24">
                  <p class="marginBottomS">一号压缩机运行电流 <span class="color-darkblue">{{ Number(websockVarData['SCADA.AI.E119LS__LS2AI05']) / 10 }}</span> A</p>
                  <p class="marginBottomS">二号压缩机运行电流 <span class="color-darkblue">{{ Number(websockVarData['SCADA.AI.E119LS__LS2AI06']) / 10 }}</span> A</p>
                  <p class="marginBottomS">一号压缩机当前容量百分比 <span class="color-darkblue">{{ Number(websockVarData['SCADA.AI.E119LS__LS2AI11']) / 10 }}</span> %</p>
                  <p class="marginBottomS">二号压缩机当前容量百分比 <span class="color-darkblue">{{ Number(websockVarData['SCADA.AI.E119LS__LS2AI12']) / 10 }}</span> %</p>
                </el-col>
              </el-row>
              <el-divider content-position="left">设备控制</el-divider>
              <el-button type="warning" icon="el-icon-refresh-left" size="small" v-has="['系统监控操作控制']" @click="faultReset('LS2')">故障复位</el-button>
              <el-button slot="reference" style="position:absolute;top: 735px;left: 65px;" size="small">机组信息</el-button>
            </el-popover>
            <el-popover placement="right" title="冷水机组2" width="240" trigger="click" v-has="['系统监控操作控制']">
              <el-button type="success" icon="el-icon-success" size="small" @click="runControl('LS2','RUN')">开启</el-button>
              <el-button type="info" icon="el-icon-error" size="small" @click="runControl('LS2','STOP')">关闭</el-button>
              <div slot="reference" class="jz" style="top: 625px;left: 55px;"></div>
            </el-popover>
            <el-popover placement="right" title="冷却泵1" width="240" trigger="click" v-has="['系统监控操作控制']">
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
            <el-popover placement="right" title="冷却泵2" width="240" trigger="click" v-has="['系统监控操作控制']">
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
            <el-popover placement="right" title="冷冻泵1" width="240" trigger="click" v-has="['系统监控操作控制']">
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
            <el-popover placement="right" title="冷冻泵2" width="240" trigger="click" v-has="['系统监控操作控制']">
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
            <div class="wd" style="top: 368px;left: 148px;">{{ Number(websockVarData['SCADA.AI.E119LS__LS1AI08']) / 10 }}°C</div>
            <div class="wd" style="top: 362px;left: 267px;">{{ Number(websockVarData['SCADA.AI.E119LS__LS1AI09']) / 10 }}°C</div>
            <div class="wd" style="top: 450px;left: 293px;">{{ Number(websockVarData['SCADA.AI.E119LS__LS2AI09']) / 10 }}°C</div>
            <div class="wd" style="top: 568px;left: 148px;">{{ Number(websockVarData['SCADA.AI.E119LS__LS2AI08']) / 10 }}°C</div>
            <div class="wd" style="top: 580px;left: 349px;">{{ Number(websockVarData['SCADA.AI.E119LS__LS1AI01']) / 10 }}°C</div>
            <div class="wd" style="top: 748px;left: 188px;">{{ Number(websockVarData['SCADA.AI.E119LS__LS2AI01']) / 10 }}°C</div>
            <div class="wd" style="top: 788px;left: 352px;">{{ Number(websockVarData['SCADA.AI.E119LS__LS1AI07']) / 10 }}°C</div>
            <div class="wd" style="top: 855px;left: 292px;">{{ Number(websockVarData['SCADA.AI.E119LS__LS2AI07']) / 10 }}°C</div>
            <div class="wd" style="top: 342px;left: 512px;">{{ Number(websockVarData['SCADA.AI.E119LQ__LQ1AIFR']) / 10 }}HZ</div>
            <div class="wd" style="top: 430px;left: 512px;">{{ Number(websockVarData['SCADA.AI.E119LQ__LQ2AIFR']) / 10 }}HZ</div>
            <div class="wd" style="top: 755px;left: 538px;">{{ Number(websockVarData['SCADA.AI.E119LD__LD1AIFR']) / 10 }}HZ</div>
            <div class="wd" style="top: 845px;left: 538px;">{{ Number(websockVarData['SCADA.AI.E119LD__LD2AIFR']) / 10 }}HZ</div>

            <div class="wd" style="top: 125px;left: 960px;">{{ Number(websockVarData['SCADA.AI.E119SDF_SDF1AIOC']) / 10 }}%</div>
            <div class="wd" style="top: 242px;left: 960px;">{{ Number(websockVarData['SCADA.AI.E119KT__KT1AIFR']) / 10 }}HZ</div>
            <div class="wd" style="top: 125px;left: 1050px;">{{ Number(websockVarData['SCADA.AI.E119SDF_SDF2AIOC']) / 10 }}%</div>
            <div class="wd" style="top: 242px;left: 1050px;">{{ Number(websockVarData['SCADA.AI.E119KT__KT2AIFR']) / 10 }}HZ</div>
          </div>
        </el-col>
        <el-col :span="24" style="background: #34383E;overflow: hidden;position: relative;" v-if="TabControl.TabControlCurrent === '设备房温度'">
          <div class="MainContain BorderRadius4 eqSysMonbg" @mousedown="move" data-move>
            <div class="eqhouse" style="top: 250px;left: 59px;">{{ Number(websockVarData['SCADA.AI.E119HTS_HN1AIWD']) / 10 }}°C</div>
            <div class="eqhouse" style="top: 250px;left: 420px;">{{ Number(websockVarData['SCADA.AI.E119HTS_HN14AIWD']) / 10 }}°C</div>
            <div class="eqhouse" style="top: 250px;left: 775px;">{{ Number(websockVarData['SCADA.AI.E119HTS_HN3AIWD']) / 10 }}°C</div>
            <div class="eqhouse" style="top: 250px;left: 1138px;">{{ Number(websockVarData['SCADA.AI.E119HTS_HN5AIWD']) / 10 }}°C</div>
            <div class="eqhouse" style="top: 624px;left: 59px;">{{ Number(websockVarData['SCADA.AI.E119HTS_HN13AIWD']) / 10 }}°C</div>
            <div class="eqhouse" style="top: 624px;left: 420px;">{{ Number(websockVarData['SCADA.AI.E119HTS_HN4AIWD']) / 10 }}°C</div>
            <div class="eqhouse" style="top: 624px;left: 775px;">{{ Number(websockVarData['SCADA.AI.E119HTS_HN6AIWD']) / 10 }}°C</div>
            <div class="eqhouse" style="top: 624px;left: 1138px;">{{ Number(websockVarData['SCADA.AI.E119HTS_HN7AIWD']) / 10 }}°C</div>
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
            {name:"冷水系统"},
            {name:"设备房温度"},
          ],
        },
        websock:null,
        websockVarData:{},
        LS1Bit:"",
        LS2Bit:"",
        LST1Bit:"",
        LST2Bit:"",
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
        this.websockVarData = JSON.parse(e.data)
        this.LS1Bit = parseInt(this.websockVarData["PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_108"],10).toString(2).split("")
        this.LS2Bit = parseInt(this.websockVarData["PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_111"],10).toString(2).split("")
        this.LST1Bit = parseInt(this.websockVarData["PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_127"],10).toString(2).split("")
        this.LST2Bit = parseInt(this.websockVarData["PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_128"],10).toString(2).split("")
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
        this.$confirm('您是否要对'+value+'执行'+type+'操作', '提示', {
          distinguishCancelAndClose:true,
          center:true,
          type: 'warning'
        }).then(()  => {
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
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消操作'
          });
        });
      },
      editHZ(value,HZ){
        this.$confirm('您是否要对'+value+'的频率进行修改', '提示', {
          distinguishCancelAndClose:true,
          center:true,
          type: 'warning'
        }).then(()  => {
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
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消操作'
          });
        });
      },
      faultReset(value){
        this.$confirm('您是否要对'+value+'进行故障复位', '提示', {
          distinguishCancelAndClose:true,
          center:true,
          type: 'warning'
        }).then(()  => {
          this.axios.post("/api/fault",{
            params: {
              EquipmentCode:value,
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
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消操作'
          });
        });
      },
      changeConservationSwitch(){
        var SwitchState = ""
        var SwitchParams = ""
        if(this.websockVarData['LS_JN_FLAG'] === "1"){
          SwitchState = "开"
          SwitchParams = "on"
          this.websockVarData['LS_JN_FLAG'] = "0"
        }else if(this.websockVarData['LS_JN_FLAG'] === "0"){
          SwitchState = "关"
          SwitchParams = "off"
          this.websockVarData['LS_JN_FLAG'] = "1"
        }
        this.$confirm('您是否要进行'+ SwitchState +'节能模式的操作？', '提示', {
          distinguishCancelAndClose:true,
          center:true,
          type: 'warning'
        }).then(()  => {
          var params = {
              switch:SwitchParams,
            }
          this.axios.post("/api/reset",this.qs.stringify(params)).then(res =>{
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
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消操作'
          });
        });
      },
      startReseting(){
        this.$confirm('您确认要复位吗？', '提示', {
          distinguishCancelAndClose:true,
          center:true,
          type: 'warning'
        }).then(()  => {
          var params = {
              reset:"yes",
            }
          this.axios.post("/api/reset",this.qs.stringify(params)).then(res =>{
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
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消操作'
          });
        });
      }
    }
  }
</script>
<style>

</style>
