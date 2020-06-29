import redis
import json
from dbset.database import constant
import time
from tools.MESLogger import MESLogger
logger = MESLogger('../logs', 'log')
import socket
import struct
import hashlib
import base64
import threading
import datetime
from dbset.database.db_operate import db_session
from models.core import TagDetail, AreaTable
import ast

pool = redis.ConnectionPool(host=constant.REDIS_HOST)
redis_conn = redis.Redis(connection_pool=pool)

def get_headers(data):
    headers = {}
    data = str(data, encoding="utf-8")

    header, body = data.split("\r\n\r\n", 1)

    header_list = header.split("\r\n")

    for i in header_list:
        i_list = i.split(":", 1)
        if len(i_list) >= 2:
            headers[i_list[0]] = "".join(i_list[1::]).strip()
        else:
            i_list = i.split(" ", 1)
            if i_list and len(i_list) == 2:
                headers["method"] = i_list[0]
                headers["protocol"] = i_list[1]
    return headers


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


def send_msg(conn, msg_bytes):
    # 接收的第一字节，一般都是x81不变
    first_byte = b"\x81"
    length = len(msg_bytes)
    if length < 126:
        first_byte += struct.pack("B", length)
    elif length <= 0xFFFF:
        first_byte += struct.pack("!BH", 126, length)
    else:
        first_byte += struct.pack("!BQ", 127, length)

    msg = first_byte + msg_bytes
    conn.sendall(msg)
    return True

sock_pool = []


def handler_accept(sock):

    while True:
        conn, addr = sock.accept()

        data = conn.recv(8096)
        headers = get_headers(data)
        # 对请求头中的sec-websocket-key进行加密
        response_tpl = "HTTP/1.1 101 Switching Protocols\r\n" \
                       "Upgrade:websocket\r\n" \
                       "Connection: Upgrade\r\n" \
                       "Sec-WebSocket-Accept: %s\r\n" \
                       "WebSocket-Location: ws://%s\r\n\r\n"

        # 第一次连接发回报文
        magic_string = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        if headers.get('Sec-WebSocket-Key'):
            value = headers['Sec-WebSocket-Key'] + magic_string

        ac = base64.b64encode(hashlib.sha1(value.encode('utf-8')).digest())
        response_str = response_tpl % (ac.decode('utf-8'), headers.get("Host"))
        conn.sendall(bytes(response_str, encoding="utf-8"))
        t = threading.Thread(target=handler_msg, args=(conn, ))
        t.start()


def handler_msg(conn):
    with conn as c:
        data_recv = c.recv(1024)
        runcount = 0
        failcount = 0
        while True:
            try:
                TagClassValue = ""
                time.sleep(2)
                if data_recv[0:1] == b"\x81":
                    data_parse = parse_payload(data_recv)
                    TagClassValue = str(data_parse)
                area_list = []
                oclass = ast.literal_eval(returnb(redis_conn.hget(constant.REDIS_TABLENAME, "all_steam_tags")))
                oc_dict_i_tag = {}
                for oc in oclass:
                    oc_dict_i = {}
                    oc_dict_i["flowValue"] = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc + "F"))  # 蒸汽瞬时流量
                    sumvalue = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc + "S"))  # 蒸汽累计流量
                    if oc == 'S_Area_GLF_45_3_502':
                        sumvalue = round(sumvalue / 1000, 4)
                    oc_dict_i["sumValue"] = sumvalue  # 蒸汽累计流量
                    oc_dict_i["SteamWD"] = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc + "WD"))  # 蒸汽体积
                    oc_dict_i_tag[oc] = oc_dict_i
                water_oclass = ast.literal_eval(returnb(redis_conn.hget(constant.REDIS_TABLENAME, "all_water_tags")))
                oc_dict_i_water_tag = {}
                for oc in water_oclass:
                    oc_water_dict_i = {}
                    oc_water_dict_i["flowValue"] = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc + "F"))
                    oc_water_dict_i["sumValue"] = abs(strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc + "S")))
                    oc_dict_i_water_tag[oc] = oc_water_dict_i
                electric_oclass = ast.literal_eval(returnb(redis_conn.hget(constant.REDIS_TABLENAME, "all_electric_tags")))
                oc_dict_i_electric_tag = {}
                for oc in electric_oclass:
                    oc_electric_dict_i = {}
                    oc_electric_dict_i["ZGL"] = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc + "_ZGL"))
                    oc_electric_dict_i["AU"] = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc + "_AU"))
                    oc_electric_dict_i["AI"] = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc + "_AI"))
                    oc_electric_dict_i["BU"] = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc + "_BU"))
                    oc_electric_dict_i["BI"] = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc + "_BI"))
                    oc_electric_dict_i["CU"] = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc + "_CU"))
                    oc_electric_dict_i["CI"] = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc + "_CI"))
                    oc_dict_i_electric_tag[oc] = oc_electric_dict_i
                oc_dict = {}
                oc_dict["steam"] = oc_dict_i_tag
                oc_dict["water"] = oc_dict_i_water_tag
                oc_dict["electric"] = oc_dict_i_electric_tag
                area_list.append(oc_dict)
                json_data = json.dumps(area_list)
                # bytemsg = bytes(json_data, encoding="utf8")
                # send_msg(c, bytes("recv: {}".format(data_parse), encoding="utf-8"))
                bytemsg = bytes(json_data,encoding="utf-8")
                send_msg(conn, bytemsg)
                runcount = runcount + 1
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
def strtofloat(f):
    if f == None or f == "" or f == b'':
        return 0.0
    else:
        return round(float(f), 2)
def returnb(rod):
    if rod == None or rod == "" or rod == b'':
        return ""
    else:
        return rod.decode()


def server_socket():
    try:
        redis_conn.hset(constant.REDIS_TABLENAME, "websocket_start",
                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", 5002))
        sock.listen(2)
        #将所有的tag写入redis
        Tags = db_session.query(TagDetail).filter().all()
        tag_steam_list = []
        tag_water_list = []
        tag_electric_list = []
        for tag in Tags:
            EnergyClass = str(tag.TagClassValue)[0:1]
            if EnergyClass == "S":
                tag_steam_list.append(tag.TagClassValue)
            elif EnergyClass == "W":
                tag_water_list.append(tag.TagClassValue)
            elif EnergyClass == "E":
                tag_electric_list.append(tag.TagClassValue)
        redis_conn.hset(constant.REDIS_TABLENAME, "all_steam_tags", str(tag_steam_list))
        redis_conn.hset(constant.REDIS_TABLENAME, "all_water_tags", str(tag_water_list))
        redis_conn.hset(constant.REDIS_TABLENAME, "all_electric_tags", str(tag_electric_list))
        areas = db_session.query(AreaTable).all()
        for area in areas:
            tagareas = db_session.query(TagDetail).filter(TagDetail.AreaName == area.AreaName).all()
            area_tag_list = []
            for ta in tagareas:
                area_tag_list.append(ta.TagClassValue)
            redis_conn.hset(constant.REDIS_TABLENAME, area.AreaName, str(area_tag_list))
        t = threading.Thread(target=handler_accept(sock))
        t.start()
    except Exception as e:
        print(e)
        redis_conn.hset(constant.REDIS_TABLENAME, "websocket_status", "执行失败")
    finally:
        t = threading.Thread(target=handler_accept(sock))
        t.start()


if __name__ == "__main__":
    server_socket()
