from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, ForeignKey, Table, Column, DateTime, Integer, String, Unicode, Float
from sqlalchemy.dialects.mssql.base import BIT
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import LoginManager

from dbset.database.db_operate import DB_URL

login_manager = LoginManager()
# 创建对象的基类
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
db_session = Session()
Base = declarative_base(engine)


class SysLog(Base):
    __tablename__ = "SysLog"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=True)

    # IP:
    IP = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 计算机名称:
    ComputerName = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 操作用户:
    UserName = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 操作日期:
    OperationDate = Column(DateTime, primary_key=False, autoincrement=False, nullable=True)

    # 操作内容:
    OperationContent = Column(Unicode(2048), primary_key=False, autoincrement=False, nullable=True)

    # 类型:
    OperationType = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)


# Organization:
class Organization(Base):
    __tablename__ = "Organization"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 组织结构编码:
    OrganizationCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 父组织机构:
    ParentNode = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 顺序号:
    OrganizationSeq = Column(Unicode(10), primary_key=False, autoincrement=False, nullable=True)

    # 组织机构名称:
    OrganizationName = Column(Unicode(100), primary_key=False, autoincrement=False, nullable=True)

    # 说明:
    Description = Column(Unicode(100), primary_key=False, autoincrement=False, nullable=True)

    # 创建人:
    CreatePerson = Column(Unicode(20), primary_key=False, autoincrement=False, nullable=True)

    # 创建时间:
    CreateDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 显示图标:
    Img = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True, default="antonio.jpg")

    # 显示图标:
    Color = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True, default="#1696d3")


# 电子批记录
class ElectronicBatch(Base):
    __tablename__ = 'ElectronicBatch'
    # id:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # id:
    TaskID = Column(Integer, primary_key=False, autoincrement=True, nullable=False)

    # 批次号:
    BatchID = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 工艺段编码:
    PDUnitRouteID = Column(Integer, nullable=False, primary_key=False)

    # 设备编码
    EQPID = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 类型:
    OpcTagID = Column(Unicode(100), primary_key=False, autoincrement=False, nullable=True)

    # 类型:
    BrandID = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 类型:
    BrandName = Column(Unicode(100), primary_key=False, autoincrement=False, nullable=True)

    # 采样值:
    SampleValue = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 采样时间:
    SampleDate = Column(DateTime, primary_key=False, autoincrement=False, nullable=True)

    # 重复次数：
    RepeatCount = Column(Integer, primary_key=False, autoincrement=False, nullable=True, default=0)

    # 描述:
    Description = Column(Unicode(200), primary_key=False, autoincrement=False, nullable=True)

    # 描述:
    Type = Column(Unicode(200), primary_key=False, autoincrement=False, nullable=True)

    # 单位:
    Unit = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# 审计追踪
class AuditTrace(Base):
    __tablename__ = 'AuditTrace'
    # id:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 操作:
    Operation = Column(Unicode(300), primary_key=False, autoincrement=False, nullable=True)

    # 详细信息:
    DeitalMSG = Column(Unicode(800), primary_key=False, autoincrement=False, nullable=True)

    # 修改日期
    ReviseDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 操作表:
    TableName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 用户:
    User = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 其他:
    Other = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# 流程确认表
class FlowConfirm(Base):
    __tablename__ = 'FlowConfirm'
    # id:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 批次:
    BatchNum = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 确认流程:
    ConfirmFlow = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 确认人:
    Confirmer = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 确认时间:
    ConfirmTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 修改时间:
    UpdateTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # key:
    key = Column(Unicode(100), primary_key=False, autoincrement=False, nullable=True)


# 数据库建表配置
class CreateTableSet(Base):
    __tablename__ = 'CreateTableSet'
    # id:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 表名:
    TableName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 表的描述:
    TableDescrip = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # # 表类型（分页表/下拉框数据表）:
    # TableType = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 是否在第一列显示多选框（checkbox）:
    ISFirstCheckBox = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 是否实现单选，设为true则复选框只能选择一行:
    SingleSelect = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 是否显示添加按钮:
    IsAdd = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 是否显示修改按钮:
    IsUpdate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 是否显示删除按钮:
    IsDelete = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # ID字段:
    TableID = Column(Unicode(32), default="ID", primary_key=False, autoincrement=False, nullable=True)


