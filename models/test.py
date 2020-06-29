import json
from flask import Blueprint, request
from dbset.log.BK2TLogger import logger
from dbset.main.BSFramwork import AlchemyEncoder
from dbset.database.db_operate import db_session

from models.core import Role

login_auth = Blueprint('login_auth', __name__, template_folder='templates')

@login_auth.route('/addrole', methods=['GET', 'POST'])
def addrole():
    '''
    添加角色
    :return:
    '''
    try:
        if request.method == 'POST':
            role = Role()
            role.RoleName = "角色名字"
            role.Description = ""
            role.RoleCode = "角色编码"
            db_session.add(role)
            db_session.commit()
    except Exception as e:
        print(e)
        db_session.rollback()
        logger.error(e)
        return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

@login_auth.route('/deleterole', methods=['GET', 'POST'])
def deleterole():
    '''
    删除角色
    :return:
    '''
    try:
        if request.method == 'POST':
            data = request.values
            ID = data.get("ID")
            role = db_session.query(Role).filter(Role.ID == ID).first()
            db_session.delete(role)
            db_session.commit()
    except Exception as e:
        print(e)
        db_session.rollback()
        logger.error(e)
        return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

@login_auth.route('/selectrole', methods=['GET', 'POST'])
def selectrole():
    '''
    查询角色
    :return:
    '''
    try:
        if request.method == 'POST':
            data = request.values
            ID = data.get("ID")
            oclass = db_session.query(Role).filter(Role.ID == ID).first()
            return json.dumps(oclass, cls=AlchemyEncoder, ensure_ascii=False)
    except Exception as e:
        print(e)
        db_session.rollback()
        logger.error(e)
        return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

@login_auth.route('/updaterole', methods=['GET', 'POST'])
def updaterole():
    '''
    修改角色
    :return:
    '''
    try:
        if request.method == 'POST':
            data = request.values
            ID = data.get("ID")
            oclass = db_session.query(Role).filter(Role.ID == ID).first()
            oclass.RoleName = "角色名字1"
            db_session.commit()
    except Exception as e:
        print(e)
        db_session.rollback()
        logger.error(e)
        return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)