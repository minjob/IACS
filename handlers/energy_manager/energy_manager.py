from typing import Optional, Any
from collections import Counter
import time
import xlrd
import xlwt
from flask import Blueprint, render_template, send_from_directory
from openpyxl.compat import file
from sqlalchemy.orm import Session, relationship, sessionmaker
from sqlalchemy import create_engine
from flask import render_template, request, make_response

from dbset.database.constant import myHours
from dbset.database.db_operate import SchedulingStatus, DB_URL
from dbset.main.BSFramwork import AlchemyEncoder
from models.schedul_model import Scheduling, plantCalendarScheduling, product_plan, ERPproductcode_prname, \
    SchedulingStandard, SchedulingStock, scheduledate, TagMaintain, scheduleDateType
from models.system import EquipmentEfficiencyTree, EquipmentStatusCount, Equipment
from tools.MESLogger import MESLogger
import json
import socket
import datetime
from flask_login import login_required, logout_user, login_user,current_user,LoginManager
import re
from sqlalchemy import create_engine, Column, ForeignKey, Table, Integer, String, and_, or_, desc,extract
from io import StringIO
import calendar
from tools.common import logger,insertSyslog,insert,delete,update,select
import os
import openpyxl
import suds
from suds.client import Client
from datetime import timedelta

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
db_session = Session()
energy = Blueprint('energy', __name__, template_folder='templates')

