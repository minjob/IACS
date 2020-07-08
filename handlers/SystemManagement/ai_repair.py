import json
import os
import time

import xlrd
from flask import Blueprint, request

from dbset.database.db_operate import db_session
from dbset.main.BSFramwork import AlchemyEncoder
from models.system import Record, Plan, Task

repair = Blueprint('repair', __name__)


def get_time_stamp(s):
    time_array = time.strptime(s)
    time_stamp = int(time.mktime(time_array))
    return 0 < int(time.time()) - time_stamp < 86400


@repair.route('/input', methods=['GET', 'POST'])
def input_plan():
    json_data = request.values
    plan = Plan(EquipmentCode=json_data.get('EquipmentCode'), Status=json_data.get('Status'),
                RemindStatus=json_data.get('RemindStatus'), WorkTime=json_data.get('WorkTime'))
    db_session.add(plan)
    db_session.commit()
    return json.dumps({'message': '操作成功'}, cls=AlchemyEncoder, ensure_ascii=False)


@repair.route('/task', methods=['GET', 'POST'])
def task():
    query_data = db_session.query(Plan).filter_by(Status='待处理').all()
    if request.method == 'GET':
        for item in query_data:
            if get_time_stamp(item.work_time):
                data = Task(EquipmentCode=item.EquipmentCode, WorkNo=item.WorkNo, Status=item.Status,
                            Type=item.Type, FoundTime=item.WorkTime)
                db_session.add(data)
                db_session.commit()
                # query_list.append(item)
            else:
                pass
        return json.dumps({'code': '1000', 'message': '操作成功', 'data': query_data}, cls=AlchemyEncoder, ensure_ascii=True)
    elif request.method == 'POST':
        # query_list = [item if get_time_stamp(item.work_time) else '' for item in query_data]
        # query_list = []
        for item in query_data:
            if get_time_stamp(item.work_time):
                data = Task(EquipmentCode=item.EquipmentCode, WorkNo=item.WorkNo, Status=item.Status,
                            Type=item.Type, FoundTime=item.WorkTime)
                db_session.add(data)
                db_session.commit()
                # query_list.append(item)
            else:
                pass
        return json.dumps({'code': '1000', 'message': '操作成功'}, cls=AlchemyEncoder, ensure_ascii=True)


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
    pass