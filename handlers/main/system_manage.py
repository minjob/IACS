import redis
from flask import Blueprint, render_template, request
from flask_login import current_user
from sqlalchemy.ext.automap import automap_base
from dbset.main.BSFramwork import AlchemyEncoder
from tools import autocode
from tools.MESLogger import MESLogger
from dbset.log.BK2TLogger import logger,insertSyslog
import json
from tools.common import engine
logger = MESLogger('../logs', 'log')
from sqlalchemy import MetaData

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