@energy.route('/energytrendtu', methods=['GET', 'POST'])
def energytrendtu():
    '''
    能耗趋势图
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            TagFlag = data.get("TagFlag")
            if TagFlag == "first":
                begin = data.get("begin")
                end = data.get("end")
                TagCodes = data.get("TagCodes")
                TagCodes = TagCodes.split(",")
                tag_str = ""
                for TagCode in TagCodes:
                    if tag_str == "":
                        tag_str =  "`"+TagCode+"` AS "+"`"+TagCode+"`"
                    else:
                        tag_str = tag_str + "," + "`"+TagCode+"` AS "+"`"+TagCode+"`"
                sql = "SELECT  " + tag_str + ",SampleTime AS SampleTime FROM datahistory WHERE SampleTime BETWEEN '"\
                      + begin + "' AND '" + end + "' group by CollectionMinuter order by SampleTime"
                re = db_session.execute(sql).fetchall()
                dict_list = []
                for i in range(len(re)):
                    oc_list = []
                    oc_list.append(datetime.datetime.strftime(re[i]["SampleTime"], '%Y-%m-%d %H:%M:%S')[11:])
                    if re[i]["SampleTime"] is not None:
                        for TagCode in TagCodes:
                            oc_list.append("-" if re[i][TagCode] is None else re[i][TagCode])
                    dict_list.append(oc_list)
            else:
                TagCode = "`"+data.get("TagCode")+"`"
                PointDates = data.get("PointDates")
                PointDates = PointDates.split(",")
                ParagraBegin = data.get("ParagraBegin")
                ParagraEnd = data.get("ParagraEnd")
                parameter_str = ""
                j = 0
                for ponit in PointDates:
                    if j == 0:
                        parameter_str = "SampleTime BETWEEN '" + ponit + " " + ParagraBegin + "' AND '" + ponit + " " + ParagraEnd
                    else:
                        parameter_str = parameter_str + "' OR SampleTime BETWEEN '" + ponit + " " + ParagraBegin + "' AND '" + ponit + " " + ParagraEnd
                    j = j + 1
                parameter_str = parameter_str + "' group by CollectionMinuter order by SampleTime"
                sql = "SELECT  " + TagCode + " AS value,SampleTime AS SampleTime FROM datahistory WHERE " + parameter_str
                re = db_session.execute(sql)
                dict_list = []
                for i in re:
                    oc_list = []
                    oc_list.append(datetime.datetime.strftime(i["SampleTime"], '%Y-%m-%d %H:%M:%S'))
                    if i["SampleTime"] is not None:
                        oc_list.append("-" if i["value"] is None else i["value"])
                        dict_list.append(oc_list)
            return json.dumps(dict_list, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            logger.error(e)
            insertSyslog("error", "能耗趋势图报错Error：" + str(e), current_user.Name)
            return json.dumps("能耗趋势图报错", cls=AlchemyEncoder, ensure_ascii=False)

@energy.route('/energyanalysis', methods=['GET', 'POST'])
def energyanalysis():
    '''
    能耗分析
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            CompareTime = data.get("CompareTime")
            if CompareTime:
                begin = CompareTime + " 00:00:00"
                end = CompareTime + " 23:59:59"
                beginnow = datetime.datetime.now().strftime("%Y-%m-%d") + " 00:00:00"
                endnow = datetime.datetime.now().strftime("%Y-%m-%d") + " 23:59:59"
                tag_str = "SUM(`MB2TCP3.A_ACR_12.Ep_total_q`) AS A_ACR_10,SUM(`MB2TCP3.A_ACR_20.Ep_total_q`) AS A_ACR_13"
                sql = "SELECT  " + tag_str + ",CollectionDate AS CollectionDate,CollectionHour AS CollectionHour FROM incrementelectrictable WHERE CollectionDate BETWEEN '"\
                      + begin + "' AND '" + end + "' OR CollectionDate BETWEEN '" + beginnow + "' AND '" + endnow + "' group by CollectionHour order by CollectionHour"
                re = db_session.execute(sql).fetchall()
                dict_i = {}
                curr_A_ACR_10_count = 0
                curr_A_ACR_13_count = 0
                comp_A_ACR_10_count = 0
                comp_A_ACR_13_count = 0
                for i in re:
                    dict_i[i["CollectionHour"]] = \
                        round(float(0 if i["A_ACR_10"] == None else i["A_ACR_10"]) + float(
                            0 if i["A_ACR_13"] == None else i["A_ACR_13"]), 2)

                    #柱状图数据获取
                    if datetime.datetime.strptime(begin, "%Y-%m-%d %H:%M:%S") <= i["CollectionDate"] <= datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S"):
                        comp_A_ACR_10_count = comp_A_ACR_10_count + float(0 if i["A_ACR_10"] == None else i["A_ACR_10"])
                        comp_A_ACR_13_count = comp_A_ACR_13_count + float(0 if i["A_ACR_13"] == None else i["A_ACR_13"])
                    if datetime.datetime.strptime(beginnow, "%Y-%m-%d %H:%M:%S") <= i["CollectionDate"] <= datetime.datetime.strptime(endnow, "%Y-%m-%d %H:%M:%S"):
                        curr_A_ACR_10_count = curr_A_ACR_10_count + float(0 if i["A_ACR_10"] == None else i["A_ACR_10"])
                        curr_A_ACR_13_count = curr_A_ACR_13_count + float(0 if i["A_ACR_13"] == None else i["A_ACR_13"])
                dir_list = []
                for h in myHours:
                    dict_h = {}
                    currhour = datetime.datetime.now().strftime("%Y-%m-%d") + " " + h
                    dict_h["时间"] = currhour
                    comphour = CompareTime + " " + h
                    if currhour in dict_i.keys():
                        dict_h["今日能耗"] = dict_i[currhour]
                    else:
                        if datetime.datetime.strptime(currhour, '%Y-%m-%d %H') > datetime.datetime.now():
                            dict_h["今日能耗"] = ""
                        else:
                            dict_h["今日能耗"] = 0
                    if comphour in dict_i.keys():
                        dict_h["对比日能耗"] = dict_i[comphour]
                    else:
                        dict_h["对比日能耗"] = 0
                    dir_list.append(dict_h)
                dir = {}
                dir["lineChartRows"] = dir_list
                row1_list = []
                row1_list.append({"电表": "LS1机组电表", "今日": round(curr_A_ACR_10_count, 2), "对比日": round(comp_A_ACR_10_count, 2)})
                row1_list.append({"电表": "LS2机组电表", "今日": round(curr_A_ACR_13_count, 2), "对比日": round(comp_A_ACR_13_count, 2)})
                row1_list.append(
                    {"电表": "总和", "今日": round(curr_A_ACR_13_count+curr_A_ACR_10_count, 2), "对比日": round(comp_A_ACR_13_count+comp_A_ACR_10_count, 2)})
                dir["histogramChartRows"] = row1_list
                return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
            else:
                return json.dumps("请选择对比日", cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            logger.error(e)
            insertSyslog("error", "能耗分析报错Error：" + str(e), current_user.Name)
            return json.dumps("能耗分析报错", cls=AlchemyEncoder, ensure_ascii=False)

@energy.route('/energyselectbytime', methods=['GET', 'POST'])
def energyselectbytime():
    '''
    根据时间段查询能耗值
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            begin = data.get("begin")
            end = data.get("end")
            tag_str = "SUM(`MB2TCP3.A_ACR_12.Ep_total_q`) AS A_ACR_10,SUM(`MB2TCP3.A_ACR_20.Ep_total_q`) AS A_ACR_13"
            sql = "SELECT  " + tag_str + ",CollectionDate AS CollectionDate,CollectionHour AS CollectionHour FROM incrementelectrictable WHERE CollectionDate BETWEEN '" \
                  + begin + "' AND '" + end + "'"
            re = db_session.execute(sql).fetchall()
            count = 0
            for i in re:
                count = round(float(0 if i["A_ACR_10"] == None else i["A_ACR_10"]) + float(
                    0 if i["A_ACR_13"] == None else i["A_ACR_13"]), 2)
            return json.dumps(count, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            logger.error(e)
            insertSyslog("error", "根据时间段查询能耗值报错Error：" + str(e), current_user.Name)
            return json.dumps("根据时间段查询能耗值报错", cls=AlchemyEncoder, ensure_ascii=False)


@energy.route('/makecoolanalysis', methods=['GET', 'POST'])
def makecoolanalysis():
    '''
    制冷分析
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            CompareTime = data.get("CompareTime")
            if CompareTime:
                begin = CompareTime + " 00:00:00"
                end = CompareTime + " 23:59:59"
                beginnow = datetime.datetime.now().strftime("%Y-%m-%d") + " 00:00:00"
                endnow = datetime.datetime.now().strftime("%Y-%m-%d") + " 23:59:59"
                tag_str = "SUM(TotalHotLoad) AS TotalHotLoad,SUM(ZLLLoad) AS ZLLLoad"
                sql = "SELECT  " + tag_str + ",SampleTime AS CollectionDate,CollectionHour AS CollectionHour FROM datahistory WHERE SampleTime BETWEEN '"\
                      + begin + "' AND '" + end + "' OR SampleTime BETWEEN '" + beginnow + "' AND '" + endnow + "' group by CollectionHour order by CollectionHour"
                re = db_session.execute(sql).fetchall()
                dict_i = {}
                curr_TotalHotLoad_count = 0
                curr_ZLLLoad_count = 0
                comp_TotalHotLoad_count = 0
                comp_ZLLLoad_count = 0
                for i in re:
                    #柱状图数据获取
                    if datetime.datetime.strptime(begin, "%Y-%m-%d %H:%M:%S") <= i["CollectionDate"] <= datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S"):
                        dict_i[i["CollectionHour"]] = round(
                            float(0 if i["TotalHotLoad"] == None else i["TotalHotLoad"]), 2)
                        dict_i[i["CollectionHour"] + "cool"] = round(float(0 if i["ZLLLoad"] == None else i["ZLLLoad"]),
                                                                     2)
                        comp_TotalHotLoad_count = comp_TotalHotLoad_count + float(0 if i["TotalHotLoad"] == None else i["TotalHotLoad"])
                        comp_ZLLLoad_count = comp_ZLLLoad_count + float(0 if i["ZLLLoad"] == None else i["ZLLLoad"])
                    if datetime.datetime.strptime(beginnow, "%Y-%m-%d %H:%M:%S") <= i["CollectionDate"] <= datetime.datetime.strptime(endnow, "%Y-%m-%d %H:%M:%S"):
                        curr_TotalHotLoad_count = curr_TotalHotLoad_count + float(0 if i["TotalHotLoad"] == None else i["TotalHotLoad"])
                        curr_ZLLLoad_count = curr_ZLLLoad_count + float(0 if i["ZLLLoad"] == None else i["ZLLLoad"])
                dir_list = []
                for h in myHours:
                    dict_h = {}
                    comphour = CompareTime + " " + h
                    dict_h["时间"] = comphour
                    if comphour in dict_i.keys():
                        dict_h["制冷量"] = dict_i[comphour+"cool"]
                        dict_h["热负载"] = dict_i[comphour]
                    else:
                        if datetime.datetime.strptime(comphour, '%Y-%m-%d %H') > datetime.datetime.now():
                            dict_h["制冷量"] = ""
                            dict_h["热负载"] = ""
                        else:
                            dict_h["制冷量"] = 0
                            dict_h["热负载"] = 0
                    dir_list.append(dict_h)
                dir = {}
                dir["lineChartRows"] = dir_list
                row1_list = []
                row1_list.append({"统计": "制冷量", "今日": round(curr_ZLLLoad_count, 2), "对比日": round(comp_ZLLLoad_count, 2)})
                row1_list.append({"统计": "热负载", "今日": round(curr_TotalHotLoad_count, 2), "对比日": round(comp_TotalHotLoad_count, 2)})
                dir["histogramChartRows"] = row1_list
                return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
            else:
                return json.dumps("请选择对比日", cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            logger.error(e)
            insertSyslog("error", "制冷分析报错Error：" + str(e), current_user.Name)
            return json.dumps("制冷分析报错", cls=AlchemyEncoder, ensure_ascii=False)

@energy.route('/makecoolselectbytime', methods=['GET', 'POST'])
def makecoolselectbytime():
    '''
    根据时间段查询制冷分析值
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            TagCode = data.get("TagCode")
            begin = data.get("begin")
            end = data.get("end")
            tag_str = "SUM("+TagCode+") AS "+TagCode
            sql = "SELECT  " + tag_str + " FROM datahistory WHERE SampleTime BETWEEN '" + begin + "' AND '" + end + "'"
            re = db_session.execute(sql).fetchall()
            count = 0
            for i in re:
                count = round(float(0 if i[TagCode] == None else i[TagCode]), 2)
            return json.dumps(count, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            logger.error(e)
            insertSyslog("error", "根据时间段查询制冷分析值报错Error：" + str(e), current_user.Name)
            return json.dumps("根据时间段查询制冷分析值报错", cls=AlchemyEncoder, ensure_ascii=False)

def getEquipmentEfficiencyTreeChildrenMap(id):
    sz = []
    try:
        orgs = db_session.query(EquipmentEfficiencyTree).filter(EquipmentEfficiencyTree.ParentEquipmentCode == id).all()
        for obj in orgs:
            if int(obj.ParentEquipmentCode) == id:
                sz.append(
                    {"label": obj.EquipmentName, "value": obj.EquipmentCode, "children": getEquipmentEfficiencyTreeChildrenMap(obj.ID)})
        return sz
    except Exception as e:
        print(e)
        return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)
@energy.route('/selectEquipmentEfficiencyTree')#组织结构
def selectEquipmentEfficiencyTree():
    '''查询设备效率分析树形结构'''
    if request.method == 'GET':
        try:
            return json.dumps(getEquipmentEfficiencyTreeChildrenMap(id=0), cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            insertSyslog("error", "查询设备效率分析树形结构报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

@energy.route('/selectrundetailbyequipmentcode', methods=['GET', 'POST'])
def selectrundetailbyequipmentcode():
    '''
    根据设备code查询设备运行情况
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            EquipmentCode = data.get("EquipmentCode")
            WorkDate = data.get("WorkDate")
            run = db_session.query(EquipmentStatusCount).filter(EquipmentStatusCount.WorkDate == WorkDate,
                                                                     EquipmentStatusCount.SYSEQPCode == EquipmentCode,
                                                                     EquipmentStatusCount.Status == "RUN").all()
            stop = db_session.query(EquipmentStatusCount).filter(EquipmentStatusCount.WorkDate == WorkDate,
                                                                     EquipmentStatusCount.SYSEQPCode == EquipmentCode,
                                                                     EquipmentStatusCount.Status == "STOP").all()
            fault = db_session.query(EquipmentStatusCount).filter(EquipmentStatusCount.WorkDate == WorkDate,
                                                                     EquipmentStatusCount.SYSEQPCode == EquipmentCode,
                                                                     EquipmentStatusCount.Status == "FAULT").all()
            equip = db_session.query(Equipment).filter(Equipment.EquipmentCode == EquipmentCode).first()
            if equip:
                pow = equip.Power
            else:
                pow = ""
            dict_run = {}
            dict_run["runcount"] = len(run)
            dict_run["stopcount"] = len(stop)
            dict_run["faultcount"] = len(fault)
            dict_run["power"] = pow
            runtime = 0
            for r in run:
               runtime = runtime + float(r.Duration)
            dict_run["runtime"] = round(runtime, 2)
            stoptime = 0
            for r in stop:
                stoptime = stoptime + float(r.Duration)
            dict_run["stoptime"] = round(stoptime, 2)
            faulttime = 0
            for r in fault:
                faulttime = faulttime + float(r.Duration)
            dict_run["faulttime"] = round(faulttime, 2)
            total_time = runtime + stoptime + faulttime
            if total_time != 0:
                dict_run["run_Proportion"] = str(round(100*(runtime/total_time),2))+"%"
                dict_run["stop_Proportion"] = str(round(100 * (stoptime / total_time), 2))+"%"
                dict_run["fault_Proportion"] = str(round(100 * (faulttime / total_time), 2))+"%"
            else:
                dict_run["run_Proportion"] = +"0%"
                dict_run["stop_Proportion"] = "0%"
                dict_run["fault_Proportion"] = "0%"
            return json.dumps(dict_run, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            logger.error(e)
            insertSyslog("error", "根据设备code查询设备运行情况报错Error：" + str(e), current_user.Name)
            return json.dumps("根据设备code查询设备运行情况报错", cls=AlchemyEncoder, ensure_ascii=False)
