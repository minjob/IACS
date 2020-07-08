import json
from flask import Blueprint, render_template
from dbset.database.db_operate import db_session
from dbset.log.BK2TLogger import logger,insertSyslog
from flask_login import current_user
from models.system import User, ShiftsGroup, UserShiftsGroup
from flask import render_template,request,Blueprint
from dbset.main.BSFramwork import AlchemyEncoder

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


@user_manage.route('/saveuserusershiftsgroup', methods=['POST', 'GET'])
def saveuserusershiftsgroup():
    '''
    用户添加班组
    :return:
    '''
    if request.method == 'POST':
        data = request.values
        try:
            userID = data.get("userID")
            shiftsgroupIDs = data.get("shiftsgroupIDs")
            if shiftsgroupIDs:
                shiftsgroupIDs = eval(shiftsgroupIDs)
            userclass = db_session.query(User).filter(User.ID == int(userID)).first()
            sql = "delete from usershiftsgroup where UserID = " + userID
            db_session.execute(sql)
            db_session.commit()
            for pid in shiftsgroupIDs:
                shiftsgroupcalss = db_session.query(ShiftsGroup).filter(ShiftsGroup.ID == int(pid)).first()
                rpclas = db_session.query(UserShiftsGroup).filter(UserShiftsGroup.UserID == userclass.ID, UserShiftsGroup.ShiftsGroupID == shiftsgroupcalss.ID).first()
                if not rpclas:
                    rp = UserShiftsGroup()
                    rp.UserID = userclass.ID
                    rp.Name = userclass.Name
                    rp.ShiftsGroupID = shiftsgroupcalss.ID
                    rp.ShiftsGroupName = shiftsgroupcalss.ShiftsGroupName
                    db_session.add(rp)
                    db_session.commit()
            return json.dumps("OK", cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            db_session.rollback()
            print(e)
            logger.error(e)
            insertSyslog("error", "角色添加权限Error：" + str(e), current_user.Name)

@user_manage.route('/selectUserShiftsGroup', methods=['POST', 'GET'])
def selectUserShiftsGroup():
    '''
    根据用户查班组
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            dir = {}
            userID = data.get("userID")
            pids = db_session.query(UserShiftsGroup).filter(UserShiftsGroup.UserID == int(userID)).all()
            perids_list = []
            for pid in pids:
                perids_list.append(pid.PermissionID)
            if len(perids_list) > 0:
                existingRows = db_session.query(ShiftsGroup).filter(ShiftsGroup.ID.in_(perids_list)).all()
                dir["existingRows"] = existingRows
            else:
                dir["existingRows"] = []
            notHaveRows = db_session.query(ShiftsGroup).filter().all()
            dir["notHaveRows"] = notHaveRows
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "根据角色查询权限Error：" + str(e), current_user.Name)


