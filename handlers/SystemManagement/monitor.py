import json
import time

import redis
from flask import Blueprint, request
from flask_login import current_user
from opcua import ua, Client

from dbset.database import constant
from dbset.main.BSFramwork import AlchemyEncoder
from dbset.database.db_operate import db_session
from models.system import Schedulelqt
from tools.common import logger, insertSyslog

opc = Blueprint('opc', __name__)


def count_time(start_time, end_time, new_start, new_end):
    t1 = [start_time, end_time]
    t2 = [new_start, new_end]
    return t1[0] < t2[0] < t2[1] < t1[1]


class ScheduleCTRLWORD(object):
    """
    RuleBasic定义
    """

    def __init__(self, AName):
        '''
        :param tagID: 要采集的变量名称
        :param src: 数据源,为dict类型
        '''
        self._redispool = redis.ConnectionPool(host=constant.REDIS_HOST, password=constant.REDIS_PASSWORD)
        self._name = AName
        self._ls1ctrlword = 0
        self._lq1pv = 40
        self._ld1pv = 50
        self._ls2ctrlword = 0
        self._lq2pv = 49
        self._ld2pv = 40
        self._kt1pv = 30
        self._kt2pv = 30
        self._kt1vopen = 50
        self._kt2vopen = 50
        self._ls1_run = 0
        self._ls1_stop = 0
        self._lqt1_run = 0
        self._lqt1_stop = 0
        self._ld1_run = 0
        self._ld1_stop = 0
        self._ls2_run = 0
        self._ls2_stop = 0
        self._lqt2_run = 0
        self._lqt2_stop = 0
        self._ld2_run = 0
        self._ld2_stop = 0
        self._ls1_wd = 10
        self._ls2_wd = 10
        self._ls1_net = 1
        self._ls2_net = 1
        self._connected = False
        self._client = None
        self._nodels1 = None
        self._nodeld1pv = None
        self._nodelq1pv = None
        self._nodels2 = None
        self._nodeld2pv = None
        self._nodelq2pv = None
        self._nodekt1pv = None
        self._nodekt2pv = None
        self._nodekt1vpv = None
        self._nodekt2vpv = None
        self.INI_CTRL_WORD()

    def INI_CTRL_WORD(self):
        # client = Client('opc.tcp://127.0.0.1:49320')
        self.connect()
        self._nodels1 = self._client.get_node('ns = 2;s = SCADA.DO.TSET1')
        self._nodeld1pv = self._client.get_node('ns = 2;s = SCADA.DO.LD1SET')
        self._nodelq1pv = self._client.get_node('ns = 2;s = SCADA.DO.LQ1SET')
        self._nodels2 = self._client.get_node('ns = 2;s = SCADA.DO.TSET2')
        self._nodeld2pv = self._client.get_node('ns = 2;s = SCADA.DO.LD2SET')
        self._nodelq2pv = self._client.get_node('ns = 2;s = SCADA.DO.LQ2SET')
        self._nodekt1pv = self._client.get_node('ns = 2;s = SCADA.DO.KT1SET')
        self._nodekt2pv = self._client.get_node('ns = 2;s = SCADA.DO.KT2SET')
        self._nodekt1vpv = self._client.get_node('ns = 2;s = SCADA.DO.SDF1SET')
        self._nodekt2vpv = self._client.get_node('ns = 2;s = SCADA.DO.SDF2SET')

    def Write_LS1_CTRLWord(self):
        # client = Client('opc.tcp://127.0.0.1:49320')
        try:
            self.connect()
            ls1ctrl = self.GetCtrlWord(self._ls1_wd, self._ls1_run, self._ls1_stop, self._ld1_run, self._ld1_stop,
                                       self._lqt1_run, self._lqt1_stop)
            self._nodels1.set_value(ua.DataValue(ua.Variant(ls1ctrl, ua.VariantType.UInt16)))
        except Exception as err:
            print(err)
            pass

    def Equip_LS1Control(self, AEquip, AType):
        # client = Client('opc.tcp://127.0.0.1:49320')
        try:
            self.connect()
            self._ls1_run = 0
            self._ls1_stop = 0
            self._ld1_run = 0
            self._ld1_stop = 0
            self._lqt1_run = 0
            self._lqt1_stop = 0
            if ((AEquip == "LS1") and (AType == "RUN")):
                self._ls1_run = 1
            elif ((AEquip == "LS1") and (AType == "STOP")):
                self._ls1_stop = 1
            elif ((AEquip == "LD1") and (AType == "RUN")):
                self._ld1_run = 1
            elif ((AEquip == "LD1") and (AType == "STOP")):
                self._ld1_stop = 1
            elif ((AEquip == "LQT1") and (AType == "RUN")):
                self._lqt1_run = 1
            elif ((AEquip == "LQT1") and (AType == "STOP")):
                self._lqt1_stop = 1
            ls1ctrl = self.GetCtrlWord(int(100), self._ls1_run, self._ls1_stop, self._ld1_run, self._ld1_stop,
                                       self._lqt1_run, self._lqt1_stop)
            self._nodels1.set_value(ua.DataValue(ua.Variant(ls1ctrl, ua.VariantType.UInt16)))
        except Exception as err:
            print(err)
            pass

    def Write_LS1_Params(self, AEquipment, AValue):
        # client = Client('opc.tcp://127.0.0.1:49320')
        try:
            self.connect()
            if (AEquipment == "LD1"):
                self._ld1pv = int(AValue)
                self._nodeld1pv.set_value(ua.DataValue(ua.Variant(10 * int(self._ld1pv), ua.VariantType.UInt16)))
            elif (AEquipment == "LQ1"):
                self._lq1pv = int(AValue)
                self._nodelq1pv.set_value(ua.DataValue(ua.Variant(10 * int(self._lq1pv), ua.VariantType.UInt16)))
            # self._nodekt1pv.set_value(ua.DataValue(ua.Variant(10*int(self._kt1pv),ua.VariantType.UInt16)))
            # self._nodekt2pv.set_value(ua.DataValue(ua.Variant(10*int(self._kt2pv),ua.VariantType.UInt16)))
            # self._nodekt1vpv.set_value(ua.DataValue(ua.Variant(10*int(self._kt1vopen),ua.VariantType.UInt16)))
            # self._nodekt2vpv.set_value(ua.DataValue(ua.Variant(10*int(self._kt2vopen),ua.VariantType.UInt16)))
        except Exception as err:
            print(err)
            pass

    def Equip_LS2Control(self, AEquip, AType):
        # client = Client('opc.tcp://127.0.0.1:49320')
        try:
            self.connect()
            self._ls2_run = 0
            self._ls2_stop = 0
            self._ld2_run = 0
            self._ld2_stop = 0
            self._lqt2_run = 0
            self._lqt2_stop = 0
            if ((AEquip == "LS2") and (AType == "RUN")):
                self._ls2_run = 1
            elif ((AEquip == "LS2") and (AType == "STOP")):
                self._ls2_stop = 1
            elif ((AEquip == "LD2") and (AType == "RUN")):
                self._ld2_run = 1
            elif ((AEquip == "LD2") and (AType == "STOP")):
                self._ld2_stop = 1
            elif ((AEquip == "LQT2") and (AType == "RUN")):
                self._lqt2_run = 1
            elif ((AEquip == "LQT2") and (AType == "STOP")):
                self._lqt2_stop = 1
            ls2ctrl = self.GetCtrlWord(int(100), self._ls2_run, self._ls2_stop, self._ld2_run, self._ld2_stop,
                                       self._lqt2_run, self._lqt2_stop)
            self._nodels2.set_value(ua.DataValue(ua.Variant(ls2ctrl, ua.VariantType.UInt16)))
        except Exception as err:
            print(err)
            pass

    def Write_LS2_Params(self, AEquipment, AValue):
        # client = Client('opc.tcp://127.0.0.1:49320')
        try:
            self.connect()
            if (AEquipment == "LD2"):
                self._ld2pv = int(AValue)
                self._nodeld2pv.set_value(ua.DataValue(ua.Variant(10 * int(self._ld2pv), ua.VariantType.UInt16)))
            elif (AEquipment == "LQ2"):
                self._lq2pv = int(AValue)
                self._nodelq2pv.set_value(ua.DataValue(ua.Variant(10 * int(self._lq2pv), ua.VariantType.UInt16)))
            # self._nodekt1pv.set_value(ua.DataValue(ua.Variant(10*int(self._kt1pv),ua.VariantType.UInt16)))
            # self._nodekt2pv.set_value(ua.DataValue(ua.Variant(10*int(self._kt2pv),ua.VariantType.UInt16)))
            # self._nodekt1vpv.set_value(ua.DataValue(ua.Variant(10*int(self._kt1vopen),ua.VariantType.UInt16)))
            # self._nodekt2vpv.set_value(ua.DataValue(ua.Variant(10*int(self._kt2vopen),ua.VariantType.UInt16)))
        except Exception as err:
            print(err)
            pass

    def connect(self):
        self.disconnect()
        self._client = Client('opc.tcp://127.0.0.1:49320')
        self._client.connect()
        self._nodels1 = self._client.get_node('ns = 2;s = SCADA.DO.TSET1')
        self._nodeld1pv = self._client.get_node('ns = 2;s = SCADA.DO.LD1SET')
        self._nodelq1pv = self._client.get_node('ns = 2;s = SCADA.DO.LQ1SET')
        self._nodels2 = self._client.get_node('ns = 2;s = SCADA.DO.TSET2')
        self._nodeld2pv = self._client.get_node('ns = 2;s = SCADA.DO.LD2SET')
        self._nodelq2pv = self._client.get_node('ns = 2;s = SCADA.DO.LQ2SET')
        self._nodekt1pv = self._client.get_node('ns = 2;s = SCADA.DO.KT1SET')
        self._nodekt2pv = self._client.get_node('ns = 2;s = SCADA.DO.KT2SET')
        self._nodekt1vpv = self._client.get_node('ns = 2;s = SCADA.DO.SDF1SET')
        self._nodekt2vpv = self._client.get_node('ns = 2;s = SCADA.DO.SDF2SET')
        self._connected = True

    def disconnect(self):
        if self._connected:
            print("Disconnecting from server")
            self._connected = False
            try:
                self._client.disconnect()
            finally:
                self._reset()

    def _reset(self):
        self.client = None
        self._connected = False

    def Write_LS2_CTRLWord(self):
        # client = Client('opc.tcp://127.0.0.1:49320')
        try:
            self.connect()
            ls2ctrl = self.GetCtrlWord(self._ls2_wd, self._ls2_run, self._ls2_stop, self._ld2_run, self._ld2_stop,
                                       self._lqt2_run, self._lqt2_stop)
            self._nodels2 = self._client.get_node('ns = 2;s = SCADA.DO.TSET2')
            self._nodels2.set_value(ua.DataValue(ua.Variant(ls2ctrl, ua.VariantType.UInt16)))
        except Exception as err:
            print(err)
            pass

    def GetCtrlWord(self, AOutTemp, ALSRun, ALSSTOP, ALDRun, ALDSTOP, ALQT_T1_RUN, ALQT_T1_STOP):
        if int(AOutTemp) > 30:
            int_num = int(AOutTemp)
        else:
            int_num = int(AOutTemp)
        bin_num = bin(int_num)
        slow = str(bin_num)[2:]
        if len(slow) == 1:
            slow = '0000000' + slow
        elif len(slow) == 2:
            slow = '000000' + slow
        elif len(slow) == 3:
            slow = '00000' + slow
        elif len(slow) == 4:
            slow = '0000' + slow
        elif len(slow) == 5:
            slow = '000' + slow
        elif len(slow) == 6:
            slow = '00' + slow
        elif len(slow) == 7:
            slow = '0' + slow

        shigh = ''
        # 第8位
        if ALSRun == 1:
            shigh = '01'
        # 第9位
        elif ALSSTOP == 1:
            shigh = '10'
        elif (ALSRun == 0) and (ALSSTOP == 0):
            shigh = '00'

        if ALDRun == 1:
            shigh = "01" + shigh
        elif ALDSTOP == 1:
            shigh = '10' + shigh
        elif (ALDRun == 0) and (ALDSTOP == 0):
            shigh = '00' + shigh
            # 第12位
        if ALQT_T1_RUN == 1:
            shigh = '01' + shigh
        elif ALQT_T1_STOP == 1:
            shigh = '10' + shigh
        elif (ALQT_T1_RUN == 0) and (ALQT_T1_RUN == 0):
            shigh = '00' + shigh

        shigh = '00' + shigh
        print("字符串" + shigh + slow + ":整型:" + str(int(shigh + slow, 2)))
        return int(shigh + slow, 2)

    def Write_LS_INIWORD(self, AEquip, AWD):
        # client = Client('opc.tcp://127.0.0.1:49320')
        try:
            self.connect()
            lsctrl = self.GetCtrlWord(int(AWD), 0, 0, 0, 0, 0, 0)
            if AEquip == "LS1":
                self._nodels1 = self._client.get_node('ns = 2;s = SCADA.DO.TSET1')
                self._nodels1.set_value(ua.DataValue(ua.Variant(lsctrl, ua.VariantType.UInt16)))
            elif AEquip == "LS2":
                self._nodels2 = self._client.get_node('ns = 2;s = SCADA.DO.TSET2')
                self._nodels2.set_value(ua.DataValue(ua.Variant(lsctrl, ua.VariantType.UInt16)))
        except Exception as err:
            print(err)
            pass

    def GetFaultCtrlWord(self, AOutTemp, AFault):
        if int(AOutTemp) > 30:
            int_num = int(AOutTemp)
        else:
            int_num = int(AOutTemp)
        bin_num = bin(int_num)
        slow = str(bin_num)[2:]
        if len(slow) == 1:
            slow = '0000000' + slow
        elif len(slow) == 2:
            slow = '000000' + slow
        elif len(slow) == 3:
            slow = '00000' + slow
        elif len(slow) == 4:
            slow = '0000' + slow
        elif len(slow) == 5:
            slow = '000' + slow
        elif len(slow) == 6:
            slow = '00' + slow
        elif len(slow) == 7:
            slow = '0' + slow

        shigh = '0000000'

        if AFault == 1:
            shigh = '1' + shigh
        else:
            shigh = '0' + shigh

        print("字符串" + shigh + slow + ":整型:" + str(int(shigh + slow, 2)))
        return int(shigh + slow, 2)

    def Write_LS_FaultReset(self, AEquipment):
        # client = Client('opc.tcp://127.0.0.1:49320')
        try:
            self.connect()
            if (AEquipment == "LS1"):
                lsctrl = self.GetFaultCtrlWord(100, 1)
                self._nodels1.set_value(ua.DataValue(ua.Variant(int(lsctrl), ua.VariantType.UInt16)))
                time.sleep(5)
                lsctrl = self.GetFaultCtrlWord(100, 0)
                self._nodels1.set_value(ua.DataValue(ua.Variant(int(lsctrl), ua.VariantType.UInt16)))
            elif (AEquipment == "LS2"):
                lsctrl = self.GetFaultCtrlWord(100, 1)
                self._nodels2.set_value(ua.DataValue(ua.Variant(int(lsctrl), ua.VariantType.UInt16)))
                time.sleep(5)
                lsctrl = self.GetFaultCtrlWord(100, 0)
                self._nodels2.set_value(ua.DataValue(ua.Variant(int(lsctrl), ua.VariantType.UInt16)))
        except Exception as err:
            print(err)
            pass


