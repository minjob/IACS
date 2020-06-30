from flask import Flask, abort, request, render_template
from flask_restful import reqparse, abort, Api, Resource
from flask_login import login_required
from dbset.account import auth_lib
from handlers.ERP_Scheduling.ERP_Schedul import erp_schedul
from handlers.SystemManagement.calendar import cale
from handlers.account import account_auth
from handlers.SystemManagement import user_management, PermissionAssignment, Role_management
from handlers.account.user_role import user_manager
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


@app.route('/')
@login_required
def index():
    return render_template("./main/index.html")


@app.route('/home')
@login_required
def home():
    return render_template("./main/home.html")


@app.route('/config')
@login_required
def config():
    if current_user.WorkNumber == "201900":
        return render_template("./main/config.html")
    else:
        return "没有此权限！"


api = Api(app)

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '哈哈哈'},
    'todo3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201


api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')

# ----------------------------------------------------------------------------------------------------------------------%%%%%%%%%%%

CUIDS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '哈哈哈'},
    'todo3': {'task': 'profit!'},
}
parser = reqparse.RequestParser()
parser.add_argument('task')


class CUID(Resource):
    def get(self, cuid_id):
        abort_if_todo_doesnt_exist(cuid_id)
        return CUIDS[cuid_id]

    def delete(self, cuid_id):
        abort_if_todo_doesnt_exist(cuid_id)
        del CUIDS[cuid_id]
        return '', 204

    def put(self, cuid_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        CUIDS[cuid_id] = task
        return task, 201


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
api.add_resource(CUID, '/CUID/<cuid_id>')


if __name__ == '__main__':
    from livereload import Server

    server = Server(app.wsgi_app)
    server.watch('**/*.*')
    server.serve()
    # app.run()