# 4.表字段配置：选择一个表，将此表的数据（字段）显示出来（新表只有ID）
# 字段表表头
class FieldSet(Base):
    __tablename__ = 'FieldSet'
    # id:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 表名称:
    TableName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # title字段名称（名字）:
    TitleName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # field字段名（name）:
    FieldName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # isedit是否做添加修改操作（默认否）:
    Isedit = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # edittype输入类型，输入框/下拉框/时间选择框（满足上一条可做编辑操作，默认输入框）:
    Edittype = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # downtable下拉框的数据表（满足上一条选择下拉框，选择一个表）:
    Downtable = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # sortable该列是否排序,表头显示双箭头(默认false):
    Sortable = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # order该列排序方式，满足上条可排序，默认asc( asc/desc):
    Order = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # visible该列是否可见(默认true):
    Visible = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # VARCHAR长度:
    length = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 字段类型:
    type = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 字段注释:
    comment = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 是否为主键（默认False）:
    primarykey = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 是否自增（默认False）:
    autoincrement = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 是否为空（默认True）:
    nullable = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 列宽:
    width = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# 是否
class ISFlag(Base):
    __tablename__ = 'ISFlag'
    # id:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 标识:
    Flag = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 描述:
    Description = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# 是否
class InputTypeTable(Base):
    __tablename__ = 'InputTypeTable'
    # id:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 类型:
    Type = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 名称:
    Title = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# 表字段类型
class FieldType(Base):
    __tablename__ = 'FieldType'
    # id:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 类型:
    Type = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 描述:
    Description = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# 用户班组表
class UserShiftsGroup(Base):
    __tablename__ = 'UserShiftsGroup'
    # ID
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 用户ID:
    UserID = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 用户名:
    Name = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 班组ID:
    ShiftsGroupID = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 班组名称
    ShiftsGroupName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 创建时间
    CreateDate = Column(DateTime, primary_key=False, autoincrement=False, nullable=True,
                        default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


# 权限表
class Permission(Base):
    __tablename__ = 'Permission'
    # ID
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 权限名字:
    PermissionName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 权限类型:
    PermissionType = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 描述:
    Description = Column(Unicode(100), primary_key=False, autoincrement=False, nullable=True)

    # 创建时间
    CreateData = Column(DateTime, primary_key=False, autoincrement=False, nullable=True,
                        default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


# 角色默认权限表
class RolePermission(Base):
    __tablename__ = 'RolePermission'
    # ID
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 角色ID:
    RoleID = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 角色名称:
    RoleName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 权限ID:
    PermissionID = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 权限名字:
    PermissionName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 创建时间
    CreateDate = Column(DateTime, primary_key=False, autoincrement=False, nullable=True,
                        default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


# 角色用户表
class RoleUser(Base):
    __tablename__ = 'RoleUser'
    # ID
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 权限ID:
    UserID = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 权限名字:
    UserName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 角色ID:
    RoleID = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 角色名称:
    RoleName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 创建时间
    CreateDate = Column(DateTime, primary_key=False, autoincrement=False, nullable=True,
                        default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


# User_START:
class User(Base):
    __tablename__ = "User"

    # id:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 用户名:
    Name = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 密码:
    Password = Column(Unicode(150), primary_key=False, autoincrement=False, nullable=True)

    # 工号:
    WorkNumber = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 所属岗位:
    StationName = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 登录状态:
    Status = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # session_id:
    session_id = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 所属部门:
    OrganizationName = Column(Unicode(50), primary_key=False, autoincrement=False, nullable=True)

    # 所属厂区:
    FactoryName = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 班组类型
    ShiftsGroupType = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 上次登录时间:
    LastLoginTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 创建时间:
    CreateTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 创建用户:
    Creater = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 是否锁定:
    IsLock = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # @property
    # def password(self):
    #     raise AttributeError('password is not a readable attribute')

    # 定义password字段的写方法，我们调用generate_password_hash将明文密码password转成密文Shadow
    # @password.setter
    def password(self, password):
        self.Password = generate_password_hash(password)
        return self.Password

    # 定义验证密码的函数confirm_password
    def confirm_password(self, password):
        return check_password_hash(self.Password, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.ID)  # python 3


# User_END:

# 服务运行情况表
class SystemRunDetail(Base):
    __tablename__ = 'SystemRunDetail'
    # ID
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 总执行次数:
    RunTotalNum = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 开始执行时间:
    RunStartTime = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 最后刷新时间:
    RunRefreshTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 执行状态:
    RunStatus = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 执行成功数:
    RunSuccessNum = Column(Unicode(150), primary_key=False, autoincrement=False, nullable=True)

    # 执行失败数:
    RunFailNum = Column(Unicode(150), primary_key=False, autoincrement=False, nullable=True)


# BatchMaintain_START:
class BatchMaintainTask(Base):
    '''
    任务表
    '''
    __tablename__ = "BatchMaintainTask"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 工艺段:
    PuidName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 计划单号:
    PlanNum = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 批次号:
    BatchID = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 品名:
    BrandName = Column(Unicode(52), primary_key=False, autoincrement=False, nullable=True)

    # 计划重量:
    PlanQuantity = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

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


class BrandMaintain(Base):
    '''品名维护表'''
    __tablename__ = "BrandMaintain"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=True)

    # 产品名称:
    BrandName = Column(Unicode(64), nullable=False, primary_key=False)

    # 产品编码:
    BrandCode = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 创建日期:
    CreateDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


class PUIDMaintain(Base):
    '''工艺维护表'''
    __tablename__ = "PUIDMaintain"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=True)

    # 工艺名称:
    PUIDName = Column(Unicode(64), nullable=False, primary_key=False)

    # 工艺编码:
    PUIDCode = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 产品名称:
    BrandName = Column(Unicode(64), nullable=False, primary_key=False)

    # 产品编码:
    BrandCode = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 创建日期:
    CreateDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# 班时
class Shifts(Base):
    __tablename__ = "Shifts"
    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    # 班次编码
    ShiftsCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)
    # 班次名称
    ShiftsName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)
    # 班次开始时间
    BeginTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)
    # 班次结束时间
    EndTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# 班制
