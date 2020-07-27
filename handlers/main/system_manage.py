import redis
from flask import Blueprint, render_template, request, make_response
from flask_login import current_user
from sqlalchemy.ext.automap import automap_base
from dbset.main.BSFramwork import AlchemyEncoder
from models.system import DataSummaryAnalysis
from tools import autocode
from tools.MESLogger import MESLogger
from dbset.log.BK2TLogger import logger,insertSyslog
import json
from tools.common import engine
from dbset.database.db_operate import DB_URL,db_session
import arrow

logger = MESLogger('../logs', 'log')
from sqlalchemy import MetaData
from io import BytesIO

metadata = MetaData()
from dbset.database import constant
Base = automap_base()
Base.prepare(engine, reflect=True)

system_set = Blueprint('system_set', __name__, template_folder='templates')


# 加载工作台
@system_set.route('/home/workbench')
def workbenck():
    return render_template('./main/workbench.html')

# 加载工作台
@system_set.route('/system_set/make_model', methods=['POST', 'GET'])
def make_model():
    if request.method == 'POST':
        data = request.values
        try:
            jsonstr = json.dumps(data.to_dict())
            return autocode.make_model_main(data)
        except Exception as e:
            print(e)
            logger.error(e)

def returnb(rod):
    if rod == None or rod == "" or rod == b'':
        return ""
    else:
        return rod.decode()
@system_set.route('/systemcollecting', methods=['POST', 'GET'])
def systemcollecting():
    '''
    系统体检
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            dir = {}
            pool = redis.ConnectionPool(host=constant.REDIS_HOST)
            redis_conn = redis.Redis(connection_pool=pool, password=constant.REDIS_PASSWORD, decode_responses=True)
            dir["name"] = "采集服务"
            dir["startTime"] = returnb(redis_conn.hget(constant.REDIS_TABLENAME, "collecting_server_start"))
            dir["endTime"] = returnb(redis_conn.hget(constant.REDIS_TABLENAME, "collecting_server_end"))
            dir["successNumber"] = returnb(redis_conn.hget(constant.REDIS_TABLENAME, "collecting_server_runcount"))
            dir["errorNumber"] = returnb(redis_conn.hget(constant.REDIS_TABLENAME, "collecting_server_failcount"))
            dir["totalNumber"] = int(returnb(redis_conn.hget(constant.REDIS_TABLENAME, "collecting_server_runcount")))+int(returnb(redis_conn.hget(constant.REDIS_TABLENAME, "collecting_server_failcount")))
            dir["state"] = returnb(redis_conn.hget(constant.REDIS_TABLENAME, "collecting_server_status"))
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "系统体检报错Error：" + str(e), current_user.Name)

@system_set.route('/systemredisdb', methods=['POST', 'GET'])
def systemredisdb():
    '''
    系统体检
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            dir = {}
            pool = redis.ConnectionPool(host=constant.REDIS_HOST)
            redis_conn = redis.Redis(connection_pool=pool, password=constant.REDIS_PASSWORD, decode_responses=True)
            dir["name"] = "写入历史数据库服务"
            dir["startTime"] = returnb(redis_conn.hget(constant.REDIS_TABLENAME, "redis_insertdb_server_start"))
            dir["endTime"] = returnb(redis_conn.hget(constant.REDIS_TABLENAME, "redis_insertdb_server_end"))
            dir["successNumber"] = returnb(redis_conn.hget(constant.REDIS_TABLENAME, "redis_insertdb_server_runcount"))
            dir["errorNumber"] = returnb(redis_conn.hget(constant.REDIS_TABLENAME, "redis_insertdb_server_failcount"))
            dir["totalNumber"] = int(returnb(redis_conn.hget(constant.REDIS_TABLENAME, "redis_insertdb_server_runcount")))+int(returnb(redis_conn.hget(constant.REDIS_TABLENAME, "redis_insertdb_server_failcount")))
            dir["state"] = returnb(redis_conn.hget(constant.REDIS_TABLENAME, "redis_insertdb_server_status"))
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "系统体检报错Error：" + str(e), current_user.Name)

