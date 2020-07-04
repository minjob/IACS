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

from dbset.database.db_operate import SchedulingStatus, DB_URL
from dbset.main.BSFramwork import AlchemyEncoder
from models.schedul_model import Scheduling, plantCalendarScheduling, product_plan, ERPproductcode_prname, \
    SchedulingStandard, SchedulingStock, scheduledate, TagMaintain, scheduleDateType
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

erp_schedul = Blueprint('erp_schedul', __name__)


@erp_schedul.route('/systemManager_model/plantCalendarSchedulingSelect', methods=['GET', 'POST'])
def plantCalendarSchedulingSelect():
    '''
    工厂日历
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            re = []
            oclass = db_session.query(Scheduling).all()
            for oc in oclass:
                dir = {}
                dir['ID'] = oc.ID
                dir['start'] = oc.SchedulingTime
                dir['title'] = oc.PRName + ": 第" + oc.SchedulingNum[6:] + "批"
                dir['color'] = "#9FDABF"
                re.append(dir)
            ocl = db_session.query(plantCalendarScheduling).all()
            for o in ocl:
                dic = {}
                dic['ID'] = str(o.ID)
                dic['start'] = str(o.start)
                dic['title'] = o.title.split(":")[0]
                dic['color'] = o.color
                re.append(dic)
            return json.dumps(re, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            logger.error(e)
            insertSyslog("error", "工厂日历查询报错Error：" + str(e), current_user.Name)
            return json.dumps("工厂日历查询报错", cls=AlchemyEncoder, ensure_ascii=False)

@erp_schedul.route('/systemManager_model/planScheduling', methods=['GET', 'POST'])
def planScheduling():
    '''
    计划排产
    :return:
    '''
    if request.method == 'POST':
        data = request.values
        try:
            plan_id = data['plan_id']
            oc = db_session.query(product_plan).filter(product_plan.plan_id == plan_id).first()
            month = data['month']
            mou = month.split("-")
            monthRange = calendar.monthrange(int(mou[0]), int(mou[1]))
            PRName = db_session.query(ERPproductcode_prname.PRName).filter(ERPproductcode_prname.product_code == oc.product_code).first()[0]
            sch = db_session.query(SchedulingStandard).filter(SchedulingStandard.PRName == PRName).first()
            batchnums = int(oc.plan_quantity)
            days = batchnums/int(sch.DayBatchNumS) #这批计划要做多少天
            re = timeChange(mou[0], mou[1], monthRange[1])

            #不能排产的时间
            if int(mou[1])<10:
                mou = mou[0]+"-0"+mou[1]
            else:
                mou = mou[0] + "-" + mou[1]
            schdays = db_session.query(plantCalendarScheduling.start).filter(plantCalendarScheduling.start.like("%" + mou + "%"),
                                    ~plantCalendarScheduling.title.like("%安全库存%")).all()#----查询休息的天数排产去除员工不上班的时间
            undays = []
            if schdays != None:
                for i in schdays:
                    undays.append(i[0])

            # 删除上一次排产同品名同月份的数据
            solds = db_session.query(Scheduling).filter(Scheduling.PRName == PRName, Scheduling.SchedulingTime.like("%"+mou+"%")).all()
            for old in solds:
                sql = "DELETE FROM Scheduling WHERE ID = "+str(old.ID)
                db_session.execute(sql)#删除同意品名下的旧的排产计划
            plans = db_session.query(plantCalendarScheduling).filter(plantCalendarScheduling.title.like(PRName), plantCalendarScheduling.start.like("%"+mou+"%")).all()
            for pl in plans:
                sql = sql1 = "DELETE FROM plantCalendarScheduling WHERE ID = " + str(pl.ID)
                db_session.execute(sql)#删除同意品名下的安全库存信息
            db_session.commit()

            # 去掉不能排产的时间，只剩可以排产的时间
            daySchedulings = list(set(re).difference(set(undays)))
            daySchedulings = list(daySchedulings)
            daySchedulings.sort()

            # 排产数据写入数据库
            dayBatchNum = db_session.query(SchedulingStandard.DayBatchNumS).filter(SchedulingStandard.PRName == PRName).first()[0]
            j = 1
            k = 1
            for day in daySchedulings:
                if k > days:#当这个计划所有的批次做完跳出循环
                    break
                for r in range(0, int(dayBatchNum)):
                    s = Scheduling()
                    s.SchedulingTime = day
                    s.PRName = PRName
                    s.BatchNumS = sch.DayBatchNumS
                    if j < 10:
                        s.SchedulingNum = day.replace("-", "")[2:6] + "600" + str(j)
                    else:
                        s.SchedulingNum = day.replace("-", "")[2:6] + "60" + str(j)
                    db_session.add(s)
                    j = j+1
                k = k + 1
            db_session.commit()
            return 'OK'
        except Exception as e:
            print(e)
            db_session.rollback()
            logger.error(e)
            insertSyslog("error", "计划排产报错Error：" + str(e), current_user.Name)
            return json.dumps("计划排产报错", cls=AlchemyEncoder, ensure_ascii=False)
def timeChange(year,month,days):
    i = 0
    da = []
    while i < days:
        if i < 9:
            i = i + 1
            date = str(year) + "-" + str(mon(month)) + "-" + str(0) + str(i)
            da.append(date)
        else:
            i = i + 1
            date = str(year)  + "-" + str(mon(month))  + "-" +  str(i)
            da.append(date)
    return da
def mon(month):
    if int(month)<10:
        return "0"+month
    else:
        return month
@erp_schedul.route('/systemManager_model/plantSchedulingAddBatch', methods=['GET', 'POST'])
def plantSchedulingAddBatch():
    '''
    计划排产增加批次
    :return:
    '''
    if request.method == 'POST':
        data = request.values
        try:
            PRName = data['title']
            code = db_session.query(ERPproductcode_prname.product_code).filter(ERPproductcode_prname.PRName ==
                                                                               PRName).first()[0]
            plan_id = db_session.query(product_plan.plan_id).filter(product_plan.product_code == code).order_by(
                desc("plan_id")).first()
            if plan_id != None:
                plan_id = plan_id[0]
            else:
                return "请先同步ERP计划！"
            date = data['start']
            #添加排产数据
            sch = db_session.query(Scheduling).filter(Scheduling.PRName == PRName).order_by(desc("SchedulingNum")).first()
            if sch == None:
                return "请先进行排产！"
            count = db_session.query(Scheduling).filter(Scheduling.SchedulingTime == sch.SchedulingTime).count()
            SchedulingTime = sch.SchedulingTime
            if int(sch.BatchNumS) == count or sch.BatchNumS == "1":
                spls = str(sch.SchedulingTime)[8:10]
                spls = str(int(spls) + 1)
                SchedulingTime = str(sch.SchedulingTime)[0:8] + spls
                ishas = db_session.query(plantCalendarScheduling).filter(plantCalendarScheduling.start == SchedulingTime).first()
                while ishas != None:
                    i = 1
                    spls = str(int(spls) + i)
                    SchedulingTime = str(sch.SchedulingTime)[0:8] + spls
                    ishas = db_session.query(plantCalendarScheduling).filter(plantCalendarScheduling.start == SchedulingTime).first()
                    i = i + 1
            sc = Scheduling()
            sc.PRName = sch.PRName
            sc.SchedulingStatus = SchedulingStatus.Unlock.value
            sc.SchedulingTime = SchedulingTime
            sc.BatchNumS = sch.BatchNumS
            sc.SchedulingNum = str(int(sch.SchedulingNum) + 1)
            sc.create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db_session.add(sc)
            db_session.commit()
            return 'OK'
        except Exception as e:
            logger.error(e)
            insertSyslog("error", "计划排产增加批次报错Error：" + str(e), current_user.Name)
            return json.dumps("计划排产增加批次报错", cls=AlchemyEncoder, ensure_ascii=False)

@erp_schedul.route('/addscheduledates', methods=['GET', 'POST'])
def addscheduledates():
    '''
    添加工作日休息日
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            month = data['month']
            count = db_session.query(scheduledate).filter(scheduledate.WorkDate.like("%"+month+"%")).count()
            if count < 20:
                mou = month.split("-")
                monthRange = calendar.monthrange(int(mou[0]), int(mou[1]))
                re = timeChange(mou[0], str(int(mou[1])), monthRange[1])
                lis = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日', ]
                dic = dict(enumerate(lis))
                for i in re:
                    ymr = i.split("-")
                    w = datetime.date(int(ymr[0]), int(ymr[1]), int(ymr[2]))
                    xq = dic[w.weekday()]
                    if xq == "星期六" or xq == "星期日":
                        # dc = db_session.query(scheduleDateType).filter(scheduleDateType.DateTypeName == "周末").first()
                        DateType = "周末"
                        color = "#FA7D00"
                    else:
                        DateType = "工作日"
                        color = "#00CAFA"
                    sc = scheduledate()
                    sc.WorkDate = i
                    sc.DateType = DateType
                    sc.comment = xq
                    sc.color = color
                    db_session.add(sc)
                    db_session.commit()
                db_session.close_all()
            return 'OK'
        except Exception as e:
            db_session.rollback()
            logger.error(e)
            insertSyslog("error", "添加工作日休息日报错Error：" + str(e), current_user.Name)
            return json.dumps("添加工作日休息日报错", cls=AlchemyEncoder, ensure_ascii=False)

