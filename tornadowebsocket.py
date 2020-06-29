# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from datetime import datetime
import os
import json
import redis
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
from dbset.database.db_operate import db_session
from models.core import TagDetail
from dbset.log.BK2TLogger import logger,insertSyslog
from dbset.database import constant
# import objgraph

clients = dict()  # 客户端Session字典
# loop = asyncio.new_event_loop()

# 设置服务器端口
define("port", default=2223, type=int)
# users = set()

class IndexHandler(RequestHandler):
    # @tornado.web.asynchronous
    # @tornado.gen.coroutine
    def get(self):
        self.render("chat-client.html")
def parse_payload(payload):
    payload_len = payload[1] & 127
    if payload_len == 126:
        extend_payload_len = payload[2:4]
        mask = payload[4:8]
        decoded = payload[8:]

    elif payload_len == 127:
        extend_payload_len = payload[2:10]
        mask = payload[10:14]
        decoded = payload[14:]
    else:
        extend_payload_len = None
        mask = payload[2:6]
        decoded = payload[6:]

    # 这里我们使用字节将数据全部收集，再去字符串编码，这样不会导致中文乱码
    bytes_list = bytearray()

    for i in range(len(decoded)):
        # 解码方式
        chunk = decoded[i] ^ mask[i % 4]
        bytes_list.append(chunk)
    body = str(bytes_list, encoding='utf-8')
    return body

def strtofloat(f):
    if f == None or f == "" or f == b'':
        return 0.0
    else:
        return round(float(f), 2)

def _AutoLoadConf():
    dir = {}
    pool = redis.ConnectionPool(host=constant.REDIS_HOST)
    redis_conn = redis.Redis(connection_pool=pool)
    pipe = redis_conn.pipeline(transaction=False)
    Tags = db_session.query(TagDetail).filter(TagDetail.AreaName != None).all()
    key_list = []
    area_list = []
    dis = []
    diw = []
    die = []
    for tag in Tags:
        S = str(tag.TagClassValue)[0:1]
        area_list.append(tag.AreaName)
        if S == "S":
            key_list.append(tag.TagClassValue + "WD")
            key_list.append(tag.TagClassValue + "F")
            key_list.append(tag.TagClassValue + "S")
            pipe.hget("collect_point", tag.TagClassValue + "WD")
            pipe.hget("collect_point", tag.TagClassValue + "F")
            pipe.hget("collect_point", tag.TagClassValue + "S")
        elif S == "W":
            key_list.append(tag.TagClassValue + "F")
            key_list.append(tag.TagClassValue + "S")
            pipe.hget("collect_point", tag.TagClassValue + "F")
            pipe.hget("collect_point", tag.TagClassValue + "S")
        elif S == "E":
            key_list.append(tag.TagClassValue + "_ZGL")
            key_list.append(tag.TagClassValue + "_AU")
            key_list.append(tag.TagClassValue + "_AI")
            key_list.append(tag.TagClassValue + "_BU")
            key_list.append(tag.TagClassValue + "_BI")
            key_list.append(tag.TagClassValue + "_CU")
            key_list.append(tag.TagClassValue + "_CI")
            pipe.hget("collect_point", tag.TagClassValue + "_ZGL")
            pipe.hget("collect_point", tag.TagClassValue + "_AU")
            pipe.hget("collect_point", tag.TagClassValue + "_AI")
            pipe.hget("collect_point", tag.TagClassValue + "_BU")
            pipe.hget("collect_point", tag.TagClassValue + "_BI")
            pipe.hget("collect_point", tag.TagClassValue + "_CU")
            pipe.hget("collect_point", tag.TagClassValue + "_CI")
    result = pipe.execute()
    for i in range(0, len(result)):
        dir[key_list[i]] = strtofloat(result[i])
    return dir

class SendThread(threading.Thread):

    # 启动单独的线程运行此函数，每隔1秒向所有的客户端推送当前时间

    def run(self):
        try:
            # tornado 5 中引入asyncio.set_event_loop,不然会报错
            # count = 0
            asyncio.set_event_loop(asyncio.new_event_loop())
            # asyncio.set_event_loop(loop)
            # conn = redis.Redis(host='127.0.0.1', port=6379, db=0)
            re = _AutoLoadConf()
            while True:
                ti = str(datetime.datetime.now())
                aa = "asd"
                if aa == "":
                    re = _AutoLoadConf()
                for key in clients.keys():
                    print(clients[key])
                    clients[key]["object"].write_message(json.dumps(re))
                    print("write to client %s:%s" % (key, re))
                # count = count + 1
                time.sleep(2)
                gc.collect()
                # print(sys.getsizeof(clients))
                # objgraph.show_most_common_types(limit=10)
                # objgraph.show_growth()
                # print("程序执行次数：" + str(count))
        except Exception as e:
            logger.error(e)
            insertSyslog("error", "查询实时数据报错Error：" + str(e), "")
        finally:
            pass


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


if __name__ == '__main__':
    # tornado.options.parse_command_line()

    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/chat", ChatHandler),
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