@system_set.route('/systemdbincrment', methods=['POST', 'GET'])
def systemdbincrment():
    '''
    系统体检
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            dir = {}
            pool = redis.ConnectionPool(host=constant.REDIS_HOST)
            redis_conn = redis.Redis(connection_pool=pool, password=constant.REDIS_PASSWORD, decode_responses=True)
            dir["name"] = "写入增量服务"
            dir["startTime"] = returnb(redis_conn.hget(constant.REDIS_TABLENAME, "redis_incremeninsertdb_server_start"))
            dir["endTime"] = returnb(redis_conn.hget(constant.REDIS_TABLENAME, "redis_incremeninsertdb_server_end"))
            dir["successNumber"] = returnb(redis_conn.hget(constant.REDIS_TABLENAME, "redis_incremeninsertdb_server_runcount"))
            dir["errorNumber"] = returnb(redis_conn.hget(constant.REDIS_TABLENAME, "redis_incremeninsertdb_server_failcount"))
            dir["totalNumber"] = int(returnb(redis_conn.hget(constant.REDIS_TABLENAME, "redis_incremeninsertdb_server_runcount")))+int(returnb(redis_conn.hget(constant.REDIS_TABLENAME, "redis_incremeninsertdb_server_failcount")))
            dir["state"] = returnb(redis_conn.hget(constant.REDIS_TABLENAME, "redis_incremeninsertdb_server_status"))
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "系统体检报错Error：" + str(e), current_user.Name)

@system_set.route('/systemwebsocket', methods=['POST', 'GET'])
def systemwebsocket():
    '''
    系统体检
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            dir = {}
            pool = redis.ConnectionPool(host=constant.REDIS_HOST)
            redis_conn = redis.Redis(connection_pool=pool, password=constant.REDIS_PASSWORD, decode_responses=True)
            dir["name"] = "实时数据服务（websocket）"
            dir["startTime"] = returnb(redis_conn.hget(constant.REDIS_TABLENAME, "websocket_start"))
            dir["endTime"] = returnb(redis_conn.hget(constant.REDIS_TABLENAME, "websocket_end"))
            dir["successNumber"] = returnb(redis_conn.hget(constant.REDIS_TABLENAME, "websocket_runcount"))
            dir["errorNumber"] = returnb(redis_conn.hget(constant.REDIS_TABLENAME, "websocket_failcount"))
            dir["totalNumber"] = int(returnb(redis_conn.hget(constant.REDIS_TABLENAME, "websocket_runcount")))+int(returnb(redis_conn.hget(constant.REDIS_TABLENAME, "websocket_failcount")))
            dir["state"] = returnb(redis_conn.hget(constant.REDIS_TABLENAME, "websocket_status"))
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "系统体检报错Error：" + str(e), current_user.Name)

@system_set.route('/exceloutdatasummaryanalysis', methods=['POST', 'GET'])
def exceloutdatasummaryanalysis():
    '''
    导出统计数据
    :return:
    '''
    data = request.values
    if request.method == 'GET':
        StartTime = data.get("StartTime")
        EndTime = data.get("EndTime")
        output = exportxdatasummaryanalysis(StartTime, EndTime)
        resp = make_response(output.getvalue())
        resp.headers["Content-Disposition"] = "attachment; filename=consumption.xlsx"
        resp.headers['Content-Type'] = 'application/x-xlsx'
        return resp