@opc.route('/fault', methods=['POST'])
def fault():
    """故障恢复"""
    try:
        json_data = request.json.get('params')
        equipment_code = json_data.get('EquipmentCode')
        ctrl = ScheduleCTRLWORD('TY')
        ctrl.Write_LS_FaultReset(equipment_code)
        return json.dumps({'code': '20001', 'message': '操作成功'}, cls=AlchemyEncoder, ensure_ascii=False)
    except Exception as e:
        logger.error(e)
        insertSyslog("error", "故障恢复错误：" + str(e), current_user.Name)
        return json.dumps({'code': '20002', 'message': str(e)}, cls=AlchemyEncoder, ensure_ascii=False)


@opc.route('/run', methods=['POST'])
def change_run():
    """修改机组开关"""
    try:
        json_data = request.json.get('params')
        equipment_code = json_data.get('EquipmentCode')
        status = json_data.get('Status')
        temperature = json_data.get('Temperature', '100')
        ctrl = ScheduleCTRLWORD('TY')
        if equipment_code in ['LS1', 'LD1', 'LQT1']:
            if equipment_code == 'LS1' and status == 'STOP':
                ctrl.Equip_LS1Control(equipment_code, status)
                ctrl.Write_LS_INIWORD(equipment_code, temperature)
            else:
                ctrl.Equip_LS1Control(equipment_code, status)
        if equipment_code in ['LS2', 'LD2', 'LQT2']:
            if equipment_code == 'LS2' and status == 'STOP':
                ctrl.Equip_LS2Control(equipment_code, status)
                ctrl.Write_LS_INIWORD(equipment_code, temperature)
            else:
                ctrl.Equip_LS2Control(equipment_code, status)
        insertSyslog("机组开关操作", f"对{equipment_code}设备进行了{status}操作", current_user.Name)
        return json.dumps({'code': '20001', 'message': '操作成功'}, cls=AlchemyEncoder, ensure_ascii=False)
    except Exception as e:
        logger.error(e)
        insertSyslog("error", "机组开关修改错误：" + str(e), current_user.Name)
        return json.dumps({'code': '20002', 'message': str(e)}, cls=AlchemyEncoder, ensure_ascii=False)


