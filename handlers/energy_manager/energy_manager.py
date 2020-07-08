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

@energy.route('/energyanalysis', methods=['GET', 'POST'])
def energyanalysis():
    '''
    能耗分析
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            CollectionDate = data.get("CollectionDate")
            if CollectionDate:
                begin = CollectionDate + " 00:00:00"
                end = CollectionDate + " 23:59:59"
                beginnow = datetime.datetime.now().strftime("%Y-%m-%d") + " 00:00:00"
                endnow = datetime.datetime.now().strftime("%Y-%m-%d") + " 23:59:59"
                tag_str = "`MB2TCP3.A_ACR_10.Ep_total` AS A_ACR_10,`MB2TCP3.A_ACR_13.Ep_total` AS A_ACR_13"
                sql = "SELECT  " + tag_str + ",CollectionDate AS CollectionDate,CollectionHour AS CollectionHour FROM incrementelectrictable WHERE CollectionDate BETWEEN '"\
                      + begin + "' AND '" + end + "' OR CollectionDate BETWEEN '" + beginnow + "' AND '" + endnow + "' group by CollectionHour order by CollectionHour"
                re = db_session.execute(sql).fetchall()
                dict_list = []
                for i in range(len(re)):
                    dict_i = {}
                    begin = datetime.datetime.strptime(begin,'%Y-%m-%d %H:%M:%S')
                    if datetime.datetime.strptime(beginnow,'%Y-%m-%d %H:%M:%S')<=re[i]["SampleTime"]<datetime.datetime.strptime(endnow,'%Y-%m-%d %H:%M:%S'):#当前天数据
                        dict_i["时间"] = datetime.datetime.strftime(re[i]["CollectionHour"], '%Y-%m-%d %H')
                        dict_i[""]
                    dict_list.append(dict_i)
            return json.dumps(dict_list, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            logger.error(e)
            insertSyslog("error", "能耗分析报错Error：" + str(e), current_user.Name)
            return json.dumps("能耗分析报错", cls=AlchemyEncoder, ensure_ascii=False)