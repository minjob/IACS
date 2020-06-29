import json

from flask import Blueprint, request

from dbset.database.db_operate import db_session
from dbset.main.BSFramwork import AlchemyEncoder
from models.core import Role, DepartmentManager, AreaMaintain
from models.system import User, RoleUser

user_manager = Blueprint('user_manager', __name__)


@user_manager.route('/system_tree', methods=['GET'])
def get_user():
    departments = db_session.query(DepartmentManager).all()
    factory = db_session.query(AreaMaintain).first()
    queryset = []
    for department in departments:
        role_query = db_session.query(Role).filter(Role.ParentNode == department.DepartCode).all()
        role_list = []
        for data in role_query:
            d1 = db_session.query(DepartmentManager).filter(DepartmentManager.DepartCode == data.ParentNode).first()
            user_list = {'name': data.RoleName, 'value': data.RoleCode, 'role_description': data.Description, 'type': 'role', 'rid': data.ID, 'did': d1.ID, 'department_name': department.DepartName, 'children': []}
            user_role_query = db_session.query(RoleUser).filter(RoleUser.RoleName == data.RoleName).all()
            for user_role in user_role_query:
                user_query = db_session.query(User).filter(User.ID == user_role.UserID).first()
                if user_query:
                    d2 = db_session.query(DepartmentManager).filter(DepartmentManager.DepartName == user_query.OrganizationName).first()
                    if d2:
                        user_data = {'name': user_query.Name, 'value': user_query.WorkNumber, 'type': 'user', 'rid': data.ID,
                                     'did': d2.ID}
                    else:
                        user_data = {'name': user_query.Name, 'value': user_query.WorkNumber, 'type': 'user', 'rid': data.ID, 'did': ''}
                    # for user in user_query:
                    #     d2 = db_session.query(DepartmentManager).filter(DepartmentManager.DepartName == user.OrganizationName).first()
                    #     if d2:
                    #         user_data = {'name': user.Name, 'value': user.WorkNumber, 'type': 'user', 'rid': data.ID, 'did': d2.ID}
                    #     else:
                    #         user_data = {'name': user.Name, 'value': user.WorkNumber, 'type': 'user', 'rid': data.ID, 'did': ''}
                    user_list['children'].append(user_data)
            role_list.append(user_list)
        department_data = {'name': department.DepartName, 'value': department.DepartCode, 'type': 'department', 'did': department.ID, 'factory_name': factory.FactoryName, 'children': role_list}
        area = db_session.query(AreaMaintain).filter(AreaMaintain.FactoryName == department.DepartLoad).first()
        if area:
            department_data['fid'] = area.ID
        queryset.append(department_data)
    data = {'name': factory.FactoryName, 'value': factory.AreaCode, 'type': 'factory', 'fid': factory.ID, 'children': queryset}
    return json.dumps(data, cls=AlchemyEncoder, ensure_ascii=False)


@user_manager.route('/system_tree/add_department', methods=['POST'])
def add_department():
    did = request.json.get('department_code')
    dname = request.json.get('department_name')
    fname = request.json.get('factory_name')
    depart = DepartmentManager(DepartCode=did, DepartName=dname, DepartLoad=fname)
    db_session.add(depart)
    db_session.commit()
    return json.dumps({'code': 10000, 'msg': '新增成功', 'data': {'Did': depart.ID}})


@user_manager.route('/system_tree/delete_department', methods=['DELETE'])
def delete_department():
    code = request.headers.get('department_code')
    department = db_session.query(DepartmentManager).filter(DepartmentManager.DepartCode == code).first()
    role_query = db_session.query(Role).filter(Role.ParentNode == department.DepartCode).all()
    for item in role_query:
        item.ParentNode = ''
    db_session.commit()
    user_query = db_session.query(User).filter(User.OrganizationName == department.DepartName).all()
    for item in user_query:
        item.OrganizationName = ''
    db_session.commit()
    db_session.delete(department)
    db_session.commit()
    return json.dumps({'code': 10001, 'msg': '删除成功'})


@user_manager.route('/system_tree/update_department', methods=['PATCH'])
def update_department():
    did = request.json.get('did')
    code = request.json.get('department_code')
    department_name = request.json.get('department_name')
    department = db_session.query(DepartmentManager).filter(DepartmentManager.ID == int(did)).first()
    role_query = db_session.query(Role).filter(Role.ParentNode == department.DepartCode).all()
    for item in role_query:
        item.ParentNode = code
    department.DepartCode = code
    department.DepartName = department_name
    db_session.commit()
    user_query = db_session.query(User).filter(User.OrganizationName == department.DepartName).all()
    for user in user_query:
        user.OrganizationName = department_name
    db_session.commit()
    return json.dumps({'code': 10002, 'msg': '更新成功'})


@user_manager.route('/system_tree/add_role', methods=['POST'])
def add_role():
    rcode = request.json.get('role_code')
    did = request.json.get('did')
    rname = request.json.get('role_name')
    rdes = request.json.get('role_description')
    department = db_session.query(DepartmentManager).filter(DepartmentManager.ID == int(did)).first()
    role = Role(RoleCode=rcode, RoleName=rname, Description=rdes, ParentNode=department.DepartCode)
    db_session.add(role)
    db_session.commit()
    return json.dumps({'code': 10003, 'msg': '新增成功', 'data': {'rid': role.ID}})


@user_manager.route('/system_tree/delete_role', methods=['DELETE'])
def delete_role():
    rid = request.headers.get('rid')
    role = db_session.query(Role).filter(Role.ID == rid).first()
    user_query = db_session.query(RoleUser).filter(RoleUser.RoleName == role.RoleName).all()
    for item in user_query:
        db_session.delete(item)
    db_session.delete(role)
    db_session.commit()
    return json.dumps({'code': 10004, 'msg': '删除成功'})


@user_manager.route('/system_tree/update_role', methods=['PATCH'])
def update_role():
    rid = request.json.get('rid')
    code = request.json.get('role_code')
    role_name = request.json.get('role_name')
    rdes = request.json.get('role_description')
    role = db_session.query(Role).filter(Role.ID == rid).first()
    user_query = db_session.query(RoleUser).filter(RoleUser.RoleName == role.RoleName).all()
    for item in user_query:
        item.RoleName = role_name
    role.RoleCode = code
    role.RoleName = role_name
    role.Description = rdes
    db_session.commit()
    return json.dumps({'code': 10005, 'msg': '更新成功'})


# @user_manager.route('/system_tree/add_user', methods=['POST'])
# def add_user():
#     rid = request.json.get('role_code')
#     did = request.json.get('did')
#     rname = request.json.get('role_name')
#     fname = request.json.get('factory_name')
#     role = db_session.query(Role).filter(Role.ID == rid).first()
#     department = db_session.query(DepartmentManager).filter(DepartmentManager.ID == did).first()
#     role = User(DepartCode=rid, DepartName=rname, DepartLoad=fname)
#     db_session.add(role)
#     db_session.commit()
#     return json.dumps({'code': 10003, 'msg': '新增成功', 'data': {'Did': role.ID}})


