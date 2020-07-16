from flask import Flask, abort, request, render_template
from flask_restful import reqparse, abort, Api, Resource
from flask_login import login_required
from dbset.account import auth_lib
from handlers.ERP_Scheduling.ERP_Schedul import erp_schedul
from handlers.SystemManagement.ai_repair import repair
from handlers.SystemManagement.calendar import cale
from handlers.SystemManagement.monitor import opc
from handlers.account import account_auth
from handlers.SystemManagement import user_management, PermissionAssignment, Role_management
from handlers.account.user_role import user_manager
from handlers.energy_manager.energy_manager import energy
from handlers.main import system_manage
from handlers.SystemManagement.organization_model import organiza
from handlers.SystemManagement.systemlog import systemlog
from flask_bootstrap import Bootstrap
from tools.common import insert, delete, update, select, accurateSelect
from flask_login import current_user
import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'qeqhdasdqiqd131'
account_auth.login_manager.init_app(app)

# 将后台函数传到前端
app.add_template_global(auth_lib.isIn, 'isIn')

# 登录
app.register_blueprint(account_auth.login_auth)
# 用户管理
app.register_blueprint(user_management.user_manage)
# 角色管理
app.register_blueprint(Role_management.role_management)
# 主页
app.register_blueprint(system_manage.system_set)
# 权限分配
app.register_blueprint(PermissionAssignment.permission_distribution)
# 组织机构
app.register_blueprint(organiza)
# # 设备管理
# app.register_blueprint(equip)
# 过程连续数据
# app.register_blueprint(ProcessContinuousData.continuous_data)
# 日志模块
app.register_blueprint(systemlog)
# 日历管理
app.register_blueprint(cale)
# 组织架构
app.register_blueprint(user_manager)
# 计划排产
app.register_blueprint(erp_schedul)
# 维保
app.register_blueprint(repair)
# 机组开关
app.register_blueprint(opc)
# 能耗管理
app.register_blueprint(energy)


@app.route('/')
@login_required
def index():
    return render_template("./main/index.html")


@app.route('/home')
@login_required
def home():
    return render_template("./main/home.html")

api = Api(app)

class CUIDList(Resource):
    def get(self):
        data = request.values
        searchModes = data.get("searchModes")
        if searchModes == "精确查询":
            return accurateSelect(request.values)
        else:  # 模糊查询
            return select(request.values)

    def post(self):
        return insert(request.values)

    def put(self):
        return update(request.values)

    def delete(self):
        return delete(request.values)


api.add_resource(CUIDList, '/CUID')

if __name__ == '__main__':
    from livereload import Server

    server = Server(app.wsgi_app)
    server.watch('**/*.*')
    server.serve()
    # app.run()
