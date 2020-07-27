import redis
import json
from dbset.database import constant
from models.schedul_model import TagMaintain
from tools.MESLogger import MESLogger
logger = MESLogger('../logs', 'log')
from dbset.database.db_operate import db_session
import ast
from datetime import datetime
import os
import tornado
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler
from tornado.options import define, options, parse_command_line
from tornado.ioloop import IOLoop
import asyncio
import threading
import time
import gc
import datetime

# pool = redis.ConnectionPool(host=constant.REDIS_HOST) #, password=constant.REDIS_PASSWORD,decode_responses=True
pool = redis.ConnectionPool(host=constant.REDIS_HOST)
redis_conn = redis.Redis(connection_pool=pool)

clients = dict()  # 客户端Session字典
# loop = asyncio.new_event_loop()

# 设置服务器端口
define("port", default=5002, type=int)
# users = set()

class IndexHandler(RequestHandler):
    # @tornado.web.asynchronous
    # @tornado.gen.coroutine
    def get(self):
        self.render("chat-client.html")

class SendThread(threading.Thread):

    # 启动单独的线程运行此函数，每隔1秒向所有的客户端推送当前时间

    def run(self):
        runcount = 0
        failcount = 0
        asyncio.set_event_loop(asyncio.new_event_loop())
        msg = ''
        # asyncio.set_event_loop(loop)
        while True:

            try:
                # oclass = ast.literal_eval(returnb(redis_conn.hget(constant.REDIS_TABLENAME, "tags_list")))
                oclass = redis_conn.hgetall(constant.REDIS_TABLENAME)
                oc_dict_i_tag = {}
                for oc in oclass:
                    oc_dict_i_tag[returnb(oc)] = returnb(oclass.get(oc))
                json_data = json.dumps(oc_dict_i_tag)
                bytemsg = bytes(json_data,encoding="utf-8")
                for key in clients.keys():
                    clients[key]["object"].write_message(bytemsg)
                runcount = runcount + 1
                time.sleep(2)
            except Exception as e:
                print(e)
                failcount = failcount + 1
                break
            finally:
                pass
            redis_conn.hset(constant.REDIS_TABLENAME, "websocket_end",
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            redis_conn.hset(constant.REDIS_TABLENAME, "websocket_runcount", str(runcount))
            redis_conn.hset(constant.REDIS_TABLENAME, "websocket_failcount", str(failcount))
            redis_conn.hset(constant.REDIS_TABLENAME, "websocket_status", "执行成功")


class ChatHandler(WebSocketHandler):
    # users = set()  # 用来存放在线用户的容器
    # clients = dict()

    def open(self):
        # 建立连接后添加用户到容器中

        # # 向已在线用户发送消息
        # for user in self.users:
        #     remote_ip, port = self.request.connection.context.address
        #     now = datetime.now().strftime("%H:%M:%S")
        #     user.write_message("[{}][{}:{}]-进入聊天室".format(now, remote_ip, port))
        remote_ip, port = self.request.connection.context.address
        self.id = remote_ip + ":" + str(port)

        # self.stream.set_nodelay(True)
        # self.set_nodelay(True)

        clients[self.id] = {"id": self.id, "object": self}  # 保存Session到clients字典中

    def on_message(self, message):
        # 向在线用户广播消息
        # now = datetime.now().strftime("%H:%M:%S")
        # remote_ip, port = self.request.connection.context.address
        # t = random.randint(1, 100)
        # for user in users:
        #     # user.write_message("[{}][{}:{}] {}".format(now, remote_ip, port, t))
        #     user.write_message("[{}][{}:{}] {}".format(now, remote_ip, port, t))
        print("Client %s received a message:%s" % (self.id, message))

    def on_close(self):
        # 用户关闭连接后从容器中移除用户
        # now = datetime.now().strftime("%H:%M:%S")
        remote_ip, port = self.request.connection.context.address
        # self.users.remove(self)
        # for user in self.users:
        #     user.write_message("[{}][{}:{}]-离开聊天室".format(now, remote_ip, port))
        if self.id in clients:
            print(clients[self.id])
            del clients[self.id]
        gc.collect()

            # print("Client %s is closed" % (self.id))

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求

def strtofloat(f):
    try:
        if f == None or f == "" or f == b'':
            return 0.0
        else:
            return round(float(f), 2)
    except Exception as e:
        print(e)
def returnb(rod):
    if rod == None or rod == "" or rod == b'':
        return rod
    else:
        return rod.decode()


if __name__ == "__main__":
    # tornado.options.parse_command_line()
    # 将所有的tag写入redis
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/socket", ChatHandler),
    ],
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        # debug=True
    )

    # http_server = tornado.httpserver.HTTPServer(app)
    # http_server.listen(options.port)
    # tornado.ioloop.IOLoop.current().start()

    # http_server = tornado.httpserver.HTTPServer(app)
    SendThread().start()

    parse_command_line()

    app.listen(options.port)
    # 挂起运行
    tornado.ioloop.IOLoop.instance().start()
    # tornado.ioloop.IOLoop.current().start()
