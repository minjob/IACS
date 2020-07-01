import json
from sqlalchemy import create_engine, desc
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from flask_login import current_user
import re
from werkzeug.security import generate_password_hash
from models.system import AuditTrace
from dbset.main.BSFramwork import AlchemyEncoder
from models.system import SysLog
from tools.MESLogger import MESLogger
import socket
import datetime
from models.system import User

from dbset.database.db_operate import DB_URL
engine = create_engine(DB_URL,max_overflow=0,  # 超过连接池大小外最多创建的连接
            pool_size=5,  # 连接池大小
            pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
            pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
         )
conn = engine.connect()
Session = sessionmaker(bind=engine)
db_session = Session()

from sqlalchemy import MetaData

metadata = MetaData()
from sqlalchemy import Table
Base = automap_base()
Base.prepare(engine, reflect=True)

logger = MESLogger('../logs', 'log')
#插入日志OperationType OperationContent OperationDate UserName ComputerName IP
def insertSyslog(operationType, operationContent, userName):
        try:
            if operationType == None: operationType = ""
            if operationContent == None:
                operationContent = ""
            else:
                operationContent = str(operationContent)
            if userName == None: userName = ""
            ComputerName = socket.gethostname()
            db_session.add(
                SysLog(OperationType=operationType, OperationContent=operationContent,OperationDate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), UserName=userName,
                       ComputerName=ComputerName, IP=socket.gethostbyname(ComputerName)))
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            print(e)
            logger.error(e)

def insert(data):
    '''
    :param data: 需要添加的数据
    :return:
    '''
    if isinstance(data, dict) and len(data) > 0:
        try:
            tableName = str(data.get("tableName"))
            obj = Base.classes.get(tableName.lower())
            ss = obj()
            for key in data:
                if key != "ID" and key != "tableName" and key != "id" and key != "Creater":
                    if key == "Password":
                        setattr(ss, key, generate_password_hash(data['Password']))
                    elif key == "WorkNumber":
                        ocal = db_session.query(User).filter(User.WorkNumber == data['WorkNumber']).first()
                        if ocal != None:
                            return "工号重复，请重新录入！"
                        else:
                            setattr(ss, key, data['WorkNumber'])
                    else:
                        setattr(ss, key, data[key])
            db_session.add(ss)
            aud = AuditTrace()
            aud.TableName = tableName
            aud.Operation = current_user.Name + " 对表" + tableName + "添加一条数据！"
            aud.DeitalMSG = "用户：" + current_user.Name + " 对表" + tableName + "添加一条数据！"+json.dumps(data.to_dict())
            aud.ReviseDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            aud.User = current_user.Name
            db_session.add(aud)
            db_session.commit()
            return 'OK'
        except Exception as e:
            print(e)
            db_session.rollback()
            logger.error(e)
            insertSyslog("error", "%s数据添加报错："%tableName + str(e), current_user.Name)
            return json.dumps('数据添加失败！')

def delete(data):
    '''
    :param data: 要删除的数据
    :return:
    '''
    try:
        tableName = str(data.get("tableName"))
        jsonstr = json.dumps(data.to_dict())
        if len(jsonstr) > 10:
            jstr = data.get("delete_data")
            jsonnumber = re.findall(r"\d+\.?\d*", jstr)
            for key in jsonnumber:
                try:
                    sql = "delete from "+"[DB_MICS].[dbo].["+tableName+"] where ID = '"+key+"'"
                    db_session.execute(sql)
                    aud = AuditTrace()
                    aud.TableName = tableName
                    aud.Operation = current_user.Name + " 对表" + tableName + "中的ID为"+key+"的数据做了删除操作！"
                    aud.DeitalMSG = "用户：" + current_user.Name + " 对表" + tableName + "中的ID为"+key+"的数据做了删除操作！"
                    aud.ReviseDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    aud.User = current_user.Name
                    db_session.add(aud)
                    db_session.commit()
                except Exception as ee:
                    print(ee)
                    db_session.rollback()
                    insertSyslog("error", "删除户ID为"+str(id)+"报错Error：" + str(ee), current_user.Name)
                    return json.dumps("删除用户报错", cls=AlchemyEncoder,ensure_ascii=False)
            return 'OK'
    except Exception as e:
        db_session.rollback()
        logger.error(e)
        insertSyslog("error", "%s数据删除报错："%tableName + str(e), current_user.Name)
        return json.dumps('数据删除失败！')

