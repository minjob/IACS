from flask import Blueprint, render_template, request
import json
from flask_login import current_user
from dbset.main.BSFramwork import AlchemyEncoder
from models.system import Organization
from dbset.log.BK2TLogger import logger,insertSyslog
from dbset.database.db_operate import db_session
from models.core import Factory, DepartmentManager, Role

organiza = Blueprint('organiza', __name__, template_folder='templates')

# 组织机构建模
@organiza.route('/organization')
def organization():
    return render_template('./sysOrganization.html')

#  企业管理
@organiza.route('/sysyEnterprise')
def sysyEnterprise():
    return render_template('./sysyEnterprise.html')

# 厂区管理
@organiza.route('/sysFactory')
def sysFactory():
    return render_template('./sysFactory.html')

#  部门管理
@organiza.route('/sysDepartment')
def sysDepartment():
    return render_template('./sysDepartment.html')

#  岗位管理
@organiza.route('/sysStation')
def sysStation():
    return render_template('./sysStation.html')

@organiza.route('/organizationMap')
def organizationMap():
    return render_template('./index_organization.html')

@organiza.route('/organizationMap/selectAll')#组织结构
def selectAll():
    if request.method == 'GET':
        try:
            return json.dumps(getMyOrganizationChildrenMap(id=0), cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            insertSyslog("error", "查询组织结构报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)
def getMyOrganizationChildrenMap(id):
    sz = []
    try:
        orgs = db_session.query(Organization).filter().all()
        for obj in orgs:
            if obj.ParentNode == id:
                sz.append(
                    {"name": obj.OrganizationName, "value": obj.ID, "children": getMyOrganizationChildrenMap(obj.ID)})
        return sz
    except Exception as e:
        print(e)
        return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

@organiza.route('/Myorganization')
def myorganization():
    return render_template('./SystemManagement/Myorganization.html')
def getMyOrganizationChildren(id=0):
    sz = []
    try:
        orgs = db_session.query(Organization).filter().all()
        for obj in orgs:
            if obj.ParentNode == id:
                sz.append({"id": obj.ID, "text": obj.OrganizationName, "nodes": getMyOrganizationChildren(obj.ID)})
        srep = ',' + 'items' + ':' + '[]'
        # data = string(sz)
        # data.replace(srep, '')
        return sz
    except Exception as e:
        print(e)
        return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)
def getMyEnterprise(id=0):
    sz = []
    try:
        orgs = db_session.query(Organization).filter().all()
        for obj in orgs:
            sz.append({"id": obj.ID, "text": obj.OrganizationName, "group": obj.ParentNode})
        return sz
    except Exception as e:
        print(e)
        logger.error(e)
        insertSyslog("error", "获取树形结构报错Error：" + str(e), current_user.Name)
        return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)
@organiza.route('/MyOp')
def MyOpFind():
    if request.method == 'GET':
        try:
            data = getMyOP(id=0)
            return json.dumps(data, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)
def getMyOP(id):
    sz = []
    try:
        orgs = db_session.query(Organization).filter().all()
        for obj in orgs:
            if obj.ParentNode == id:
                sz.append(
                    {"text": obj.OrganizationName, "value": obj.ID, "nodes": getMyOP(obj.ID)})
        return sz
    except Exception as e:
        print(e)
        return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

@organiza.route('/Myenterprise')
def myenterprise():
    if request.method == 'GET':
        try:
            return json.dumps(getMyEnterprise(id=0), cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

# 组织架构图
@organiza.route('/organizationTU', methods=['POST', 'GET'])
def organizationTU():
    if request.method == 'GET':
        data = request.values
        try:
            dic = []
            facs = db_session.query(Factory).all()
            for fa in facs:
                deps = db_session.query(DepartmentManager).filter(DepartmentManager.DepartLoad == fa.FactoryName).all()
                for dep in deps:
                    die = []
                    die.append(fa.FactoryName)
                    die.append(dep.DepartName)
                    dic.append(die)
                    ros = db_session.query(Role).filter(Role.ParentNode == dep.DepartName).all()
                    for ro in ros:
                        dif = []
                        dif.append(dep.DepartName)
                        dif.append(ro.RoleName)
                        dic.append(dif)
            return json.dumps(dic, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "组织架构图报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)