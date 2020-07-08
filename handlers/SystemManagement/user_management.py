from flask import Blueprint, render_template
from dbset.database.db_operate import db_session
from dbset.log.BK2TLogger import logger,insertSyslog
from flask_login import current_user
from models.system import User
from flask import render_template,request,Blueprint

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


@user_manage.route('/permission/saverolepermission', methods=['POST', 'GET'])
def saverolepermission():
    '''
    用户添加权限
    :return:
    '''
    if request.method == 'POST':
        data = request.values
        try:
            roleID = data.get("roleID")
            permissionIDs = data.get("permissionIDs")
            if permissionIDs:
                permissionIDs = eval(permissionIDs)
            roleclass = db_session.query(Role).filter(Role.ID == int(roleID)).first()
            sql = "delete from [DB_MICS].[dbo].[RolePermission] where [RoleID] = " + roleID
            db_session.execute(sql)
            db_session.commit()
            for pid in permissionIDs:
                permissioncalss = db_session.query(Permission).filter(Permission.ID == int(pid)).first()
                rpclas = db_session.query(RolePermission).filter(RolePermission.RoleID == roleclass.ID, RolePermission.PermissionID == permissioncalss.ID).first()
                if not rpclas:
                    rp = RolePermission()
                    rp.RoleID = roleclass.ID
                    rp.RoleName = roleclass.RoleName
                    rp.PermissionID = permissioncalss.ID
                    rp.PermissionName = permissioncalss.PermissionName
                    db_session.add(rp)
                    db_session.commit()
            return json.dumps("OK", cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            db_session.rollback()
            print(e)
            logger.error(e)
            insertSyslog("error", "角色添加权限Error：" + str(e), current_user.Name)

@user_manage.route('/permission/selectpermissionbyrole', methods=['POST', 'GET'])
def selectpermissionbyrole():
    '''
    根据角色查询权限
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            dir = {}
            roleID = data.get("roleID")
            pids = db_session.query(RolePermission).filter(RolePermission.RoleID == int(roleID)).all()
            perids_list = []
            for pid in pids:
                perids_list.append(pid.PermissionID)
            if len(perids_list) > 0:
                existingRows = db_session.query(Permission).filter(Permission.ID.in_(perids_list)).all()
                dir["existingRows"] = existingRows
            else:
                dir["existingRows"] = []
            notHaveRows = db_session.query(Permission).filter().all()
            dir["notHaveRows"] = notHaveRows
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "根据角色查询权限Error：" + str(e), current_user.Name)

@permission_distribution.route('/permission/selectpermissionbyuser', methods=['POST', 'GET'])
def selectpermissionbyuser():
    '''
    根据用户查询权限
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            PermissionName = data.get("PermissionName")
            sql = "SELECT [UserID] AS UserID FROM [DB_MICS].[dbo].[RoleUser] t INNER JOIN [DB_MICS].[dbo].[RolePermission] p ON t.RoleID = p.RoleID WHERE P.PermissionName = '"+PermissionName+"'"
            oclass = db_session.execute(sql).fetchall()
            db_session.close()
            user_ids = []
            UserID = db_session.query(User.ID).filter(User.WorkNumber == current_user.WorkNumber).first()[0]
            for userid in oclass:
                user_ids.append(userid['UserID'])
            if UserID in user_ids:
                return 'OK'
            else:
                return '没有此权限'
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "根据用户查询权限Error：" + str(e), current_user.Name)