def update(data):
    '''
    :param data: 更新数据
    :return:
    '''
    if isinstance(data, dict) and len(data) > 0:
        try:
            tableName = str(data.get("tableName"))
            obj = Base.classes.get(tableName.lower())
            ss = obj()
            ID = data.get('ID')
            oclass = db_session.query(obj).filter_by(ID=int(data.get('ID'))).first()
            if oclass:
                for key in data:
                    if hasattr(oclass, key) and key != 'ID' and key != 'tableName' and key != "id" and key != "Creater":
                        if key == "Password":
                            setattr(oclass, key, generate_password_hash(data['Password']))
                        elif key == "WorkNumber":
                            ocal = db_session.query(User).filter(User.WorkNumber == data['WorkNumber']).first()
                            if ocal != None:
                                if oclass.WorkNumber != data['WorkNumber']:
                                    return "工号重复，请重新录入！"
                            else:
                                setattr(oclass, key, data['WorkNumber'])
                        else:
                            setattr(oclass, key, data[key])
                db_session.add(oclass)
                aud = AuditTrace()
                aud.TableName = tableName
                aud.Operation =current_user.Name+" 对表"+tableName+"的数据做了更新操作！"
                aud.DeitalMSG = "用户："+current_user.Name+" 对表"+tableName+"ID为："+ID+"做了更新操作："+json.dumps(data.to_dict())
                aud.ReviseDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                aud.User = current_user.Name
                db_session.add(aud)
                db_session.commit()
                return 'OK'
            else:
                return json.dumps('当前记录不存在！', cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            db_session.rollback()
            logger.error(e)
            insertSyslog("error", "%s数据更新报错："%tableName + str(e), current_user.Name)
            return json.dumps('数据更新失败！', cls=AlchemyEncoder, ensure_ascii=False)

def select(data):#table, page, rows, fieid, param
    '''
    :param tablename: 查询表
    :param pages: 页数
    :param rowsnumber: 一页多少行
    :param fieid: 查询字段
    :param param: 查询条件
    :return:
    '''
    try:
        pages = int(data.get("offset"))
        rowsnumber = int(data.get("limit"))
        param = data.get("field")
        tableName = data.get("tableName")
        paramvalue = data.get("fieldvalue")
        inipage = pages * rowsnumber + 0  # 起始页
        endpage = pages * rowsnumber + rowsnumber  # 截止页
        newTable = Table(tableName, metadata, autoload=True, autoload_with=engine)
        if (param == "" or param == None):
            total = db_session.query(newTable).count()
            oclass = db_session.query(newTable).order_by(desc("ID")).all()[inipage:endpage]
        else:
            total = db_session.query(newTable).filter(newTable.columns._data[param].like("%"+paramvalue+"%")).count()
            oclass = db_session.query(newTable).filter(newTable.columns._data[param].like("%"+paramvalue+"%")).order_by(desc("ID")).all()[
                     inipage:endpage]
        dir = []
        for i in oclass:
            a = 0
            divi = {}
            for j in newTable.columns._data:
                divi[str(j)] = str(i[a])
                a = a + 1
            dir.append(divi)
        jsonoclass = json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        jsonoclass = '{"total"' + ":" + str(total) + ',"rows"' + ":\n" + jsonoclass + "}"
        return jsonoclass
    except Exception as e:
        db_session.rollback()
        print(e)
        logger.error(e)
        insertSyslog("error", "查询报错Error：" + str(e), current_user.Name)

def accurateSelect(data):
    '''
    精确查询
    :param data:
    :return:
    '''
    try:
        pages = int(data.get("offset"))
        rowsnumber = int(data.get("limit"))
        param = data.get("field")
        tableName = data.get("tableName")
        paramvalue = data.get("fieldvalue")
        inipage = pages * rowsnumber + 0  # 起始页
        endpage = pages * rowsnumber + rowsnumber  # 截止页
        newTable = Table(tableName, metadata, autoload=True, autoload_with=engine)
        if (param == "" or param == None):
            total = db_session.query(newTable).count()
            oclass = db_session.query(newTable).order_by(desc("ID")).all()[inipage:endpage]
        else:
            total = db_session.query(newTable).filter(
                newTable.columns._data[param] == paramvalue).count()
            oclass = db_session.query(newTable).filter(
                newTable.columns._data[param] == paramvalue).order_by(desc("ID")).all()[
                     inipage:endpage]
        dir = []
        for i in oclass:
            a = 0
            divi = {}
            for j in newTable.columns._data:
                divi[str(j)] = str(i[a])
                a = a + 1
            dir.append(divi)
        jsonoclass = json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        jsonoclass = '{"total"' + ":" + str(total) + ',"rows"' + ":\n" + jsonoclass + "}"
        return jsonoclass
    except Exception as e:
        db_session.rollback()
        print(e)
        logger.error(e)
        insertSyslog("error", "查询报错Error：" + str(e), current_user.Name)

def FuzzyQuery(tablename, params):
    '''
    :param tablename: 要进行查询的model
    :param params: 一个字典，字典中的key为model的字段，value为进行查询的关键字
    :return: 返回json信息，包含status，message，data
    '''
    if hasattr(tablename, '__tablename__'):
        if isinstance(params, dict) and len(params) > 0:
            for key in params.keys():
                if hasattr(tablename, key):
                    try:
                        data = db_session.query(tablename).filter_by(key = params[key]).all()
                        if data:
                            return json.dumps({'status': 'OK', 'message': '数据更新成功！', 'data':data}, cls=AlchemyEncoder, ensure_ascii=False)
                        else:
                            return json.dumps({'status': 'OK', 'message': '未查询到相关的数据！'}, cls=AlchemyEncoder, ensure_ascii=False)
                    except Exception as e:
                        logger.error(e)
                        insertSyslog("error", "%s数据更新报错："%tablename + str(e), current_user.Name)
                return json.dumps({'status':'error', 'message': '数据查询失败，请输入正确的关键字...'}, cls=AlchemyEncoder, ensure_ascii=False)

        else:
            return json.dumps({'status': 'error', 'message': '系统错误，请联系系统管理员解决...'}, cls=AlchemyEncoder, ensure_ascii=False)
    else:
        return json.dumps({'status': 'error', 'message': '系统错误，请联系系统管理员解决...'}, cls=AlchemyEncoder, ensure_ascii=False)

def ExactQuery(tablename, field, param,type='one'):
    '''
    :param tablename: 需要精确查询的model
    :param field: 查询条件（model的字段）
    :param param: 查询条件的value
    :param type: 查询类型（查询单条type为'one',查询多条为'more'）
    :return: 返回json信息，包含status，message，data
    '''
    if hasattr(tablename, '__tablename__') and hasattr(tablename, field):
        if isinstance(param, str) and len(param) > 0:
            if type == 'one':
                try:
                    one_data = db_session.query(tablename).filter_by(field=param).first()
                    if one_data:
                        return json.dumps({'status': 'OK', 'message': '数据查询成功！', 'data':one_data}, cls=AlchemyEncoder, ensure_ascii=False)
                    else:
                        return json.dumps({'status': 'OK', 'message': '未查询到相关数据！'}, cls=AlchemyEncoder, ensure_ascii=False)
                except Exception as e:
                    logger.error(e)
                    insertSyslog("error", "%s数据更新报错：" % tablename + str(e), current_user.Name)
            if type == 'more':
                try:
                    more_data = db_session.query(tablename).filter_by(field=param).all()
                    if more_data:
                        return json.dumps({'status': 'OK', 'message': '数据查询成功！', 'data':more_data}, cls=AlchemyEncoder, ensure_ascii=False)
                    else:
                        return json.dumps({'status': 'OK', 'message': '未查询到相关数据！'}, cls=AlchemyEncoder, ensure_ascii=False)
                except Exception as e:
                    logger.error(e)
                    insertSyslog("error", "%s数据更新报错：" % tablename + str(e), current_user.Name)
            else:
                return json.dumps({'status': 'error', 'message': '系统错误，请联系系统管理员解决...'}, cls=AlchemyEncoder, ensure_ascii=False)
        return json.dumps({'status': 'error', 'message': '数据查询失败，请输入正确的关键字...'}, cls=AlchemyEncoder, ensure_ascii=False)
    else:
        return json.dumps({'status': 'error', 'message': '系统错误，请联系系统管理员解决...'}, cls=AlchemyEncoder, ensure_ascii=False)