class ShiftsClass(Base):
    __tablename__ = "ShiftsClass"
    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    # 班制编码
    ShiftsClassCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)
    # 班制名称
    ShiftsClassName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)
    # 排班序号
    ShiftsClassNum = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)
    # 班制开始时间
    BeginTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)
    # 班制结束时间
    EndTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

# 班组
class ShiftsGroup(Base):
    __tablename__ = "ShiftsGroup"
    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    # 班组编码
    ShiftsGroupCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)
    # 班组名称
    ShiftsGroupName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)
    # 班组类型
    ShiftsGroupType = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)
    # 描述:
    Description = Column(Unicode(100), primary_key=False, autoincrement=False, nullable=True)
    # 创建日期:
    CreateDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# 模块菜单表
class ModulMenus(Base):
    __tablename__ = 'ModulMenus'
    # 模块ID
    ID = Column(Integer, primary_key=True, autoincrement=True)

    # 模块菜单名字:
    ModulMenuName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 模块菜单编码:
    ModulMenuCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 菜单路由:
    ModulMenuRoute = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 创建时间
    CreateDate = Column(Unicode(32), default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), nullable=True)

    # 父节点
    ParentNode = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 菜单类型:
    MenuType = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 菜单图标:
    MenuLogo = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 菜单创建人:
    Creator = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# 电价格维护表:
class ElectricPrice(Base):
    __tablename__ = "ElectricPrice"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 价格名称:
    PriceName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 价格值:
    PriceValue = Column(Float(53), primary_key=False, autoincrement=False, nullable=True)

    # 价格类型:
    PriceType = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True, default="电")

    # 开始时间:
    StartTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 结束时间:
    EndTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 是否启用:
    IsEnabled = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 描述:
    Description = Column(Unicode(100), primary_key=False, autoincrement=False, nullable=True)

    # 单位:
    Unit = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


