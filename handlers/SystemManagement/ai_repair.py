import json
import os
import time

import xlrd
from flask import Blueprint, request
from flask_login import current_user

from dbset.database.db_operate import db_session
from dbset.main.BSFramwork import AlchemyEncoder
from models.system import Repair, Equipment, RepairTask, KeepPlan, KeepTask, KeepRecord
from tools.common import logger, insertSyslog

repair = Blueprint('repair', __name__)


def add_date(week, work_time):
    """
    递增预工作时间
    :param week: 工作周期
    :param work_time: 预计工作时间
    :return:
    """
    """递增周期"""
    time_array = time.strptime(work_time, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_array))
    if week[1] == '周':
        new_time_stamp = time_stamp + 604800 * int(week[0])
        new_time_array = time.localtime(new_time_stamp)
        new_time = time.strftime("%Y-%m-%d %H:%M:%S", new_time_array)
        return new_time
    elif week[1] == '月':
        new_time_stamp = time_stamp + 86400 * 30 * int(week[0])
        new_time_array = time.localtime(new_time_stamp)
        new_time = time.strftime("%Y-%m-%d %H:%M:%S", new_time_array)
        return new_time
    elif week[1] == '年':
        new_time_stamp = time_stamp + 86400 * 365 * int(week[0])
        new_time_array = time.localtime(new_time_stamp)
        new_time = time.strftime("%Y-%m-%d %H:%M:%S", new_time_array)
        return new_time


def get_time_stamp(work_time):
    """
    计算工作时间间隔
    :param work_time: 预工作时间
    :return:
    """
    time_array = time.strptime(work_time, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_array))
    # 倒数三天
    # return 0 < time_stamp - int(time.time()) < 259200
    # 倒数7天
    return 0 < time_stamp - int(time.time()) < 604800
    # 倒数47天
    # return 0 < time_stamp - int(time.time()) < 604800 * 7


def get_no(no):
    """自动生成工单号"""
    return str(str(str(no).replace('-', '')).replace(':', '')).replace(' ', '')


@repair.route('/repair', methods=['GET', 'POST'])
def repairs():
    """
    添加设备维修任务
    :return:
    """
    if request.method == 'GET':
        data = db_session.query(Repair).all()
        return json.dumps({'code': '10001', 'message': '操作成功', 'data': data}, cls=AlchemyEncoder, ensure_ascii=False)
    if request.method == 'POST':
        json_data = request.values
        data = Repair(EquipmentCode=json_data.get('EquipmentCode'), No=get_no(json_data.get('ApplyTime')),
                      Worker=current_user.Name, ApplyTime=json_data.get('ApplyTime'),
                      FaultExpound=json_data.get('FaultExpound'))
        equipment = db_session.query(Equipment).filter_by(EquipmentCode=json_data.get('EquipmentCode')).first()
        equipment.Status = '待接单'
        db_session.add_all([data, equipment])
        db_session.commit()
        db_session.close()
        return json.dumps({'code': '10000', 'message': '操作成功'}, cls=AlchemyEncoder, ensure_ascii=False)


@repair.route('/repair_task/<p>', methods=['PATCH'])
def repair_tasks(p):
    """
    更新维修任务表的状态
    :param p: 更改工单状态
    :return:
    """
    if p == 'jiedan':
        json_data = request.values
        data = db_session.query(Repair).filter_by(No=json_data.get('No')).first()
        data.Status = '维修中'
        data.ReceiveWorker = current_user.Name
        data.ReceiveTime = json_data.get('Time')
        equipment = db_session.query(Equipment).filter_by(EquipmentCode=json_data.get('EquipmentCode')).first()
        equipment.Status = '维修中'
        db_session.add_all([data, equipment])
        db_session.commit()
        db_session.close()
        return json.dumps({'code': '10001', 'message': '操作成功'}, cls=AlchemyEncoder, ensure_ascii=False)
    if p == 'over':
        json_data = request.values
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
        return json.dumps({'code': '10001', 'message': '操作成功'}, cls=AlchemyEncoder, ensure_ascii=False)


@repair.route('/record/<p>', methods=['GET', 'POST'])
def repair_record(p):
    """维修记录"""
    # 每页多少条
    limit = int(request.values.get('limit'))
    # 当前页
    offset = int(request.values.get('offset'))
    total = db_session.query(RepairTask).filter_by(EquipmentCode=p).count()
    data = db_session.query(RepairTask).filter(RepairTask.EquipmentCode == p).order_by(
        RepairTask.ApplyTime.desc()).limit(limit).offset((offset - 1) * limit)
    return json.dumps({'code': '10001', 'message': '操作成功', 'data': {'rows': data.all(), 'total': total}},
                      cls=AlchemyEncoder, ensure_ascii=False)


@repair.route('/keep_plan', methods=['POST'])
def keep_plans():
    """保养计划"""
    try:
        json_data = request.get_json()
        # equipments = ['XXF-2', 'XXF-1', 'PYF-1']
        equipments = json_data.get('EquipmentCode')
        if len(equipments) == 1:
            equipment_code = equipments[0]
        else:
            equipment_code = '  '.join(equipments)
        work_time = add_date(json_data.get('WeekTime'), json_data.get('StartTime'))
        work_type = json_data.get('Type')
        week_time = '单次' if work_type == '单次' else json_data.get('WeekTime')
        data = KeepPlan(EquipmentCode=equipment_code, No=get_no(json_data.get('ApplyTime')),
                        Worker=current_user.Name, ApplyTime=json_data.get('ApplyTime'), Type=json_data.get('Type'),
                        StartTime=json_data.get('StartTime'), Describe=json_data.get('Describe'),
                        WorkTime=work_time, WeekTime=week_time)
        db_session.add(data)
        db_session.commit()
        db_session.close()
        return json.dumps({'code': '10001', 'message': '操作成功'}, cls=AlchemyEncoder, ensure_ascii=False)
    except Exception as e:
        logger.error(e)
        insertSyslog("error", "保养计划表添加错误：" + str(e), current_user.Name)
        return json.dumps({'code': '20002', 'message': str(e)}, cls=AlchemyEncoder, ensure_ascii=False)


