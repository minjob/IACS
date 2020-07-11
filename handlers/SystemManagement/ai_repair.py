import json
import os
import time

import xlrd
from flask import Blueprint, request
from flask_login import current_user

from dbset.database.db_operate import db_session
from dbset.main.BSFramwork import AlchemyEncoder
from models.system import Repair, Equipment, RepairTask, KeepPlan, KeepTask, KeepRecord

repair = Blueprint('repair', __name__)


def get_time_stamp(s):
    time_array = time.strptime(s, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_array))
    return 0 < int(time.time()) - time_stamp < 604800


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
        task_data = RepairTask(EquipmentCode=data.EquipmentCode, No=data.No, Status='维修完成', Worker=data.Worker,
                               ReceiveWorker=data.ReceiveWorker, Content=json_data.get('Content'),
                               ApplyTime=data.ApplyTime, ReceiveTime=data.ReceiveTime,
                               EndTime=json_data.get('EndTime'))
        equipment = db_session.query(Equipment).filter_by(EquipmentCode=json_data.get('EquipmentCode')).first()
        equipment.Status = '运行中'
        db_session.add_all([task_data, equipment])
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
    data = db_session.query(RepairTask).filter(RepairTask.EquipmentCode == p).order_by(
        RepairTask.ApplyTime.desc()).limit(limit).offset((offset - 1) * limit)
    return json.dumps({'code': '10001', 'message': '操作成功', 'data': {'rows': data.all(), 'total': total}},
                      cls=AlchemyEncoder, ensure_ascii=True)


@repair.route('/keep_plan', methods=['POST'])
def keep_plans():
    # if request.method == 'GET':
    #     data = db_session.query(Repair).all()
    #     return json.dumps({'code': '10001', 'message': '操作成功', 'data': data}, cls=AlchemyEncoder, ensure_ascii=True)
    # if request.method == 'POST':
    json_data = request.json.get('params')
    data = KeepPlan(EquipmentCode=json_data.get('EquipmentCode'), No=get_no(json_data.get('ApplyTime')),
                    Worker=current_user.Name, ApplyTime=json_data.get('ApplyTime'),
                    StartTime=json_data.get('StartTime'), Describe=json_data.get('Describe'),
                    WeekTime=json_data.get('WeekTime'))
    db_session.add(data)
    db_session.commit()
    db_session.close()
    return json.dumps({'code': '10001', 'message': '操作成功'}, cls=AlchemyEncoder, ensure_ascii=True)


@repair.route('/keep_task', methods=['GET'])
def task():
    query_data = db_session.query(KeepPlan).filter_by(Status='待保养').all()
    if request.method == 'GET':
        # 每页多少条
        limit = int(request.values.get('limit'))
        # 当前页
        offset = int(request.values.get('offset'))
        for item in query_data:
            q = db_session.query(KeepTask).filter_by(No=item.No).first()
            if not q and get_time_stamp(item.StartTime):
                data = KeepTask(EquipmentCode=item.EquipmentCode, No=item.No, Worker=item.Worker, Status=item.Status,
                                ApplyTime=item.ApplyTime, StartTime=item.StartTime, Content=item.Content,
                                WeekTime=item.WeekTime)
                db_session.add(data)
                db_session.commit()
            else:
                pass
        data = db_session.query(KeepTask).order_by(KeepTask.ApplyTime.desc()).limit(limit).offset((offset - 1) * limit)
        total = db_session.query(KeepTask).count()
        return json.dumps({'code': '10001', 'message': '操作成功', 'data': {'rows': data.all(), 'total': total}}, cls=AlchemyEncoder,
                          ensure_ascii=True)
    elif request.method == 'POST':
        no = request.args.get('No')
        endtime = request.args.get('EndTime')
        content = request.args.get('Content')
        item = db_session.query(KeepTask).filter_by(No=no).first()
        data = KeepRecord(EquipmentCode=item.EquipmentCode, No=no, Worker=item.Worker, Status='已完成',
                          KeepWorker=current_user.Name, ApplyTime=item.ApplyTime, StartTime=item.StartTime,
                          Describe=item.Describe, Content=content, WeekTime=item.WeekTime, EndTime=endtime)
        db_session.add(data)
        db_session.commit()
        return json.dumps({'code': '10001', 'message': '操作成功'}, cls=AlchemyEncoder, ensure_ascii=True)


@repair.route('/keep_record/<no>', methods=['GET'])
def keep_record(no):
    # 每页多少条
    limit = int(request.values.get('limit'))
    # 当前页
    offset = int(request.values.get('offset'))
    total = db_session.query(KeepRecord).filter_by(No=no).count()
    data = db_session.query(KeepRecord).filter(KeepRecord.No == no).order_by(
        RepairTask.ApplyTime.desc()).limit(limit).offset((offset - 1) * limit)
    return json.dumps({'code': '10001', 'message': '操作成功', 'data': {'rows': data.all(), 'total': total}},
                      cls=AlchemyEncoder, ensure_ascii=True)