class Equipment(Base):
    __tablename__ = "Equipment"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=True)

    # 设备编码:
    EquipmentCode = Column(Unicode(30), primary_key=False, autoincrement=False, nullable=True)

    # 功率:
    Power = Column(Unicode(50), primary_key=False, autoincrement=False, nullable=True)

    # 数量:
    Quantity = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 注释:
    Comment = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 设备状态（运行中，维修中）
    Status = Column(Unicode(32), default="运行中", nullable=True)
    # 设备名称
    # Name = Column(Unicode(32), nullable=True)
    # 设备型号
    # Model = Column(Unicode(128), nullable=True)
    # 生产商
    Manufacturer = Column(Unicode(32), nullable=True)
    # SAP号
    Sap = Column(Unicode(64), nullable=True)
    # 固定资产编号
    FixedAssetsNo = Column(Unicode(128), nullable=True)
    # 固定资产名称s
    FixedAssetsName = Column(Unicode(32), nullable=True)
    # 区域
    Area = Column(Unicode(32), nullable=True)
    # 进厂日期
    IntoTime = Column(Unicode(32), nullable=True, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class Plan(Base):
    __tablename__ = 'Plan'

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    # 设备编码:
    EquipmentCode = Column(Unicode(30), nullable=True)
    # 班组
    WorkNo = Column(Unicode(32), nullable=False)
    # 工单类型(维修，保养)
    Type = Column(Unicode(32), nullable=True)
    # 计划状态（良好,异常）
    Status = Column(Unicode(32), default="待处理")
    # 提醒状态（待提醒，已提醒）
    RemindStatus = Column(Unicode(32), default="待提醒", nullable=True)
    # 预工作时间
    WorkTime = Column(Unicode(32), nullable=True, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class Record(Base):
    __tablename__ = 'Record'

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    # 设备编码:
    EquipmentCode = Column(Unicode(30), primary_key=False, autoincrement=False, nullable=True)
    # 确认人
    Name = Column(Unicode(32), nullable=True)
    # 设备状态（良好,异常）
    Status = Column(Unicode(32), default="良好")
    # 班组
    WorkNo = Column(Unicode(32), nullable=False)
    # 工单类型(维修，保养)
    Type = Column(Unicode(32), nullable=True)
    # 工作时间
    WorkTime = Column(Unicode(32), nullable=True, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class Repair(Base):
    """维修申请表"""
    __tablename__ = 'repair'

    id = Column(Integer, autoincrement=True, primary_key=True)
    # 工单号
    No = Column(Unicode(128), nullable=True, default=datetime.now().strftime('%Y%m%d%H%M%S'))
    # 设备编码
    EquipmentCode = Column(Unicode(128), nullable=True)
    # 设备名称
    Name = Column(Unicode(32), nullable=True)
    # 申请人
    Worker = Column(Unicode(32), nullable=True)
    # 故障阐述
    FaultExpound = Column(Unicode(128), nullable=True)
    # 工单状态（待接单，已接单）
    Status = Column(Unicode(32), default="待接单")
    # 申请时间
    ApplyTime = Column(Unicode(32), nullable=True, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # 接单人
    ReceiveWorker = Column(Unicode(32), nullable=True)
    # 接单时间
    ReceiveTime = Column(Unicode(32), nullable=True, default='尚未接单')


class RepairTask(Base):
    __tablename__ = 'repairtask'
    """维修任务表"""
    id = Column(Integer, autoincrement=True, primary_key=True)
    # 工单号
    No = Column(Unicode(128), nullable=True)
    # 设备编码
    EquipmentCode = Column(Unicode(128), nullable=True)
    # 设备名称
    Name = Column(Unicode(32), nullable=True)
    # 申请人
    Worker = Column(Unicode(32), nullable=True)
    # 维修人
    ReceiveWorker = Column(Unicode(32), nullable=True)
    # 工单状态（维修完成）
    Status = Column(Unicode(32), default="维修完成")
    # 维修内容
    Content = Column(Unicode(128), nullable=True)
    # 申请时间
    ApplyTime = Column(Unicode(32), nullable=True)
    # 接单时间
    ReceiveTime = Column(Unicode(32), nullable=True)
    # 完成时间
    EndTime = Column(Unicode(32), nullable=True)


class CollectionPoint(Base):
    __tablename__ = "CollectionPoint"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 采集点名称:
    CollectionPointName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集点编码:
    CollectionPointCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集位置:
    CollectionPosition = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 厂区:
    FactoryName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 车间:
    Workshop = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 位置描述:
    PositionDescription = Column(Unicode(100), primary_key=False, autoincrement=False, nullable=True)


# 生成表单的执行语句
Base.metadata.create_all(engine)
