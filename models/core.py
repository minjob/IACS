# /******************************************************************************************
# ************* STK make model usage:
# ************* version: print python3.6.3  version
# ************* make: make Python file
# ************* STK makemodel.py 1.0.0
# ************* @author Xujin
# ************* @date 2019-08-09 15:58:36
# ************* @Model 
# ******************************************************************************************/

# 引入必要的类库
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Column, ForeignKey, Table, DateTime, Integer, String
from sqlalchemy import Column, DateTime, Float, Integer, String, Unicode, BigInteger
from datetime import datetime
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

# 引入mssql数据库引擎
import pymssql

# 创建对象的基类
from dbset.database.db_operate import DB_URL

engine = create_engine(DB_URL)
SessionFactory = sessionmaker(bind=engine)
session = SessionFactory()
Base = declarative_base(engine)

# Role_Menu_START:
# 菜单与角色关联表
Role_Menu = Table(
    "role_menu",
    Base.metadata,
    Column("Role_ID", Integer, ForeignKey("Role.ID"), nullable=False, primary_key=True),
    Column("Menu_ID", Integer, ForeignKey("Menu.ID"), nullable=False, primary_key=True)
)

# Role_Menu_END:


# DepartmentManager_START:
class DepartmentManager(Base):
    '''部门'''
    __tablename__ = "DepartmentManager"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 部门名称:
    DepartName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 部门编码:
    DepartCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 所属厂区:
    DepartLoad = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# DepartmentManager_END:

# MenuType_START:
class MenuType(Base):
    __tablename__ = "MenuType"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 类型名称:
    TypeName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 类型编码:
    TypeCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# MenuType_END:

# Role_START:
class Role(Base):
    '''角色'''
    __tablename__ = "Role"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 角色编码:
    RoleCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # RoleName:
    RoleName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # Description:
    Description = Column(Unicode(50), primary_key=False, autoincrement=False, nullable=True)

    # 所属部门:
    ParentNode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 查询权限
    menus = relationship("Menu", secondary=Role_Menu)


# Role_END:

# Menu_START:
# 模块菜单表
class Menu(Base):
    __tablename__ = 'Menu'
    # 模块ID
    ID = Column(Integer, primary_key=True, autoincrement=True)

    # 模块名称
    ModuleName = Column(Unicode(32), nullable=False)

    # 模块编码
    ModuleCode = Column(String(100),nullable=False)

    # 模块路由
    Url = Column(String(100), nullable=True)

    # 描述
    Description = Column(Unicode(1024), nullable=True)

    # 创建时间
    CreateDate = Column(DateTime, default=datetime.now, nullable=True)

    # 创建人
    Creator = Column(Unicode(50), nullable=True)

    # 父节点
    ParentNode = Column(Integer, nullable=True)

    # 查询角色
    roles = relationship("Role", secondary=Role_Menu)

# Menu_END:



# plantCalendarScheduling_START:
class plantCalendarScheduling(Base):
    '''日历'''
    __tablename__ = "plantCalendarScheduling"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 颜色:
    color = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 标题:
    title = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 时间:
    start = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 结束:
    end = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# plantCalendarScheduling_END:


# Enterprise_START:
class Enterprise(Base):
    __tablename__ = "Enterprise"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 上级企业:
    ParentNode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 企业类型:
    Type = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 描述:
    Desc = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 父节点名称:
    ParentNodeName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 企业代码:
    EnterpriseNo = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 企业名称:
    EnterpriseName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 企业编码:
    EnterpriseCode = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)


# Enterprise_END:


# Factory_START:
class Factory(Base):
    __tablename__ = "Factory"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 所属企业:
    EnterpriseName = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 厂名:
    FactoryName = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 所在地区:
    Region = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)


# Factory_END:


# Station_START:
class Station(Base):
    '''岗位'''
    __tablename__ = "Station"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 地址:
    Address = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 电话:
    Phone = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 岗位负责人:
    PersonCharge = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 岗位职责:
    Responsibility = Column(Unicode(100), primary_key=False, autoincrement=False, nullable=True)

    # 所属部门:
    DepartName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 岗位类型:
    StationType = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 岗位名称:
    StationName = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 岗位编码:
    StationCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# Station_END:


# RedisKey_START:
class RedisKey(Base):
    __tablename__ = "RedisKey"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 对应的键值:
    KEY = Column(Unicode(52), primary_key=False, autoincrement=False, nullable=True)

    # 描述:
    Description = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)


# RedisKey_END:


# AreaMaintain_START:
class AreaMaintain(Base):
    '''厂区'''
    __tablename__ = "AreaMaintain"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 区域编码:
    AreaCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 区域名称:
    AreaName = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 所属厂区:
    FactoryName = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)


# AreaMaintain_END:


# LimitTable_START:
class LimitTable(Base):
    __tablename__ = "LimitTable"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 名称:
    LimitName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 编码:
    LimitCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 限值:
    LimitValue = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# LimitTable_END:


# Unit_START:
class Unit(Base):
    __tablename__ = "Unit"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 单位名称:
    UnitName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 单位值:
    UnitValue = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# Unit_END:


# BrandAreaTable_START:
class BrandAreaTable(Base):
    __tablename__ = "BrandAreaTable"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 区域:
    AreaName = Column(Unicode(52), primary_key=False, autoincrement=False, nullable=True)

    # 品名:
    BrandName = Column(Unicode(52), primary_key=False, autoincrement=False, nullable=True)


# BrandAreaTable_END:


# BatchMaintain_START:
class BatchMaintain(Base):
    '''
    计划表
    '''
    __tablename__ = "BatchMaintain"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 计划单号:
    PlanNum = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 批次号:
    BatchID = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 品名:
    BrandName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 计划重量:
    PlanQuantity = Column(Unicode(52), primary_key=False, autoincrement=False, nullable=True)

    # 水用量:
    WaterConsumption = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 汽用量:
    SteamConsumption = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 创建日期:
    CreateDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 生产日期:
    ProductionDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 开始时间:
    StartTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 结束时间:
    EndTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 生产车间:
    AreaName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# BatchMaintain_END:


# WorkShop_START:
class WorkShop(Base):
    '''车间'''
    __tablename__ = "WorkShop"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 车间名称:
    WorkShopName = Column(Unicode(52), primary_key=False, autoincrement=False, nullable=True)

    # 车间编码:
    WorkShopCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 所属厂区:
    FactoryName = Column(Unicode(52), primary_key=False, autoincrement=False, nullable=True)

    # 描述:
    Desc = Column(Unicode(100), primary_key=False, autoincrement=False, nullable=True)


# WorkShop_END:


# Instrumentation_START:
class Instrumentation(Base):
    __tablename__ = "Instrumentation"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 仪表编码:
    InstrumentationCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 仪表名称:
    InstrumentationName = Column(Unicode(52), primary_key=False, autoincrement=False, nullable=True)

    # 检定周期:
    VerificationCycle = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 检定次数:
    NumberVerification = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 提醒时间:
    ReminderTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 状态:
    Status = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 录入时间:
    CreateTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 处理人:
    Handler = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 处理状态:
    HandleStatus = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 审核人:
    Reviewer = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 审核状态:
    ReviewStatus = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 更新时间:
    UpdateTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# Instrumentation_END:



# 生成表单的执行语句_START
Base.metadata.create_all(engine)

# 生成表单的执行语句_END
