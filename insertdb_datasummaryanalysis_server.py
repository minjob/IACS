import datetime

import arrow as arrow
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dbset.database.db_operate import DB_URL,db_session
from models.system import DataSummaryAnalysis
from tools.common import logger,insertSyslog,insert,delete,update,select


# pool = redis.ConnectionPool(host=constant.REDIS_HOST)
def run():
    runcount = 0
    failcount = 0
    # redis_conn = redis.Redis(connection_pool=pool, password=constant.REDIS_PASSWORD, decode_responses=True)
    # redis_conn.hset(constant.REDIS_TABLENAME, "insertdb_datasummaryanalysis_server_start",
    #                 datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    while True:
        # time.sleep(2)
        print("数据汇总分析数据开始写入数据库")
        t = arrow.now()
        hourst = t.shift(hours=-1).format("YYYY-MM-DD HH")+":00:00"
        hourend = t.shift(hours=-1).format("YYYY-MM-DD HH") + ":59:59"
        try:
            dsa = DataSummaryAnalysis()
            tag_str = "SUM(`MB2TCP3.A_ACR_12.Ep_total_q`) AS A_ACR_10,SUM(`MB2TCP3.A_ACR_20.Ep_total_q`) AS A_ACR_13"
            sql = "SELECT  " + tag_str + ",CollectionDate AS CollectionDate FROM incrementelectrictable WHERE CollectionDate BETWEEN '" \
                  + hourst + "' AND '" + hourend + "'"
            re = db_session.execute(sql).fetchall()
            dsa.CollectionDate = t.shift(hours=-1).format("YYYY-MM-DD HH")
            dsa.CarbonDioxideContent =
            dsa.ConsumptionLfirst =
            dsa.ConsumptionLsecond =
            dsa.ConsumptionLtotal =
            dsa.PlatformHumidity =
            dsa.PlatformTemperature =
            dsa.StationHallTemperature =
            dsa.StationHallHumidity =
            runcount = runcount + 1
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "数据汇总分析数据写入报错Error：" + str(e), "")
            # redis_conn.hset(constant.REDIS_TABLENAME, "insertdb_datasummaryanalysis_server_status", "执行失败")
            failcount = failcount + 1
        finally:
            pass
        print("数据汇总分析数据开始写入数据库结束")
        # redis_conn.hset(constant.REDIS_TABLENAME, "insertdb_datasummaryanalysis_server_end",
        #                 datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # redis_conn.hset(constant.REDIS_TABLENAME, "insertdb_datasummaryanalysis_server_runcount", str(runcount))
        # redis_conn.hset(constant.REDIS_TABLENAME, "insertdb_datasummaryanalysis_server_failcount", str(failcount))
        # redis_conn.hset(constant.REDIS_TABLENAME, "insertdb_datasummaryanalysis_server_status", "执行成功")

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