@opc.route('/status', methods=['POST'])
def change_status():
    """修改机组频率"""
    try:
        json_data = request.json.get('params')
        equipment_code = json_data.get('EquipmentCode')
        hz = json_data.get('HZ')
        ctrl = ScheduleCTRLWORD('TY')
        if equipment_code in ['LD1', 'LQ1']:
            ctrl.Write_LS1_Params(equipment_code, hz)
        elif equipment_code in ['LD2', 'LQ2']:
            ctrl.Write_LS2_Params(equipment_code, hz)
        insertSyslog("频率修改操作", f"将{equipment_code}设备的频率修改为{hz}", current_user.Name)
        return json.dumps({'code': '20001', 'message': '操作成功'}, cls=AlchemyEncoder, ensure_ascii=False)
    except Exception as e:
        logger.error(e)
        insertSyslog("error", "频率修改错误：" + str(e), current_user.Name)
        return json.dumps({'code': '20002', 'message': str(e)}, cls=AlchemyEncoder, ensure_ascii=False)


@opc.route('/schedule_lqt', methods=['POST'])
def schedule_lqt():
    """排班日程"""
    try:
        new_start = request.values.get('start_time')
        new_end = request.values.get('end_time')
        query_list = db_session.query(Schedulelqt).all()
        for item in query_list:
            if not count_time(item.enablestarttime, item.enableendtime, new_start, new_end):
                return json.dumps({'code': '20003', 'message': '工作时间设置出现冲突'})
        data = Schedulelqt(enablestarttime=new_start, enableendtime=new_end, comment=request.values.get('comment'),
                           energystrategyCode=request.values.get('energystrategyCode'),
                           lqt1_allowrun=request.values.get('lqt1'), lqt2_allowrun=request.values.get('lqt2'))
        db_session.add(data)
        db_session.commit()
        db_session.close()
        return json.dumps({'code': '20001', 'message': '设置成功'})
    except Exception as e:
        logger.error(e)
        insertSyslog("error", "工时安排设置出错：" + str(e), current_user.Name)
        return json.dumps({'code': '20002', 'message': str(e)}, cls=AlchemyEncoder, ensure_ascii=False)