import pandas as pd
def exportxdatasummaryanalysis(StartTime, EndTime):
    # 创建数据流
    output = BytesIO()
    # 创建excel work book
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    workbook = writer.book
    # 创建excel sheet
    worksheet = workbook.add_worksheet('sheet1')

    cell_format = workbook.add_format({
        'font_size': 18,
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#006633'})
    worksheet.set_column('A:F', 24)
    col = 0
    row = 1
    # 写入列名
    columns = ['日期', '站厅温度', '站台温度', '站厅湿度', '站台湿度', '二氧化碳含量', 'L1冷水机组耗量', 'L2冷水机组耗量', '冷水机组总耗量']
    for item in columns:
        worksheet.write(0, col, item, cell_format)
        col += 1
    oclass = db_session.query(DataSummaryAnalysis).filter(DataSummaryAnalysis.CollectionDate.between(StartTime, EndTime)).all()
    i = 0
    for oc in oclass:
        print(oc.CollectionDate)
        for cum in columns:
            if cum == '日期':
                worksheet.write(i + 1, columns.index(cum), oc.CollectionDate)
            if cum == '站厅温度':
                worksheet.write(i + 1, columns.index(cum), oc.StationHallTemperature)
            if cum == '站台温度':
                worksheet.write(i + 1, columns.index(cum), oc.PlatformTemperature)
            if cum == '站厅湿度':
                worksheet.write(i + 1, columns.index(cum), oc.StationHallHumidity)
            if cum == '站台湿度':
                worksheet.write(i + 1, columns.index(cum), oc.PlatformHumidity)
            if cum == '二氧化碳含量':
                worksheet.write(i + 1, columns.index(cum), oc.CarbonDioxideContent)
            if cum == 'L1冷水机组耗量':
                worksheet.write(i + 1, columns.index(cum), oc.ConsumptionLfirst)
            if cum == 'L2冷水机组耗量':
                worksheet.write(i + 1, columns.index(cum), oc.ConsumptionLsecond)
            if cum == '冷水机组总耗量':
                worksheet.write(i + 1, columns.index(cum), oc.ConsumptionLtotal)
        i = i + 1
    writer.close()
    output.seek(0)
    return output



@system_set.route('/insertdb_datasummaryanalysis', methods=['POST', 'GET'])
def insertdb_datasummaryanalysis():
    '''
    数据汇总分析数据写入
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            CollectDay = data.get("CollectDay")
            dasoc = db_session.query(DataSummaryAnalysis).filter(DataSummaryAnalysis.CollectionDate == CollectDay).first()
            if not dasoc:
                daysta = CollectDay + " 00:00:00"
                dayend = CollectDay + " 23:59:59"
                dsa = DataSummaryAnalysis()
                sql = "SELECT  SUM(`MB2TCP3.A_ACR_12.Ep_total_q`) AS ConsumptionLfirst,SUM(`MB2TCP3.A_ACR_20.Ep_total_q`) AS ConsumptionLsecond FROM incrementelectrictable WHERE CollectionDate BETWEEN '" \
                      + daysta + "' AND '" + dayend + "'"
                re = db_session.execute(sql).fetchall()
                ConsumptionLfirst = 0
                ConsumptionLsecond = 0
                for oc in re:
                    ConsumptionLfirst = 0 if oc["ConsumptionLfirst"] == None or oc["ConsumptionLfirst"] == "" else int(oc["ConsumptionLfirst"])
                    ConsumptionLsecond = 0 if oc["ConsumptionLsecond"] == None or oc["ConsumptionLsecond"] == "" else int(oc["ConsumptionLsecond"])
                sql = "SELECT  AVG(TY_CO2_AVG) AS CarbonDioxideContent,AVG(ZT01_TEMP_AVG) AS PlatformTemperature,AVG(ZT01_SD_AVG) AS PlatformHumidity,AVG(ZT02_TEMP_AVG) AS StationHallTemperature,AVG(ZT02_SD_AVG) AS StationHallHumidity" \
                      " FROM datahistory WHERE SampleTime BETWEEN '" + daysta + "' AND '" + dayend + "'"
                re1 = db_session.execute(sql).fetchall()
                CarbonDioxideContent = ""
                PlatformHumidity = ""
                PlatformTemperature = ""
                StationHallTemperature = ""
                StationHallHumidity = ""
                for i in re1:
                    CarbonDioxideContent = i["CarbonDioxideContent"]
                    PlatformHumidity = i["PlatformHumidity"]
                    PlatformTemperature = i["PlatformTemperature"]
                    StationHallTemperature = i["StationHallTemperature"]
                    StationHallHumidity = i["StationHallHumidity"]
                dsa.CollectionDate = CollectDay
                dsa.CarbonDioxideContent = CarbonDioxideContent
                dsa.ConsumptionLfirst = ConsumptionLfirst
                dsa.ConsumptionLsecond = ConsumptionLsecond
                dsa.ConsumptionLtotal = ConsumptionLsecond + ConsumptionLfirst
                dsa.PlatformHumidity = PlatformHumidity
                dsa.PlatformTemperature = PlatformTemperature
                dsa.StationHallTemperature = StationHallTemperature
                dsa.StationHallHumidity = StationHallHumidity
                db_session.add(dsa)
                db_session.commit()
                return json.dumps("OK", cls=AlchemyEncoder, ensure_ascii=False)
            else:
                return json.dumps("已经导入过此天的数据", cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "数据汇总分析数据写入报错Error：" + str(e), current_user.Name)



