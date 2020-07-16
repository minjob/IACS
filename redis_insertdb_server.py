#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
import base64
import hashlib
import time
import redis
from flask import Blueprint, render_template, request, make_response
import json
import datetime
from sqlalchemy import desc
from dbset.database.db_operate import db_session,pool
from dbset.main.BSFramwork import AlchemyEncoder
from flask_login import login_required, logout_user, login_user,current_user,LoginManager
import arrow
from models.SystemManagement.core import RedisKey, TagClassType, ElectricEnergy, Unit, SteamEnergy, \
    WaterEnergy, TagDetail, Equipment
from models.SystemManagement.system import EarlyWarningLimitMaintain, EarlyWarning, EarlyWarningPercentMaintain, \
    ElectricPrice, WaterSteamPrice
from tools.common import insert,delete,update
from dbset.database import constant
from dbset.log.BK2TLogger import logger,insertSyslog

pool = redis.ConnectionPool(host=constant.REDIS_HOST)
def run():
    runcount = 0
    failcount = 0
    redis_conn = redis.Redis(connection_pool=pool, password=constant.REDIS_PASSWORD, decode_responses=True)
    redis_conn.hset(constant.REDIS_TABLENAME, "redis_insertdb_server_start",
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    while True:
        time.sleep(180)
        print("Redis数据开始写入数据库")
        # a = arrow.now()
        # currentyear = str(a.shift(years=0))[0:4]
        # currentmonth = str(a.shift(years=0))[0:7]
        # currentday = str(a.shift(days=0))[0:10]
        keys = db_session.query(TagDetail).filter(TagDetail.TagClassValue != None).all()
        for key in keys:
            try:
                k = key.TagClassValue[0:1]
                if k == "E":
                    ZGL = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "_ZGL"))
                    ZGLSamptime = returnb(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "_ZGL_Samptime"))
                    esamptime = db_session.query(ElectricEnergy.CollectionDate).filter(ElectricEnergy.TagClassValue == key.TagClassValue, ElectricEnergy.CollectionDate == ZGLSamptime).order_by(desc("CollectionDate")).first()
                    if esamptime is None and ZGL != 0.0:
                        AU = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "_AU"))
                        AI = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "_AI"))
                        BU = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "_BU"))
                        BI = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "_BI"))
                        CU = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "_CU"))
                        CI = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "_CI"))
                        ele = db_session.query(ElectricEnergy).filter(ElectricEnergy.TagClassValue == key.TagClassValue).order_by(desc("CollectionDate")).first()
                        unit = db_session.query(Unit.UnitValue).filter(Unit.UnitName == "电").first()
                        # equip = db_session.query(TagClassType.EquipmnetID).filter(TagClassType.TagClassValue == key.TagClassValue).first()
                        timeprices = db_session.query(ElectricPrice).filter(ElectricPrice.PriceType == "电",
                                                                            ElectricPrice.IsEnabled == "是").all()
                        PriceID = 0
                        for timeprice in timeprices:
                            if PriceID != 0:
                                continue
                            nowtime = time.strptime(ZGLSamptime, '%Y-%m-%d %H:%M:%S')
                            nowint = int(time.mktime(nowtime))  # 当前时间
                            ststr = ZGLSamptime[0:11] + timeprice.StartTime
                            endstr = ZGLSamptime[0:11] + timeprice.EndTime
                            sttimeArray = time.strptime(ststr, '%Y-%m-%d %H:%M')
                            endtimeArray = time.strptime(endstr, '%Y-%m-%d %H:%M')
                            sttime = int(time.mktime(sttimeArray))
                            endtime = int(time.mktime(endtimeArray))
                            if timeprice.EndTime == "00:00":
                                # 如果结束时间小于开始时间，说明已经跨天，往后加一天再比大小
                                sampday = datetime.datetime.strptime(ZGLSamptime, '%Y-%m-%d %H:%M:%S')
                                cuday = str(sampday + datetime.timedelta(days=1))[0:10]
                                endstr = cuday + " " + timeprice.EndTime
                                endArray = time.strptime(endstr, '%Y-%m-%d %H:%M')
                                endtime = int(time.mktime(endArray))
                            if sttime < nowint < endtime:
                                PriceID = timeprice.ID
                        el = ElectricEnergy()
                        el.TagClassValue = key.TagClassValue
                        el.CollectionYear = ZGLSamptime[0:4]
                        el.CollectionMonth = ZGLSamptime[0:7]
                        el.CollectionDay = ZGLSamptime[0:10]
                        el.ZGL = ZGL
                        el.AU = AU
                        el.AI = AI
                        el.BU = BU
                        el.BI = BI
                        el.CU = CU
                        el.CI = CI
                        el.CollectionDate = ZGLSamptime
                        el.Unit = unit[0]
                        # el.EquipmnetID = equip[0]
                        el.PriceID = PriceID
                        db_session.query(ElectricEnergy)
                        if ele:
                            el.PrevID = ele.ID
                        el.AreaName = key.AreaName
                        el.IncrementFlag = "0"
                        db_session.add(el)
                        db_session.commit()
                        # 实时预电压电流故障
                        if AU == 0.0 or BU == 0.0 or CU == 0.0:
                            earw = EarlyWarning()
                            earw.TagClassValue = key.TagClassValue
                            earw.AreaName = key.AreaName
                            EQPName = db_session.query(TagClassType).filter(
                                TagClassType.TagClassValue == key.TagClassValue).first()
                            if EQPName != None:
                                EQPName = EQPName[0]
                            else:
                                EQPName = ""
                            earw.EQPName = EQPName
                            earw.WarningType = "三相电压中缺相"
                            earw.WarningDate = ZGLSamptime
                            db_session.commit()
                        else:
                            avgI_list = [AI,BI,CI]
                            avgc = max(avgI_list) - min(avgI_list)
                            if avgc > 0:
                                percentI = 100*(avgc/max(avgI_list))
                            EQPName = db_session.query(TagClassType).filter(
                                TagClassType.TagClassValue == key.TagClassValue).first()
                            if EQPName != None:
                                EQPName = EQPName[0]
                            else:
                                EQPName = ""
                            percent = db_session.query(EarlyWarningPercentMaintain.Percent).filter(EarlyWarningPercentMaintain.AreaName == key.AreaName,
                                EarlyWarningPercentMaintain.EQPName == EQPName).first()
                            if percent != None:
                                percent = percent[0]
                                if percentI > percent:
                                    earw = EarlyWarning()
                                    earw.TagClassValue = key.TagClassValue
                                    earw.AreaName = key.AreaName
                                    earw.EQPName = EQPName
                                    earw.WarningType = "三相电流不平衡"
                                    earw.WarningDate = ZGLSamptime
                                    db_session.commit()
                    else:
                        continue
                elif k == "S":
                    valueWD = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "WD"))  # 蒸汽温度
                    #实时预警判断温度是否达到设定值
                    warn = db_session.query(EarlyWarningLimitMaintain).filter(EarlyWarningLimitMaintain.AreaName == key.AreaName,
                                                                              EarlyWarningLimitMaintain.EnergyClass == key.EnergyClass).first()
                    if warn is not None:
                        if valueWD < warn.LowerLimit or valueWD > warn.UpperLimit:
                            earw = EarlyWarning()
                            earw.TagClassValue = key.TagClassValue
                            earw.AreaName = key.AreaName
                            EQPName = db_session.query(TagClassType).filter(TagClassType.TagClassValue == key.TagClassValue).first()
                            if EQPName != None:
                                EQPName = EQPName[0]
                            else:
                                EQPName = ""
                            earw.EQPName = EQPName
                            if valueWD < warn.LowerLimit:
                                earw.WarningType = "温度低于最低限值"
                            if valueWD > warn.UpperLimit:
                                earw.WarningType = "温度高于最高限值"
                            db_session.commit()
                    valueF = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "F"))  # 蒸汽瞬时流量
                    valueS = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "S"))  # 蒸汽累计流量
                    Volume = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "V"))  # 蒸汽体积
                    valueSSamptime = returnb(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "_Samptime"))  # 蒸汽累计流量采集时间
                    ssamptime = db_session.query(SteamEnergy.CollectionDate).filter(SteamEnergy.TagClassValue == key.TagClassValue, SteamEnergy.CollectionDate == valueSSamptime).order_by(desc("CollectionDate")).first()
                    if ssamptime is None and valueS != 0.0:
                        ste = db_session.query(SteamEnergy).filter(SteamEnergy.TagClassValue == key.TagClassValue).order_by(desc("CollectionDate")).first()
                        unitf = db_session.query(Unit.UnitValue).filter(Unit.UnitName == "汽瞬时流量单位").first()
                        units = db_session.query(Unit.UnitValue).filter(Unit.UnitName == "汽累计量体积单位").first()
                        # equip = db_session.query(TagClassType.EquipmnetID).filter(TagClassType.TagClassValue == key.TagClassValue).first()
                        price = db_session.query(WaterSteamPrice.ID).filter(WaterSteamPrice.PriceType == "汽",
                                                                          WaterSteamPrice.IsEnabled == "是").first()
                        PriceID = 0
                        if price:
                            PriceID = price[0]
                        sl = SteamEnergy()
                        sl.TagClassValue = key.TagClassValue
                        sl.CollectionYear = valueSSamptime[0:4]
                        sl.CollectionMonth = valueSSamptime[0:7]
                        sl.CollectionDay = valueSSamptime[0:10]
                        sl.WD = valueWD
                        sl.FlowValue = valueF
                        sl.SumValue = valueS
                        sl.CollectionDate = valueSSamptime
                        sl.FlowUnit = unitf[0]
                        sl.SumUnit = units[0]
                        # sl.EquipmnetID = equip[0]
                        sl.PriceID = PriceID
                        sl.Volume = Volume
                        if ste:
                            sl.PrevID = ste.ID
                        sl.IncrementFlag = "0"
                        sl.insertVolumeFlag = "0"
                        sl.AreaName = key.AreaName
                        db_session.add(sl)
                        db_session.commit()
                elif k == "W":
                    valueS = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "S"))  # 水的累计流量
                    valueF = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "F"))  # 水的瞬时流量
                    valueSSamptime = returnb(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "_Samptime"))  # 水的累计流量
                    wsamptime = db_session.query(SteamEnergy.CollectionDate).filter(SteamEnergy.CollectionDate == key.TagClassValue, SteamEnergy.CollectionDate == valueSSamptime).order_by(desc("CollectionDate")).first()
                    if valueS != 0.0 and wsamptime is None:
                        wat = db_session.query(WaterEnergy).filter(WaterEnergy.TagClassValue == key.TagClassValue).order_by(desc("CollectionDate")).first()
                        unitf = db_session.query(Unit.UnitValue).filter(Unit.UnitName == "水瞬时流量单位").first()
                        units = db_session.query(Unit.UnitValue).filter(Unit.UnitName == "水累计量体积单位").first()
                        # equip = db_session.query(TagClassType.EquipmnetID).filter(TagClassType.TagClassValue == key.TagClassValue).first()
                        price = db_session.query(WaterSteamPrice).filter(WaterSteamPrice.PriceType == key.FEFportIP[0:-1],
                                                                          WaterSteamPrice.IsEnabled == "是").first()
                        PriceID = 0
                        if price:
                            PriceID = price.ID
                        wa = WaterEnergy()
                        wa.TagClassValue = key.TagClassValue
                        wa.CollectionYear = valueSSamptime[0:4]
                        wa.CollectionMonth = valueSSamptime[0:7]
                        wa.CollectionDay = valueSSamptime[0:10]
                        wa.WaterFlow = valueF
                        wa.WaterSum = valueS
                        wa.CollectionDate = valueSSamptime
                        wa.FlowWUnit = unitf[0]
                        wa.SumWUnit = units[0]
                        # wa.EquipmnetID = equip[0]
                        wa.PriceID = PriceID
                        if wat:
                            wa.PrevID = wat.ID
                        wa.IncrementFlag = "0"
                        wa.AreaName = key.AreaName
                        db_session.add(wa)
                        db_session.commit()
                runcount = runcount + 1
            except Exception as e:
                print("报错tag："+key.TagClassValue+" |报错IP："+key.IP+"  |报错端口："+key.COMNum+"  |错误："+str(e))
                logger.error(e)
                insertSyslog("error", "实时数据写入DB报错Error：" + str(e),"")
                redis_conn.hset(constant.REDIS_TABLENAME, "redis_insertdb_server_status", "执行失败")
                failcount = failcount + 1
            finally:
                pass
        print("Redis数据开始写入数据库结束")
        redis_conn.hset(constant.REDIS_TABLENAME, "redis_insertdb_server_end",
                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        redis_conn.hset(constant.REDIS_TABLENAME, "redis_insertdb_server_runcount", str(runcount))
        redis_conn.hset(constant.REDIS_TABLENAME, "redis_insertdb_server_failcount", str(failcount))
        redis_conn.hset(constant.REDIS_TABLENAME, "redis_insertdb_server_status", "执行成功")

def roundtwo(rod):
    if rod == None or rod == "" or rod == b'':
        return 0.0
    else:
        if float(rod) < 0:
            return round(abs(float(rod)), 2)
        return round(float(rod), 2)
def returnb(rod):
    if rod == None or rod == "" or rod == b'':
        return ""
    else:
        return rod.decode()
if __name__ == '__main__':
    run()