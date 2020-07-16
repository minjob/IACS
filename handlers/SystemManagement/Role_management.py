import json
from flask import render_template,request,Blueprint

from dbset.database.db_operate import db_session
from models.core import Role
from models.system import User, RoleUser
from flask_login import current_user
from dbset.log.BK2TLogger import logger,insertSyslog
from dbset.main.BSFramwork import AlchemyEncoder

role_management = Blueprint('role_management', __name__, template_folder='templates')
# 工作台菜单role
@role_management.route('/sysrole')
def sysrole():

    # dataRoleInfo = []
    # roleNames = db_session.query(Role.ID, Role.RoleName).all()
    # for role in roleNames:
    #     li = list(role)
    #     id = li[0]
    #     name = li[1]
    #     roleName = {'RoleID': id, 'RoleName': name}
    #     dataRoleInfo.append(roleName)
    return render_template('./sysRole.html') #RoleInfos=dataRoleInfo

@role_management.route('/role_management/saveroleuser', methods=['POST', 'GET'])
def saveroleuser():
    '''
    用户添加角色
    :return:
    '''
    if request.method == 'POST':
        data = request.values
        try:
            UserID = data.get("UserID")
            RoleIDs = data.get("RoleIDs")
            if RoleIDs:
                RoleIDs = eval(RoleIDs)
            userclass = db_session.query(User).filter(User.ID == int(UserID)).first()
            sql = "delete from RoleUser where UserID = " + UserID
            db_session.execute(sql)
            db_session.commit()
            for pid in RoleIDs:
                rolecalss = db_session.query(Role).filter(Role.ID == int(pid)).first()
                rpclas = db_session.query(RoleUser).filter(RoleUser.UserID == userclass.ID, RoleUser.RoleID == rolecalss.ID).first()
                if not rpclas:
                    rp = RoleUser()
                    rp.UserID = userclass.ID
                    rp.UserName = userclass.Name
                    rp.RoleID = rolecalss.ID
                    rp.RoleName = rolecalss.RoleName
                    db_session.add(rp)
                    db_session.commit()
            return json.dumps("OK", cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            db_session.rollback()
            print(e)
            logger.error(e)
            insertSyslog("error", "用户添加角色Error：" + str(e), current_user.Name)

@role_management.route('/role_management/selectrolebyuser', methods=['POST', 'GET'])
def selectrolebyuser():
    '''
    根据用户查询角色
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            dir = {}
            UserID = data.get("UserID")
            pids = db_session.query(RoleUser).filter(RoleUser.UserID == int(UserID)).all()
            perids_list = []
            for pid in pids:
                perids_list.append(pid.RoleID)
            if len(perids_list) > 0:
                existingRows = db_session.query(Role).filter(Role.ID.in_(perids_list)).all()
                dir["existingRows"] = existingRows
            else:
                dir["existingRows"] = []
            notHaveRows = db_session.query(Role).filter().all()
            dir["notHaveRows"] = notHaveRows
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "根据用户查询角色Error：" + str(e), current_user.Name)