@opc.route('/reset', methods=['GET', 'POST'])
def reset():
    """复位"""
    try:
        redis_conn = redis.Redis(password=constant.REDIS_PASSWORD, decode_responses=True)
        if request.method == 'GET':
            data = redis_conn.hget(constant.REDIS_TABLENAME, 'LS_JN_FLAG')
            return json.dumps({'code': '20001', 'message': '成功', 'data': data},
                              cls=AlchemyEncoder, ensure_ascii=False)
        if request.values.get('reset') == 'yes':
            ctrl = ScheduleCTRLWORD('TY')
            ctrl.Write_LS_INIWORD('LS1', '100')
            ctrl.Write_LS_INIWORD('LS2', '100')
            return json.dumps({'code': '20001', 'message': '设置成功'})
        if request.values.get('switch') == 'on':
            data = redis_conn.hset(constant.REDIS_TABLENAME, 'LS_JN_FLAG', '1')
            return json.dumps({'code': '20001', 'message': '设置成功', 'data': data})
        if request.values.get('switch') == 'off':
            data = redis_conn.hset(constant.REDIS_TABLENAME, 'LS_JN_FLAG', '0')
            return json.dumps({'code': '20001', 'message': '设置成功', 'data': data})
    except Exception as e:
        logger.error(e)
        insertSyslog("error", "工时安排设置出错：" + str(e), current_user.Name)
        return json.dumps({'code': '20002', 'message': str(e)}, cls=AlchemyEncoder, ensure_ascii=False)


