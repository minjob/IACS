from flask import Blueprint, render_template
from dbset.database.db_operate import db_session
from dbset.log.BK2TLogger import logger,insertSyslog
from flask_login import current_user
from models.system import User

user_manage = Blueprint('user_manage', __name__, template_folder='templates')

# 用户管理
@user_manage.route('/user_manage/userpage')
def userpage():
    # departments = db_session.query(Organization.ID, Organization.OrganizationName).all()
    # # print(departments)
    # # departments = json.dumps(departments, cls=AlchemyEncoder, ensure_ascii=False)
    # data = []
    # for tu in departments:
    #     li = list(tu)
    #     id = li[0]
    #     name = li[1]
    #     department = {'OrganizationID':id,'OrganizationName':name}
    #     data.append(department)
    #
    # dataRoleName = []
    # roleNames = db_session.query(Role.ID, Role.RoleName).all()
    # for role in roleNames:
    #     li = list(role)
    #     id = li[0]
    #     name = li[1]
    #     roleName = {'RoleID': id, 'RoleName': name}
    #     dataRoleName.append(roleName)
    return render_template('./user.html')#, departments=data, roleNames=dataRoleName

@user_manage.route('/user_manage/userselect')
def userselect(data):#table, page, rows, fieid, param
    '''
    :param tablename: 查询表
    :param pages: 页数
    :param rowsnumber: 一页多少行
    :param fieid: 查询字段
    :param param: 查询条件
    :return:用户查询
    '''
    try:
        pages = int(data.get("offset"))
        rowsnumber = int(data.get("limit"))
        param = data.get("field")
        tableName = data.get("tableName")
        paramvalue = data.get("fieldvalue")
        if (paramvalue == "" or paramvalue == None):
            oclass = db_session.query(User).filter(User.WorkNumber == paramvalue).all()
            total = db_session.query(User).filter(User.WorkNumber == paramvalue).count()
        jsonoclass = '{"total"' + ":" + str(total) + ',"rows"' + ":\n" + oclass + "}"
        return jsonoclass
    except Exception as e:
        print(e)
        logger.error(e)
        insertSyslog("error", "用户查询报错Error：" + str(e), current_user.Name)