@erp_schedul.route('/energytrendtu', methods=['GET', 'POST'])
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
                      + begin + "' AND '" + end + "' order by ID"
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
                begin = data.get("begin")
                end = data.get("end")
                begin1 = data.get("begin1")
                end1 = data.get("end1")
                begin2 = data.get("begin2")
                end2 = data.get("end2")
                begin3 = data.get("begin3")
                end3 = data.get("end3")
                begin4 = data.get("begin4")
                end4 = data.get("end4")
                sql = "SELECT  " + TagCode + " AS value,SampleTime AS SampleTime FROM datahistory WHERE SampleTime " \
                     "BETWEEN '" + begin + "' AND '" + end + "' OR SampleTime BETWEEN '" + begin1 + "' AND '" + end1 + \
                      "' OR SampleTime BETWEEN '" + begin2 + "' AND '" + end2 + "' OR SampleTime BETWEEN '" + begin3 + \
                      "' AND '" + end3 + "' OR SampleTime BETWEEN '" + begin4 + "' AND '" + end4 + "' order by ID"
                re = db_session.execute(sql).fetchall()
                dict_list = []
                for i in re:
                    oc_list = []
                    oc_list.append(datetime.datetime.strftime(re[i]["SampleTime"], '%Y-%m-%d %H:%M:%S')[11:])
                    if re[i]["SampleTime"] is not None:
                        oc_list.append("-" if re["value"] is None else re[i]["value"])
                        dict_list.append(oc_list)
            return json.dumps(dict_list, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            logger.error(e)
            insertSyslog("error", "能耗趋势图报错Error：" + str(e), current_user.Name)
            return json.dumps("能耗趋势图报错", cls=AlchemyEncoder, ensure_ascii=False)