@opc.route('/energy_trend', methods=['GET'])
def energy_trends():
    """趋势图"""
    try:
        if request.values.get('TagFlag') == 'first':
            # 多个tag点查询一天
            TagCodes = request.values.get('TagCodes').split(",")
            Begin = request.values.get('begin')
            End = request.values.get('end')
            data = []
            for item in TagCodes:
                sql = "select " + "AVG(`" + item + "`)" + "as total_value from datahistory where" \
                      " SampleTime between " + "'" + Begin + "'" + " and " + "'" + End + "'"
                result = db_session.execute(sql).fetchall()
                data.append(round(result[0]['total_value'], 2))
            return json.dumps({'code': '20001', 'message': '成功', 'data': data}, cls=AlchemyEncoder, ensure_ascii=False)
        else:
            # 一个tag查询多天
            # TagCode = request.values.get('TagCode') + "`)"
            PointDates = request.values.get("PointDates").split(",")
            Begin = request.values.get("ParagraBegin")
            End = request.values.get("ParagraEnd")
            data = []
            for item in PointDates:
                start_time = item + " " + Begin
                end_time = item + " " + End
                sql = "select " + "AVG(`" + request.values.get('TagCode') + "`)" + "as total_value from datahistory" \
                      " where SampleTime between " + "'" + start_time + "'" + " and " + "'" + end_time + "'"
                result = db_session.execute(sql).fetchall()
                data.append(round(result[0]['total_value'], 2))
            return json.dumps({'code': '20001', 'message': '成功', 'data': data}, cls=AlchemyEncoder, ensure_ascii=False)
    except Exception as e:
        logger.error(e)
        insertSyslog("error", "energy_trend错误：" + str(e), current_user.Name)
        return json.dumps({'code': '20002', 'message': 'energy_trend错误： ' + str(e)},
                          cls=AlchemyEncoder, ensure_ascii=False)
