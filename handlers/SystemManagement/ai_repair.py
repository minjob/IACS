import json
import os
import time

import xlrd
from flask import Blueprint, request
from flask_login import current_user

from dbset.database.db_operate import db_session
from dbset.main.BSFramwork import AlchemyEncoder
from models.system import Repair, Equipment, RepairTask

repair = Blueprint('repair', __name__)


def get_time_stamp(s):
    time_array = time.strptime(s)
    time_stamp = int(time.mktime(time_array))
    return 0 < int(time.time()) - time_stamp < 86400


def get_no(no):
    return str(str(str(no).replace('-', '')).replace(':', '')).replace(' ', '')


@repair.route('/repair', methods=['GET', 'POST'])
def repairs():
    if request.method == 'GET':
        data = db_session.query(Repair).all()
        return json.dumps({'code': '10001', 'message': '操作成功', 'data': data}, cls=AlchemyEncoder, ensure_ascii=True)
    if request.method == 'POST':
        json_data = request.json.get('params')
        data = Repair(EquipmentCode=json_data.get('EquipmentCode'), No=get_no(json_data.get('ApplyTime')),
                      Worker=current_user.Name, ApplyTime=json_data.get('ApplyTime'),
                      FaultExpound=json_data.get('FaultExpound'))
        equipment = db_session.query(Equipment).filter_by(EquipmentCode=json_data.get('EquipmentCode')).first()
        equipment.Status = '待接单'
        db_session.add_all([data, equipment])
        db_session.commit()
        db_session.close()
        return json.dumps({'code': '10000', 'message': '操作成功'}, cls=AlchemyEncoder, ensure_ascii=True)


@repair.route('/repair_task/<p>', methods=['PATCH'])
def repair_tasks(p):
    if p == 'jiedan':
        json_data = request.json.get('params')
        data = db_session.query(Repair).filter_by(No=json_data.get('No')).first()
        data.Status = '维修中'
        data.ReceiveWorker = current_user.Name
        data.ReceiveTime = json_data.get('Time')
        equipment = db_session.query(Equipment).filter_by(EquipmentCode=json_data.get('EquipmentCode')).first()
        equipment.Status = '维修中'
        db_session.add_all([data, equipment])
        db_session.commit()
        db_session.close()
        return json.dumps({'code': '10001', 'message': '操作成功'}, cls=AlchemyEncoder, ensure_ascii=True)
    if p == 'over':
        json_data = request.json.get('params')
        data = db_session.query(Repair).filter_by(No=json_data.get('No')).first()
        task = RepairTask(EquipmentCode=data.EquipmentCode, No=data.No, Status='维修完成', Worker=data.Worker,
                          ReceiveWorker=data.ReceiveWorker, Content=json_data.get('Content'),
                          ApplyTime=data.ApplyTime, ReceiveTime=data.ReceiveTime,
                          EndTime=json_data.get('EndTime'))
        equipment = db_session.query(Equipment).filter_by(EquipmentCode=json_data.get('EquipmentCode')).first()
        equipment.Status = '运行中'
        db_session.add_all([task, equipment])
        db_session.delete(data)
        db_session.commit()
        db_session.close()
        return json.dumps({'code': '10001', 'message': '操作成功'}, cls=AlchemyEncoder, ensure_ascii=True)


@repair.route('/record/<p>', methods=['GET', 'POST'])
def record(p):
    # 每页多少条
    limit = int(request.values.get('limit'))
    # 当前页
    offset = int(request.values.get('offset'))
    total = db_session.query(RepairTask).filter_by(EquipmentCode=p).count()
    data = db_session.query(RepairTask).filter(RepairTask.EquipmentCode == p).order_by(RepairTask.ApplyTime.desc()).limit(limit).offset((offset-1)*limit)
    return json.dumps({'code': '10001', 'message': '操作成功', 'data': {'rows': data.all(), 'total': total}}, cls=AlchemyEncoder, ensure_ascii=True)


# @repair.route('/task', methods=['GET', 'POST'])
# def task():
#     query_data = db_session.query(Plan).filter_by(Status='待处理').all()
#     if request.method == 'GET':
#         for item in query_data:
#             if get_time_stamp(item.work_time):
#                 data = Task(EquipmentCode=item.EquipmentCode, WorkNo=item.WorkNo, Status=item.Status,
#                             Type=item.Type, FoundTime=item.WorkTime)
#                 db_session.add(data)
#                 db_session.commit()
#                 # query_list.append(item)
#             else:
#                 pass
#         return json.dumps({'code': '1000', 'message': '操作成功', 'data': query_data}, cls=AlchemyEncoder, ensure_ascii=True)
#     elif request.method == 'POST':
#         # query_list = [item if get_time_stamp(item.work_time) else '' for item in query_data]
#         # query_list = []
#         for item in query_data:
#             if get_time_stamp(item.work_time):
#                 data = Task(EquipmentCode=item.EquipmentCode, WorkNo=item.WorkNo, Status=item.Status,
#                             Type=item.Type, FoundTime=item.WorkTime)
#                 db_session.add(data)
#                 db_session.commit()
#                 # query_list.append(item)
#             else:
#                 pass
#         return json.dumps({'code': '1000', 'message': '操作成功'}, cls=AlchemyEncoder, ensure_ascii=True)


# @repair.route('/record', methods=['GET', 'POST'])
# def record():
#     root_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
#     file_path = os.path.join(root_path, 'work.xlsx')
#     data = xlrd.open_workbook(file_path)
#     print('查看工作表', data.sheet_names())
#     table = data.sheet_by_index(0)
#
#     print(table.nrows)
#     for rowNum in range(table.nrows):
#         if rowNum != 0:
#             rowValue = table.row_values(rowNum)
#             plan = Plan(EquipmentCode=rowValue[0], Status=rowValue[1],
#                         RemindStatus=rowValue[2], WorkTime=rowValue[3])
#             db_session.add(plan)
#             db_session.commit()
# for colNum in range(table.ncols):
#     if colNum > 0 and colNum == 0:
#         print(int(rowValue[0]))
#     else:
#         print(rowValue[colNum])
# print("++"*10)
# pass
