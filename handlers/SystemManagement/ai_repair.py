import json
import os
import time

import xlrd
from flask import Blueprint, request
from flask_login import current_user

from dbset.database.db_operate import db_session
from dbset.main.BSFramwork import AlchemyEncoder
from models.system import Repair, Plan, RepairTask

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
        db_session.add(data)
        db_session.commit()
        return json.dumps({'code': '10000', 'message': '操作成功'}, cls=AlchemyEncoder, ensure_ascii=True)


@repair.route('/repair_task/<p>', methods=['GET', 'POST'])
def repair_tasks(p):
    if p == 'jiedan':
        no = request.args.get('No')
        data = db_session.query(Repair).filter_by(No=no).first()
        data.Status = '维修中'
        data.ReceiveTime = request.args.get('Time')
        db_session.add(data)
        db_session.commit()
        return json.dumps({'code': '10001', 'message': '操作成功'}, cls=AlchemyEncoder, ensure_ascii=True)
    if p == 'over':
        no = request.args.get('No')
        data = db_session.query(Repair).filter_by(No=no).first()
        task = RepairTask(EquipmentCode=data.EquipmentCode, No=data.No, Status='维修完成', Worker=data.Worker,
                          ReceiveWorker=data.ReceiveWorker, Content=request.args.get('Content'), Name='',
                          ApplyTime=data.ApplyTime, ReceiveTime=data.ReceiveTime,
                          EndTime=request.args.get('EndTime'))
        db_session.add(task)
        db_session.commit()
        return json.dumps({'code': '10001', 'message': '操作成功'}, cls=AlchemyEncoder, ensure_ascii=True)


@repair.route('/record/<p>', methods=['GET', 'POST'])
def record(p):
    # 每页多少条
    limit = request.args.get('limit')
    # 当前页
    offset = request.args.get('offset')
    data = db_session.query(RepairTask).filter_by(EquipmentCode=p).all()
    return json.dumps({'code': '10001', 'message': '操作成功', 'data': {'rows': data, 'total': len(data)}}, cls=AlchemyEncoder, ensure_ascii=True)
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
