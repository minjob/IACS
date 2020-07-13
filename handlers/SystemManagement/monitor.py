import json

import redis
from flask import Blueprint, request
from opcua import ua, Client

from dbset.database import constant
from dbset.main.BSFramwork import AlchemyEncoder
from tools.common import logger, insertSyslog

opc = Blueprint('opc', __name__)


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

        shigh = '10' + shigh
        print("字符串" + shigh + slow + ":整型:" + str(int(shigh + slow, 2)))
        return int(shigh + slow, 2)


@opc.route('/run', methods=['POST'])
def change_run():
    try:
        equipment_code = request.values.get('EquipmentCode')
        status = request.values.get('Status')
        if equipment_code in ['LS1', 'LD1', 'LQT1']:
            ScheduleCTRLWORD().Equip_LS1Control(equipment_code, status)
        elif equipment_code in ['LS2', 'LD2', 'LQT2']:
            ScheduleCTRLWORD().Equip_LS2Control(equipment_code, status)
        return json.dumps({'code': '20001', 'message': '操作成功'}, cls=AlchemyEncoder, ensure_ascii=True)
    except Exception as e:
        logger.error(e)
        insertSyslog("error", "机组开关修改错误：" + str(e))


@opc.route('/change_status', methods=['POST'])
def change_status():
    try:
        equipment_code = request.values.get('EquipmentCode')
        hz = request.values.get('HZ')
        if equipment_code in ['LD1', 'LQ1']:
            ScheduleCTRLWORD().Write_LS1_Params(equipment_code, hz)
        elif equipment_code in ['LD2', 'LQ2']:
            ScheduleCTRLWORD().Write_LS2_Params(equipment_code, hz)
        return json.dumps({'code': '20001', 'message': '操作成功'}, cls=AlchemyEncoder, ensure_ascii=True)
    except Exception as e:
        logger.error(e)
        insertSyslog("error", "频率修改错误：" + str(e))
