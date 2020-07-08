import configparser
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, r'database\config.ini')
config = configparser.ConfigParser()
config.read(CONFIG_DIR, encoding='UTF-8')

REDIS_HOST = config['data_realtime_server']['host']
REDIS_TABLENAME = config['data_realtime_server']['tablename']
REDIS_ZENGLIANG = config['data_realtime_server']['db_zengliang']
REDIS_PORT = int(config['data_realtime_server']['port']) if config['data_realtime_server'][
    'port'].isdigit() else 6379
REDIS_PASSWORD = config['data_realtime_server']['password']

MES_DATABASE_HOST = config['MES_DataBase']['host']
MES_DATABASE_USER = config['MES_DataBase']['user']
MES_DATABASE_PASSWD = config['MES_DataBase']['password']
MES_DATABASE_NAME = config['MES_DataBase']['database']
MES_DATABASE_CHARSET = config['MES_DataBase']['charset']


def transform_dict(position):
    if position:
        dict_ = dict()
        for key in eval(position).keys():
            dict_[key] = eval(position)[key]
        return dict_





myHours = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14","15", "16", "17", "18", "19", "20", "21", "22", "23"]
mydays = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
mymonths = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]