@repair.route('/keep_task', methods=['GET', 'POST'])
def keep_tasks():
    """保养任务表"""
    try:
        query_data = db_session.query(KeepPlan).filter_by(Status='待保养').all()
        if request.method == 'GET':
            # 每页多少条
            limit = int(request.values.get('limit', '5'))
            # 当前页
            offset = int(request.values.get('offset', '1'))
            for item in query_data:
                q = db_session.query(KeepTask).filter_by(No=item.No).first()
                if not q and get_time_stamp(item.WorkTime):
                    data = KeepTask(EquipmentCode=item.EquipmentCode, No=item.No, Worker=item.Worker, Status=item.Status,
                                    ApplyTime=item.ApplyTime, StartTime=item.StartTime, WorkTime=item.WorkTime,
                                    WeekTime=item.WeekTime, Type=item.Type)
                    db_session.add(data)
                    db_session.commit()
                # if item.Type == '单次':
                #     pass
                    # db_session.delete(item)
                    # db_session.commit()
            data = db_session.query(KeepTask).order_by(KeepTask.ApplyTime.desc()).limit(limit).offset((offset - 1) * limit)
            total = db_session.query(KeepTask).count()
            return json.dumps({'code': '10001', 'message': '操作成功', 'data': {'rows': data.all(), 'total': total}},
                              cls=AlchemyEncoder, ensure_ascii=False)
        if request.method == 'POST':
            json_data = request.values
            no = json_data.get('No')
            end_time = json_data.get('EndTime')
            content = json_data.get('Content')
            item = db_session.query(KeepTask).filter_by(No=no).first()
            data = KeepRecord(EquipmentCode=item.EquipmentCode, No=no, Worker=item.Worker, Status='已完成', Type=item.Type,
                              KeepWorker=current_user.Name, ApplyTime=item.ApplyTime, StartTime=item.StartTime,
                              Describe=item.Describe, Content=content, WeekTime=item.WeekTime, EndTime=end_time)
            db_session.delete(item)
            db_session.commit()
            keep_plan = db_session.query(KeepPlan).filter_by(No=no).first()
            if keep_plan and keep_plan.Type == '周期':
                keep_plan.WorkTime = add_date(keep_plan.WeekTime, keep_plan.WorkTime)
                db_session.add_all([data, keep_plan])
                db_session.commit()
                db_session.close()
                return json.dumps({'code': '10001', 'message': '操作成功'}, cls=AlchemyEncoder, ensure_ascii=False)
            else:
                db_session.delete(keep_plan)
                db_session.add(data)
                db_session.commit()
                db_session.close()
            return json.dumps({'code': '10001', 'message': '操作成功'}, cls=AlchemyEncoder, ensure_ascii=False)
    except Exception as e:
        logger.error(e)
        insertSyslog("error", "保养任务表修改错误：" + str(e), current_user.Name)
        return json.dumps({'code': '20002', 'message': str(e)}, cls=AlchemyEncoder, ensure_ascii=False)


@repair.route('/keep_record/<p>', methods=['GET'])
def keep_record(p):
    """
    查看保养记录
    :param p: 设备号
    :return: 该设备的所有保养记录记录
    """
    try:
        # 当前页码
        page = int(request.values.get('offset'))
        # 每页多少条
        per_page = int(request.values.get('limit'))

        query_data = db_session.query(KeepRecord).order_by(KeepRecord.ApplyTime.desc()).all()
        # data_list = [item for item in query_data]
        result = []
        for data in query_data:
            if p in data.EquipmentCode:
                result.append(data)
        result_data = result[(page - 1)*per_page:page*per_page]
        return json.dumps({'code': '10001', 'message': '操作成功', 'data': {'rows': result_data, 'total': len(result)}},
                          cls=AlchemyEncoder, ensure_ascii=False)
        # total = db_session.query(KeepRecord).filter_by(EquipmentCode=p).count()
        # data = db_session.query(KeepRecord).filter(KeepRecord.EquipmentCode == p).order_by(
        #     KeepRecord.ApplyTime.desc()).limit(per_page).offset((page - 1) * per_page)
        # return json.dumps({'code': '10001', 'message': '操作成功', 'data': {'rows': data.all(), 'total': total}},
        #                   cls=AlchemyEncoder, ensure_ascii=False)
    except Exception as e:
        logger.error(e)
        insertSyslog("error", "保养记录查询错误：" + str(e), current_user.Name)
        return json.dumps({'code': '20002', 'message': str(e)}, cls=AlchemyEncoder, ensure_ascii=False)


@repair.route('/get_keep_plan/<p>', methods=['GET'])
def get_keep_plan(p):
    """
    获取对应设备的保养计划
    :param p: 设备号
    :return: 该设备的所有记录
    """
    query_data = db_session.query(KeepPlan).order_by(KeepPlan.ApplyTime.desc()).all()
    result = []
    for data in query_data:
        if p in data.EquipmentCode:
            result.append(data)
    return json.dumps({'code': '10001', 'message': '操作成功', 'data': result}, cls=AlchemyEncoder, ensure_ascii=False)
